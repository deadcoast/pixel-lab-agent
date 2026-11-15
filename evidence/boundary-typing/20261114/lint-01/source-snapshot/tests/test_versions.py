import unittest

from pixl import codec


class VersionTests(unittest.TestCase):
    def test_existing_positional_document_defaults_to_px1(self):
        records = {"a": codec.Record("a", "A", {"nm": "x", "rl": codec.Symbol("agent")})}
        doc = codec.Document(7, records)
        self.assertEqual(doc.format, 1)
        self.assertEqual(codec.encode(doc), b"PX1 7\n@a:A{nm=~1:x;rl=agent}\n")

    def test_format_follows_existing_document_positional_arguments(self):
        records = {"a": codec.Record("a", "A", {})}
        doc = codec.Document(7, records, 2)
        self.assertEqual(codec.encode(doc), b"PX2 7\n@a:A{}\n")

    def test_px1_canonical_bytes_and_hashes_are_unchanged(self):
        doc = codec.parse(b"PX1\t0007\r\n@b:A{rl=tool;nm=~0:}\n@a:A{rl=agent;nm=~1:x}")
        self.assertEqual(
            codec.encode(doc),
            b"PX1 7\n@a:A{nm=~1:x;rl=agent}\n@b:A{nm=~0:;rl=tool}\n",
        )
        self.assertEqual(codec.digest(doc), "1a9688fe16350ec75ab1c31e2d08da33c6cde32e15202887bb068e970836f3da")
        self.assertEqual(codec.record_hash(doc.records["a"]), "43205c4cb7a10447a176c58034bb8bf6f01bc52a0f237675351c477d66b42d57")

    def test_px2_encoding_changes_document_identity_only(self):
        doc = codec.parse(b"PX1 7\n@b:A{rl=tool;nm=~0:}\n@a:A{rl=agent;nm=~1:x}")
        doc.format = 2
        self.assertEqual(
            codec.encode(doc),
            b"PX2 7\n@a:A{nm=~1:x;rl=agent}\n@b:A{nm=~0:;rl=tool}\n",
        )
        self.assertEqual(codec.digest(doc), "7da9dcc95dc329f4da995264cbb6eb2246964124f962b950449d4e3ab9fe0cd0")
        self.assertEqual(codec.record_hash(doc.records["a"]), "43205c4cb7a10447a176c58034bb8bf6f01bc52a0f237675351c477d66b42d57")

    def test_parsing_preserves_each_supported_format(self):
        for version in (1, 2):
            for whitespace in (" ", "\t", "\r", "\n"):
                with self.subTest(version=version, whitespace=whitespace):
                    raw = f"PX{version}{whitespace}0007\n@a:A{{x=[agent,~5:agent,@agent,+,-,?,0,-4,~3:火]}}"
                    doc = codec.parse(raw)
                    self.assertEqual(doc.format, version)
                    self.assertEqual(doc.records["a"].fields["x"], [
                        codec.Symbol("agent"), "agent", codec.Ref("agent"),
                        True, False, None, 0, -4, "火",
                    ])
                    self.assertEqual(codec.parse(codec.encode(doc)), doc)

    def test_encoder_rejects_unknown_or_noninteger_formats(self):
        for version in (0, -1, 3, 2**64, True, False, 1.0, 2.0, "1", "2", None, [], {}):
            with self.subTest(version=version):
                doc = codec.Document()
                doc.format = version
                with self.assertRaises(codec.PixlError) as caught:
                    codec.encode(doc)
                self.assertEqual(caught.exception.code, "format")

    def test_parser_requires_an_exact_supported_header(self):
        for header in (b"PX0", b"PX3", b"PX10", b"PX02", b"PX2x", b"px2", b" PX2", b"PX", b"PX2\x00"):
            with self.subTest(header=header), self.assertRaises(codec.PixlError):
                codec.parse(header + b" 0\n")
        for raw in (b"PX2", b"PX20\n", b"PX2 0", b"PX2 0@a:A{}"):
            with self.subTest(raw=raw), self.assertRaises(codec.PixlError):
                codec.parse(raw)

    def test_both_formats_keep_integer_and_nesting_limits(self):
        invalid_bodies = (
            b"-1\n", b"9223372036854775808\n",
            b"0\n@a:A{x=9223372036854775808}",
            b"0\n@a:A{x=-9223372036854775809}",
            b"0\n@a:A{x=" + b"[" * 70 + b"0" + b"]" * 70 + b"}",
        )
        for version in (1, 2):
            for body in invalid_bodies:
                with self.subTest(version=version, body=body), self.assertRaises(codec.PixlError):
                    codec.parse(f"PX{version} ".encode() + body)


if __name__ == "__main__":
    unittest.main()
