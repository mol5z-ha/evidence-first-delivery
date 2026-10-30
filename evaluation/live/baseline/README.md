# Export helper
collect(fetch_page) returns every item in upstream order, preserving duplicates.
fetch_page(cursor) returns {"items": list, "next_cursor": opaque token or None}.
Start with cursor=None. Only next_cursor=None means end of the sequence.
The upstream API may return an empty items list before the final page.
Opaque cursor tokens may be strings or numbers; pass them through unchanged.
The API guarantees a finite acyclic sequence. Exceptions should propagate.
