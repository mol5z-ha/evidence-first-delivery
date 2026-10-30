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

    def test_empty_final_page(self):
        pages = {None: {"items": ["a"], "next_cursor": "second"},
                 "second": {"items": [], "next_cursor": None}}
        self.assertEqual(collect(pages.__getitem__), ["a"])

    def test_only_empty_page(self):
        pages = {None: {"items": [], "next_cursor": None}}
        self.assertEqual(collect(pages.__getitem__), [])

    def test_falsy_cursors_are_not_terminal(self):
        pages = {None: {"items": ["a"], "next_cursor": 0},
                 0: {"items": ["b"], "next_cursor": ""},
                 "": {"items": ["c"], "next_cursor": None}}
        self.assertEqual(collect(pages.__getitem__), ["a", "b", "c"])

    def test_cursors_passed_through_unchanged(self):
        pages = {None: {"items": ["a"], "next_cursor": 1.5},
                 1.5: {"items": ["b"], "next_cursor": "07"},
                 "07": {"items": ["c"], "next_cursor": None}}
        seen = []
        def fetch_page(cursor):
            seen.append(cursor)
            return pages[cursor]
        collect(fetch_page)
        self.assertEqual(seen, [None, 1.5, "07"])
        self.assertIs(type(seen[1]), float)
        self.assertIs(type(seen[2]), str)

    def test_duplicates_preserved(self):
        pages = {None: {"items": ["a", "a"], "next_cursor": "second"},
                 "second": {"items": ["a", "b"], "next_cursor": None}}
        self.assertEqual(collect(pages.__getitem__), ["a", "a", "a", "b"])

    def test_exception_propagates(self):
        def fetch_page(cursor):
            if cursor is None:
                return {"items": ["a"], "next_cursor": "second"}
            raise RuntimeError("upstream failure")
        with self.assertRaises(RuntimeError):
            collect(fetch_page)

if __name__ == "__main__":
    unittest.main()
