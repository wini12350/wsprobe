"""WSProbe scanner. Restricted to loopback hosts for safe local practice."""
from __future__ import annotations
import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed
from .classifier import classify_message, classify_exception

DEFAULT_ORIGIN = "http://localhost:3000"
FOREIGN_ORIGIN = "https://attacker.example"
DEFAULT_TOKEN = "lab-token"
FUZZ_CASES = [
    ("valid_json_object", '{"type":"chat","message":"hello from WSProbe"}'),
    ("malformed_json", '{"type":'),
    ("unexpected_json_array", '["unexpected","array"]'),
    ("unexpected_json_number", '42'),
]

def validate_local_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ("ws", "wss") or not parsed.hostname:
        raise ValueError("URL must start with ws:// or wss:// and include a hostname.")
    if parsed.hostname.lower() not in ("localhost", "127.0.0.1", "::1"):
        raise ValueError("Safety stop: WSProbe only scans localhost/loopback URLs in this project.")

def headers_for(token: str | None) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"} if token else {}

async def handshake_probe(url: str, label: str, origin: str | None, token: str | None, timeout: float):
    record = {"probe": label, "origin": origin, "token_supplied": bool(token)}
    try:
        async with connect(
            url,
            origin=origin,
            additional_headers=headers_for(token),
            open_timeout=timeout,
            close_timeout=2,
            ping_interval=None,
        ):
            record.update({"classification": "accepted", "verdict": "REVIEW" if label != "baseline" else "PASS",
                           "evidence": "WebSocket handshake completed successfully."})
    except Exception as exc:
        evidence = f"{type(exc).__name__}: {exc}"
        status = None
        response = getattr(exc, "response", None)
        if response is not None:
            status = getattr(response, "status_code", None)
        if status is not None:
            evidence += f" (HTTP status {status})"
        record.update({"classification": "rejected", "verdict": "PASS", "evidence": evidence,
                       "http_status": status})
    return record

async def fuzz_probe(url: str, label: str, payload: str, token: str, timeout: float, max_fuzz_bytes: int):
    record = {"probe": label, "payload_bytes": len(payload.encode("utf-8"))}
    try:
        async with connect(
            url,
            origin=DEFAULT_ORIGIN,
            additional_headers=headers_for(token),
            open_timeout=timeout,
            close_timeout=2,
            ping_interval=None,
            max_size=max_fuzz_bytes * 2,
        ) as websocket:
            await websocket.send(payload)
            try:
                reply = await asyncio.wait_for(websocket.recv(), timeout=timeout)
                classification = classify_message(reply)
                record.update({
                    "classification": classification,
                    "verdict": "PASS" if classification in ("normal_reply", "error_reply") else "REVIEW",
                    "evidence": str(reply)[:500],
                })
            except asyncio.TimeoutError:
                record.update({"classification": "silence", "verdict": "REVIEW",
                               "evidence": f"No reply within {timeout:g} seconds."})
            except ConnectionClosed as exc:
                classification, evidence = classify_exception(exc)
                record.update({"classification": classification, "verdict": "PASS" if label == "oversized_frame" and "code=1009" in evidence else "REVIEW", "evidence": evidence})
    except Exception as exc:
        classification, evidence = classify_exception(exc)
        record.update({"classification": classification, "verdict": "REVIEW", "evidence": evidence})
    return record

async def run_scan(url: str, token: str, timeout: float, max_fuzz_bytes: int):
    validate_local_url(url)
    results = []
    results.append(await handshake_probe(url, "baseline", DEFAULT_ORIGIN, token, timeout))
    results.append(await handshake_probe(url, "foreign_origin", FOREIGN_ORIGIN, token, timeout))
    results.append(await handshake_probe(url, "missing_origin", None, token, timeout))
    results.append(await handshake_probe(url, "missing_authentication_token", DEFAULT_ORIGIN, None, timeout))

    fuzz_payloads = list(FUZZ_CASES)
    fuzz_payloads.append(("oversized_frame", "A" * (max_fuzz_bytes + 1)))
    for label, payload in fuzz_payloads:
        results.append(await fuzz_probe(url, label, payload, token, timeout, max_fuzz_bytes))

    accepted_foreign = next((r for r in results if r["probe"] == "foreign_origin"), {}).get("classification") == "accepted"
    accepted_missing_origin = next((r for r in results if r["probe"] == "missing_origin"), {}).get("classification") == "accepted"
    accepted_no_auth = next((r for r in results if r["probe"] == "missing_authentication_token"), {}).get("classification") == "accepted"
    summary = {
        "baseline_connection": "PASS" if results[0]["classification"] == "accepted" else "FAIL",
        "foreign_origin_check": "REVIEW - foreign Origin accepted" if accepted_foreign else "PASS - foreign Origin rejected",
        "missing_origin_check": "REVIEW - missing Origin accepted" if accepted_missing_origin else "PASS - missing Origin rejected",
        "authentication_check": "REVIEW - connection accepted without token" if accepted_no_auth else "PASS - missing token rejected",
        "note": "Origin acceptance is an observation, not proof of exploitable CSWSH. Review browser cookie/authentication behavior and server-side controls."
    }
    return {
        "tool": "WSProbe",
        "version": "1.0.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "target": url,
        "scope": "localhost/loopback lab only",
        "summary": summary,
        "probes": results,
    }

def main():
    parser = argparse.ArgumentParser(
        prog="wsprobe",
        description="WSProbe - local-lab WebSocket security tester (loopback targets only)."
    )
    parser.add_argument("--url", default="ws://127.0.0.1:8765", help="Local lab WebSocket URL")
    parser.add_argument("--token", default=DEFAULT_TOKEN, help="Lab bearer token (default: lab-token)")
    parser.add_argument("--output", default="reports/wsprobe-report.json", help="JSON report output path")
    parser.add_argument("--timeout", type=float, default=3.0, help="Seconds to wait for a response")
    parser.add_argument("--max-fuzz-bytes", type=int, default=70_000, help="Oversized frame test size in bytes")
    args = parser.parse_args()

    if args.timeout <= 0 or args.max_fuzz_bytes < 65_537:
        parser.error("--timeout must be positive and --max-fuzz-bytes must be at least 65537.")
    try:
        report = asyncio.run(run_scan(args.url, args.token, args.timeout, args.max_fuzz_bytes))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("\n=== WSProbe Results ===")
    for item in report["probes"]:
        print(f"[{item['verdict']}] {item['probe']}: {item['classification']}")
    print("\n=== Summary ===")
    for key, value in report["summary"].items():
        print(f"- {key}: {value}")
    print(f"\n[+] Full JSON report saved to: {output.resolve()}")

if __name__ == "__main__":
    main()
