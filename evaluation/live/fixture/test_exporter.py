import unittest
from exporter import collect

class ExportTests(unittest.TestCase):
    def test_two_pages(self):
        pages = {None: {"items": ["a", "b"], "next_cursor": "second"},
                 "second": {"items": ["c"], "next_cursor": None}}
        self.assertEqual(collect(pages.__getitem__), ["a", "b", "c"])

if __name__ == "__main__":
    unittest.main()
