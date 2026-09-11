import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import service
from pixl.codec import PixlError, encode, to_data
from tests.support import sample


class ServiceTests(unittest.TestCase):
    def test_host_json_bridge_preserves_types_and_bytes(self):
        with TemporaryDirectory() as tmp:
            doc = sample(Path(tmp))
            data = {
                "revision": doc.revision,
                "records": [
                    {"id": r.id, "kind": r.kind, "fields": to_data(r.fields)}
                    for r in doc.records.values()
                ],
            }
            self.assertEqual(encode(service.from_json(data)), encode(doc))

    def test_record_fields_cannot_decode_to_a_reference_or_symbol(self):
        for fields in ({"$ref": "actor"}, {"$symbol": "agent"}):
            with (
                self.subTest(fields=fields),
                self.assertRaisesRegex(PixlError, "record_shape"),
            ):
                service.from_json(
                    {
                        "revision": 0,
                        "records": [{"id": "actor", "kind": "A", "fields": fields}],
                    }
                )

    def test_source_slice_is_hash_grounded_and_never_silently_truncated(self):
        with TemporaryDirectory() as tmp:
            doc = sample(Path(tmp))
            path = Path(tmp) / "source.txt"
            expected = doc.records["source"].fields["dg"]
            result = service.source_slice(path, expected, 1, 1, 100)
            self.assertEqual(result["text"], "source intent\n")
            with self.assertRaisesRegex(PixlError, "source_budget"):
                service.source_slice(path, expected, 1, 1, 2)
            path.write_text("modified\n")
            with self.assertRaisesRegex(PixlError, "source_hash"):
                service.source_slice(path, expected, 1, 1, 100)

    def test_source_slice_rejects_invalid_ranges(self):
        with TemporaryDirectory() as tmp:
            doc = sample(Path(tmp))
            for start, end in [(0, 1), (2, 1), (1, 2)]:
                with self.subTest(start=start, end=end), self.assertRaises(PixlError):
                    service.source_slice(
                        Path(tmp) / "source.txt",
                        doc.records["source"].fields["dg"],
                        start,
                        end,
                    )
