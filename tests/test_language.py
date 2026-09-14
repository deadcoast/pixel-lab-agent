import unittest

from pixl import codec


class LanguageTests(unittest.TestCase):
    def test_compound_utf8_literal_roundtrip_and_canonical_order(self):
        doc = codec.parse(b"PX1 7\n@b:A{rl=agent;nm=~7:\xe7\x81\xab;[];}\n@a:A{nm=~0:;rl=tool}\n")
        self.assertEqual(doc.records["b"].fields["nm"], "火;[];")
        encoded = codec.encode(doc)
        self.assertTrue(encoded.startswith(b"PX1 7\n@a:A{"))
        self.assertEqual(codec.parse(encoded), doc)

    def test_types_remain_distinct(self):
        doc = codec.parse(b"PX1 0\n@a:A{x=[agent,~5:agent,@agent,+,-,?,0,-4]}\n")
        values = doc.records["a"].fields["x"]
        self.assertIsInstance(values[0], codec.Symbol)
        self.assertIsInstance(values[1], str)
        self.assertIsInstance(values[2], codec.Ref)
        self.assertEqual(values[3:], [True, False, None, 0, -4])

    def test_rejects_ambiguity_truncation_bad_utf8_and_duplicates(self):
        invalid = [b"PX3 0\n", b"PX1 -1\n", b"PX1 0\n@a:A{x=1;x=2}",
                   b"PX1 0\n@a:A{}@a:A{}", b"PX1 0\n@a:A{x=~4:hi}",
                   b"PX1 0\n@a:A{x=~1:\xe7}", b"PX1 0\n@a:A{x=1.5}",
                   b"PX1 0\n@a:A{x=9223372036854775808}", b"PX1 0\n@a:A{x=[1,]}"]
        for raw in invalid:
            with self.subTest(raw=raw), self.assertRaises(codec.PixlError):
                codec.parse(raw)

    def test_depth_limit(self):
        with self.assertRaises(codec.PixlError):
            codec.parse(b"PX1 0\n@a:A{x=" + b"[" * 70 + b"0" + b"]" * 70 + b"}")

    def test_record_hash_changes_only_with_semantics(self):
        a = codec.parse(b"PX1 0\n@a:A{rl=agent;nm=~1:x}")
        b = codec.parse(b"PX1 9\n@a:A{nm=~1:x;rl=agent}")
        self.assertEqual(codec.record_hash(a.records["a"]), codec.record_hash(b.records["a"]))
        self.assertNotEqual(codec.digest(a), codec.digest(b))


if __name__ == "__main__":
    unittest.main()
