"""Small, testable helpers for classifying WebSocket probe outcomes."""
from __future__ import annotations

def classify_message(message: str | bytes | None) -> str:
    """Classify a received application message as normal or error."""
    if message is None:
        return "silence"
    if isinstance(message, bytes):
        return "normal_reply"
    try:
        import json
        parsed = json.loads(message)
    except (ValueError, TypeError):
        return "normal_reply"
    if isinstance(parsed, dict) and str(parsed.get("status", "")).lower() == "error":
        return "error_reply"
    return "normal_reply"

def classify_exception(exc: BaseException) -> tuple[str, str]:
    """Return (classification, evidence) for a failed receive/handshake."""
    from websockets.exceptions import ConnectionClosed
    if isinstance(exc, ConnectionClosed):
        code = getattr(exc, "code", None)
        reason = getattr(exc, "reason", "") or ""
        return "close_frame", f"Connection closed (code={code}, reason={reason!r})"
    return "error_reply", f"{type(exc).__name__}: {exc}"
