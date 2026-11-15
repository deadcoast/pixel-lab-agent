"""Exercise ambiguous JSON at the real CLI and MCP process boundaries."""

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import service
from pixl.codec import PixlError


class JsonInputTests(unittest.TestCase):
    def cli(self, *arguments, stdin=None):
        return subprocess.run(
            [sys.executable, "-m", "pixl", *map(str, arguments)],
            input=stdin,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=15,
            check=False,
        )

    def test_cli_duplicate_members_do_not_overwrite_existing_output(self):
        documents = [
            '{"revision":1,"revision":0,"records":[]}',
            '{"revision":0,"format":1,"format":2,"records":[]}',
            (
                '{"revision":0,"records":[{"id":"a","kind":"A","fields":'
                '{"nm":"first","nm":"second","rl":{"$symbol":"agent"}}}]}'
            ),
            # JSON escapes are decoded before member names are compared.
            (
                '{"revision":0,"records":[{"id":"a","kind":"A","fields":'
                '{"nm":"first","n\\u006d":"second","rl":{"$symbol":"agent"}}}]}'
            ),
        ]
        with TemporaryDirectory() as tmp:
            source, output = Path(tmp) / "input.json", Path(tmp) / "saved.px"
            original = b"PX1 7\n@old:A{nm=~4:kept;rl=agent}\n"
            for document in documents:
                with self.subTest(document=document):
                    source.write_text(document, encoding="utf-8")
                    output.write_bytes(original)
                    result = self.cli("encode", source, "--out", output)
                    self.assertEqual(
                        result.returncode, 2, result.stdout + result.stderr
                    )
                    self.assertEqual(json.loads(result.stderr)["error"], "json_read")
                    self.assertEqual(result.stdout, "")
                    self.assertEqual(output.read_bytes(), original)

    def test_cli_round_trip_preserves_both_formats_and_distinct_objects(self):
        with TemporaryDirectory() as tmp:
            for version in (1, 2):
                with self.subTest(version=version):
                    source = Path(tmp) / "input.json"
                    wire = Path(tmp) / "output.px"
                    document = {
                        "revision": 0,
                        "records": [
                            {
                                "id": "a",
                                "kind": "A",
                                "fields": {"nm": "one", "rl": {"$symbol": "agent"}},
                            },
                            {
                                "id": "b",
                                "kind": "A",
                                "fields": {"nm": "two", "rl": {"$symbol": "agent"}},
                            },
                        ],
                    }
                    if version == 2:
                        document["format"] = 2
                    source.write_text(json.dumps(document), encoding="utf-8")
                    result = self.cli("encode", source, "--out", wire)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(
                        wire.read_bytes(),
                        (
                            f"PX{version} 0\n@a:A{{nm=~3:one;rl=agent}}\n"
                            "@b:A{nm=~3:two;rl=agent}\n"
                        ).encode(),
                    )
                    result = self.cli("decode", wire)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    decoded = json.loads(result.stdout)
                    self.assertEqual(decoded["records"], document["records"])
                    self.assertEqual(decoded.get("format", 1), version)

    def test_mcp_ambiguous_mutation_is_rejected_before_store_creation(self):
        requests = [
            (
                '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":'
                '{"name":"pixl_init","arguments":{"store":"first","store":"second"}}}'
            ),
            (
                '{"jsonrpc":"2.0","id":2,"method":"ping","method":"tools/call",'
                '"params":{"name":"pixl_init","arguments":{"store":"third"}}}'
            ),
            '{"jsonrpc":"2.0","id":3,"method":"ping"}',
        ]
        with TemporaryDirectory() as tmp:
            result = self.cli("mcp", "--root", tmp, stdin="\n".join(requests) + "\n")
            self.assertEqual(result.returncode, 0, result.stderr)
            replies = [json.loads(line) for line in result.stdout.splitlines()]
            self.assertEqual(len(replies), 3)
            for reply in replies[:2]:
                self.assertEqual(reply.get("error", {}).get("code"), -32700, reply)
                self.assertIsNone(reply["id"])
            self.assertEqual(replies[2], {"jsonrpc": "2.0", "id": 3, "result": {}})
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_mcp_duplicate_document_fields_then_valid_encode(self):
        ambiguous = (
            '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":'
            '{"name":"pixl_encode","arguments":{"document":{"revision":0,'
            '"records":[{"id":"a","kind":"A","fields":{"nm":"lost",'
            '"nm":"kept","rl":{"$symbol":"agent"}}}]}}}}'
        )
        valid = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "pixl_encode",
                "arguments": {
                    "document": {
                        "revision": 0,
                        "records": [
                            {
                                "id": "a",
                                "kind": "A",
                                "fields": {
                                    "nm": "kept",
                                    "rl": {"$symbol": "agent"},
                                },
                            }
                        ],
                    }
                },
            },
        }
        with TemporaryDirectory() as tmp:
            result = self.cli(
                "mcp", "--root", tmp, stdin=ambiguous + "\n" + json.dumps(valid) + "\n"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            replies = [json.loads(line) for line in result.stdout.splitlines()]
            self.assertEqual(
                replies[0].get("error", {}).get("code"), -32700, replies[0]
            )
            self.assertFalse(replies[1]["result"]["isError"])
            self.assertEqual(
                replies[1]["result"]["structuredContent"]["wire"],
                "PX1 0\n@a:A{nm=~4:kept;rl=agent}\n",
            )

    def test_file_json_rejects_duplicate_nested_members_and_nonfinite_numbers(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "observation.json"
            for value in (
                '{"evidence":{"status":"fail","status":"pass"}}',
                '{"value":NaN}',
                '{"value":Infinity}',
                '{"value":-Infinity}',
            ):
                with self.subTest(value=value):
                    path.write_text(value, encoding="utf-8")
                    with self.assertRaisesRegex(PixlError, "json_read"):
                        service.read_json(path)
