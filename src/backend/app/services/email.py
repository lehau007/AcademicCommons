"""Email sending wrapper.

Two backends, selected by `settings.email_backend`:

- ``console`` (default): no external dependency. The verification link/OTP is
  written to the application logger (and thus to stdout / `docker logs`),
  which is what tests and local dev rely on.
- ``resend``: production. Sends real mail through the Resend SDK using
  ``settings.resend_api_key`` and ``settings.resend_from`` as the From address.

Failures in either backend are swallowed and logged: registration must NOT
abort just because the mail provider is unreachable — the user can still use
the "resend verification" flow afterwards.
"""

from __future__ import annotations

import asyncio
import logging

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def send_email(to: str, subject: str, html: str) -> None:
    """Send an email via the configured backend, swallowing provider errors."""
    backend = (settings.email_backend or "console").strip().lower()
    if backend == "resend":
        await _send_via_resend(to, subject, html)
    else:
        _send_via_console(to, subject, html)


def _send_via_console(to: str, subject: str, html: str) -> None:
    # Tests grep stdout / docker logs for the verification link/OTP.
    logger.info(
        "[email.console] to=%s subject=%s body_start=%s",
        to,
        subject,
        html[:2000],
    )
    print(f"[email.console] to={to} subject={subject}\n{html}", flush=True)


async def _send_via_resend(to: str, subject: str, html: str) -> None:
    if not settings.resend_api_key:
        logger.warning(
            "email_backend=resend but RESEND_API_KEY is unset; falling back to console. "
            "to=%s subject=%s",
            to,
            subject,
        )
        _send_via_console(to, subject, html)
        return

    try:
        import resend

        resend.api_key = settings.resend_api_key
        params = {
            "from": settings.resend_from,
            "to": [to],
            "subject": subject,
            "html": html,
        }
        # resend SDK's send() is blocking (sync HTTP); off-load it so it never
        # stalls the event loop and blocks other in-flight requests.
        await asyncio.to_thread(resend.Emails.send, params)  # type: ignore[arg-type]
        logger.info("email.sent via resend to=%s subject=%s", to, subject)
    except Exception as exc:  # noqa: BLE001 — provider SDK raises arbitrary types
        logger.warning("email.send_failed via resend to=%s err=%s", to, exc)