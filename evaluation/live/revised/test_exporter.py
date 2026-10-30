import unittest
from exporter import collect

class ExportTests(unittest.TestCase):
    def test_two_pages(self):
        pages = {None: {"items": ["a", "b"], "next_cursor": "second"},
                 "second": {"items": ["c"], "next_cursor": None}}
        self.assertEqual(collect(pages.__getitem__), ["a", "b", "c"])

    def test_empty_page_before_final_page(self):
        pages = {None: {"items": ["a"], "next_cursor": "second"},
                 "second": {"items": [], "next_cursor": "third"},
                 "third": {"items": ["b"], "next_cursor": None}}
        self.assertEqual(collect(pages.__getitem__), ["a", "b"])

    def test_empty_first_page(self):
        pages = {None: {"items": [], "next_cursor": "second"},
                 "second": {"items": ["a"], "next_cursor": None}}
        self.assertEqual(collect(pages.__getitem__), ["a"])

    def test_consecutive_empty_pages_and_empty_final_page(self):
        pages = {None: {"items": ["a"], "next_cursor": 1},
                 1: {"items": [], "next_cursor": 2},
                 2: {"items": [], "next_cursor": 3},
                 3: {"items": ["b"], "next_cursor": 4},
                 4: {"items": [], "next_cursor": None}}
        self.assertEqual(collect(pages.__getitem__), ["a", "b"])

    def test_all_pages_empty(self):
        pages = {None: {"items": [], "next_cursor": None}}
        self.assertEqual(collect(pages.__getitem__), [])

    def test_falsy_cursors_are_passed_through_unchanged(self):
        calls = []
        pages = {None: {"items": ["a"], "next_cursor": 0},
                 0: {"items": [], "next_cursor": ""},
                 "": {"items": ["b"], "next_cursor": None}}
        def fetch_page(cursor):
            calls.append(cursor)
            return pages[cursor]
        self.assertEqual(collect(fetch_page), ["a", "b"])
        self.assertEqual(calls, [None, 0, ""])
        self.assertIs(type(calls[1]), int)

    def test_preserves_duplicates_and_order(self):
        pages = {None: {"items": ["b", "a", "b"], "next_cursor": "second"},
                 "second": {"items": ["a", "a"], "next_cursor": None}}
        self.assertEqual(collect(pages.__getitem__), ["b", "a", "b", "a", "a"])

    def test_fetch_error_propagates_after_empty_page(self):
        pages = {None: {"items": [], "next_cursor": "second"}}
        with self.assertRaises(KeyError):
            collect(pages.__getitem__)

if __name__ == "__main__":
    unittest.main()
