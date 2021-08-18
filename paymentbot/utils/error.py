import html


def error(e: Exception) -> str:
    return html.escape(f"{type(e)} | {type(e).__name__} | {e}")
