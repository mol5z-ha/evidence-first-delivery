def collect(fetch_page):
    """Return items in API order. None is the only terminal next_cursor."""
    result = []
    page = fetch_page(None)
    while True:
        result.extend(page["items"])
        cursor = page["next_cursor"]
        if cursor is None:
            break
        page = fetch_page(cursor)
    return result
