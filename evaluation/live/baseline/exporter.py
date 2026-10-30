def collect(fetch_page):
    """Return items in API order. None is the only terminal next_cursor."""
    result = []
    cursor = None
    while True:
        page = fetch_page(cursor)
        result.extend(page["items"])
        cursor = page["next_cursor"]
        if cursor is None:
            return result
