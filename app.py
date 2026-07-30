from __future__ import annotations

import html
import json
import logging
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Spider Invite", page_icon="🕷️", layout="wide")

LOGGER = logging.getLogger("spider_invite")
MELBOURNE_TZ = ZoneInfo("Australia/Melbourne")
MAX_NAME_LENGTH = 40
YES_SCALE_MIN = 1.0
YES_SCALE_MAX = 1.9
APP_DIR = Path(__file__).resolve().parent
RESPONSE_LOG_FILE = APP_DIR / "yes_responses.jsonl"
YES_WEBHOOK_URL = "https://eouzyq6a3g725gg.m.pipedream.net"


def init_session_state() -> None:
    """Initialize all session fields used by the app."""
    if "visitor_name" not in st.session_state:
        st.session_state.visitor_name = ""

    if "name_submitted" not in st.session_state:
        st.session_state.name_submitted = False

    if "response_submitted" not in st.session_state:
        st.session_state.response_submitted = False

    if "submitted_answer" not in st.session_state:
        st.session_state.submitted_answer = ""

    if "email_sent" not in st.session_state:
        st.session_state.email_sent = False

    if "no_escape_count" not in st.session_state:
        st.session_state.no_escape_count = 0

    if "yes_scale" not in st.session_state:
        st.session_state.yes_scale = 1.0

    if "json_logged" not in st.session_state:
      st.session_state.json_logged = False

    if "last_save_error" not in st.session_state:
      st.session_state.last_save_error = ""

    if "yes_notification_sent" not in st.session_state:
      st.session_state.yes_notification_sent = False

    if "yes_notification_attempted" not in st.session_state:
      st.session_state.yes_notification_attempted = False

    if "webhook_success" not in st.session_state:
      st.session_state.webhook_success = False


def inject_base_page_css() -> None:
    """Hide default Streamlit chrome and keep iframe edge to edge."""
    st.markdown(
        """
        <style>
          .stAppHeader, [data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer {
            visibility: hidden;
            height: 0;
            position: fixed;
          }
          [data-testid="stHeaderActionElements"] {
            display: none;
          }
          .block-container {
            max-width: 100% !important;
            padding: 0 !important;
          }
          div[data-testid="stMarkdownContainer"] p {
            margin-bottom: 0;
          }
          iframe {
            border: 0 !important;
          }
          .main-yes-anchor {
            position: relative;
            z-index: 90;
            width: clamp(180px, 30vw, 240px);
            margin-top: -156px;
            margin-left: clamp(300px, 55vw, 720px);
            margin-bottom: 88px;
            pointer-events: auto !important;
          }
          .main-yes-anchor div[data-testid="stButton"] {
            margin: 0 !important;
          }
          .main-yes-anchor div[data-testid="stButton"] button {
            width: 100% !important;
            min-height: clamp(64px, 9vw, 76px) !important;
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            color: #ffffff !important;
            font-size: clamp(1.15rem, 4vw, 1.45rem) !important;
            font-weight: 900 !important;
            line-height: 1 !important;
            background: linear-gradient(130deg, #f14f60, #df3042) !important;
            box-shadow: 0 10px 24px rgba(223, 48, 66, 0.42) !important;
          }
          @media (max-width: 760px) {
            .main-yes-anchor {
              width: clamp(170px, 46vw, 220px);
              margin-top: -170px;
              margin-left: clamp(150px, 52vw, 320px);
              margin-bottom: 100px;
            }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sanitize_name(raw_name: str) -> str:
    """Trim spaces and constrain length for safe display."""
    return raw_name.strip()[:MAX_NAME_LENGTH]


def render_name_entry_card() -> None:
    """Render the first screen that asks for the visitor name."""
    st.markdown(
        """
        <style>
          .welcome-background {
            position: fixed;
            inset: 0;
            background: radial-gradient(circle at 20% 15%, #203768 0%, #111827 38%, #090d16 80%, #060910 100%);
            z-index: -2;
            pointer-events: none !important;
          }
          .welcome-pattern {
            position: fixed;
            inset: 0;
            background-image: radial-gradient(rgba(255, 255, 255, 0.12) 1px, transparent 1px);
            background-size: 14px 14px;
            opacity: 0.24;
            z-index: -1;
            pointer-events: none !important;
          }
          .welcome-shell {
            max-width: 560px;
            margin: min(8vh, 72px) auto 0 auto;
            border-radius: 24px;
            border: 2px solid rgba(255, 255, 255, 0.16);
            background: linear-gradient(155deg, rgba(220, 47, 63, 0.18), rgba(20, 84, 216, 0.2), rgba(8, 12, 20, 0.92));
            box-shadow: 0 24px 58px rgba(0, 0, 0, 0.38);
            padding: clamp(18px, 5vw, 34px);
            backdrop-filter: blur(3px);
            animation: welcomeEnter 700ms ease;
            position: relative;
            pointer-events: auto !important;
            z-index: 20;
          }
          @keyframes welcomeEnter {
            from {
              opacity: 0;
              transform: translateY(20px) scale(0.98);
            }
            to {
              opacity: 1;
              transform: translateY(0) scale(1);
            }
          }
          .welcome-web {
            position: absolute;
            width: clamp(70px, 16vw, 115px);
            opacity: 0.35;
            pointer-events: none !important;
            z-index: 1;
          }
          .welcome-web.wl {
            top: 6px;
            left: 8px;
            transform: rotate(-8deg);
          }
          .welcome-web.wr {
            top: 8px;
            right: 10px;
            transform: rotate(10deg);
          }
          .welcome-shell h1 {
            margin: 0 0 10px 0;
            color: #fff4cc;
            line-height: 1.25;
            font-size: clamp(1.45rem, 4.8vw, 2.2rem);
          }
          .welcome-shell p {
            color: #dbe9ff !important;
            font-weight: 700;
          }
          .welcome-shell div[data-testid="stForm"] {
            margin-top: 10px;
          }
          div[data-testid="stForm"] {
            position: relative;
            z-index: 20;
            pointer-events: auto !important;
          }
          div[data-testid="stTextInput"] {
            position: relative;
            z-index: 20;
            pointer-events: auto !important;
          }
          div[data-testid="stTextInput"] label p {
            color: #ffe8a2 !important;
            font-weight: 800 !important;
            letter-spacing: 0.03em;
          }
          div[data-testid="stTextInput"] input {
            pointer-events: auto !important;
            cursor: text !important;
            color: #ffffff !important;
            caret-color: #ffffff !important;
            background: rgba(8, 18, 45, 0.9) !important;
            border: 2px solid rgba(255, 255, 255, 0.35) !important;
            border-radius: 12px !important;
            font-size: 1rem !important;
            min-height: 48px !important;
            opacity: 1 !important;
            visibility: visible !important;
            display: block !important;
          }
          div[data-testid="stTextInput"] input::placeholder {
            color: rgba(255, 255, 255, 0.72) !important;
          }
          div[data-testid="stFormSubmitButton"] {
            position: relative;
            z-index: 20;
            pointer-events: auto !important;
          }
          div[data-testid="stFormSubmitButton"] button {
            width: 100%;
            min-height: 48px;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.28);
            color: white;
            font-size: 1.03rem;
            font-weight: 800;
            background: linear-gradient(130deg, #df3042, #1a59da);
            transition: transform 150ms ease, filter 150ms ease;
            pointer-events: auto !important;
            cursor: pointer !important;
          }
          div[data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-1px);
            filter: brightness(1.06);
          }
          @media (max-width: 640px) {
            .welcome-shell {
              padding: 16px;
              margin-top: 24px;
            }
          }
        </style>
        <div class="welcome-background"></div>
        <div class="welcome-pattern"></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="welcome-shell">
          <svg class="welcome-web wl" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cfe7ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
          <svg class="welcome-web wr" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cfe7ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
        """,
        unsafe_allow_html=True,
    )

    st.title("Enter your name 🕷️")
    st.write("Your spider mission starts here.")

    with st.form("name_form", clear_on_submit=False):
        name = st.text_input(
            "NAME",
            placeholder="Type your name here...",
            max_chars=40,
        )

        submitted = st.form_submit_button(
            "Next 🕷️",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        cleaned_name = name.strip()

        if not cleaned_name:
            st.error("Please enter your name first 🕷️")
        else:
            st.session_state.visitor_name = cleaned_name
            st.session_state.name_submitted = True
            st.rerun()


def send_yes_email(visitor_name: str) -> bool:
    """Send one secure YES notification email using Streamlit secrets."""
    try:
        sender = st.secrets["EMAIL_SENDER"]
        recipient = st.secrets["EMAIL_RECIPIENT"]
        app_password = st.secrets["EMAIL_APP_PASSWORD"]
    except Exception:
        LOGGER.warning("Email send skipped: required Streamlit secrets are missing.")
        return False

    response_time = datetime.now(MELBOURNE_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")
    subject = "Spider-Man invitation response: YES ❤️"
    body = (
        f"{visitor_name} clicked YES on your Spider-Man movie invitation! ❤️🕷️\n\n"
        f"Name: {visitor_name}\n"
        "Selected answer: YES\n"
        f"Response time (Australia/Melbourne): {response_time}\n"
        "Source: Response came from the Spider-Man invitation app.\n"
    )

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20) as smtp:
            smtp.login(sender, app_password)
            smtp.send_message(message)
        return True
    except Exception as exc:  # pragma: no cover
        LOGGER.warning("Email delivery failed safely. Error type: %s", type(exc).__name__)
        return False


def notify_backend(visitor_name: str, answer: str) -> bool:
  """Send webhook notification to backend for the submitted answer."""
  payload = {
    "name": visitor_name,
    "answer": answer,
    "timestamp": datetime.now(MELBOURNE_TZ).isoformat(),
  }

  try:
    response = requests.post(YES_WEBHOOK_URL, json=payload, timeout=10)
    status = int(response.status_code)
    LOGGER.info("YES webhook status: %s", status)
    return 200 <= status < 300
  except Exception as exc:  # pragma: no cover
    LOGGER.warning("YES webhook send failed safely. Error type: %s", type(exc).__name__)
    print(f"YES webhook send failed safely: {type(exc).__name__}")
    return False


def log_yes_response_json(visitor_name: str) -> tuple[bool, str]:
    """Append a YES response record to a local JSONL file."""
    payload = {
        "name": visitor_name,
        "answer": "YES",
        "response_time_melbourne": datetime.now(MELBOURNE_TZ).isoformat(),
        "source": "spiderman-invitation-app",
    }

    try:
        RESPONSE_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with RESPONSE_LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return True, ""
    except Exception as exc:  # pragma: no cover
        LOGGER.warning("JSON response logging failed safely. Error type: %s", type(exc).__name__)
        return False, f"{type(exc).__name__}: {exc}"


def clamp_yes_scale(value: float) -> float:
    """Keep the Yes button growth in a mobile-safe range."""
    return max(YES_SCALE_MIN, min(YES_SCALE_MAX, value))


def submit_yes_response(visitor_name: str, *, attempts: int, yes_scale: float) -> None:
  """Persist YES response and send notification once per session."""
  if st.session_state.response_submitted:
    return

  st.session_state.no_escape_count = max(st.session_state.no_escape_count, max(0, attempts))
  st.session_state.yes_scale = max(float(st.session_state.yes_scale), clamp_yes_scale(yes_scale))
  st.session_state.response_submitted = True
  st.session_state.submitted_answer = "YES"

  # Keep a temporary local record for each successful YES action.
  logged, save_error = log_yes_response_json(visitor_name)
  st.session_state.json_logged = logged
  st.session_state.last_save_error = save_error

  if not st.session_state.yes_notification_attempted and not st.session_state.yes_notification_sent:
    success = notify_backend(st.session_state.visitor_name, "YES")
    st.session_state.yes_notification_attempted = True
    if success:
      st.session_state.yes_notification_sent = True

  # Send email once per session only.
  if not st.session_state.email_sent:
    st.session_state.email_sent = send_yes_email(visitor_name)


def process_component_event(event_payload: object) -> None:
    """Handle events from the custom HTML component."""
    if not isinstance(event_payload, dict):
        return

    event_type = str(event_payload.get("type", "")).strip().lower()
    attempts_raw = event_payload.get("attempts", st.session_state.no_escape_count)
    scale_raw = event_payload.get("yes_scale", st.session_state.yes_scale)

    try:
        attempts = max(0, int(attempts_raw))
    except (TypeError, ValueError):
        attempts = st.session_state.no_escape_count

    try:
        yes_scale = clamp_yes_scale(float(scale_raw))
    except (TypeError, ValueError):
        yes_scale = float(st.session_state.yes_scale)

    if event_type == "progress" and not st.session_state.response_submitted:
        st.session_state.no_escape_count = max(st.session_state.no_escape_count, attempts)
        st.session_state.yes_scale = max(float(st.session_state.yes_scale), yes_scale)
        return

    # YES submission is handled by the real Streamlit button in Python.
    return


def retry_save_yes_response() -> None:
    """Retry writing a YES response when the first save attempt failed."""
    if not st.session_state.response_submitted or st.session_state.json_logged:
        return

    logged, save_error = log_yes_response_json(st.session_state.visitor_name)
    st.session_state.json_logged = logged
    st.session_state.last_save_error = save_error


def retry_notification() -> None:
    """Retry webhook notification only when the previous attempt failed."""
    if st.session_state.yes_notification_sent:
        return

    success = notify_backend(st.session_state.visitor_name, "YES")
    st.session_state.webhook_success = success
    if success:
        st.session_state.yes_notification_sent = True


def build_invitation_html(
    *,
    safe_visitor_name: str,
    response_submitted: bool,
    submitted_answer: str,
    email_sent: bool,
    no_escape_count: int,
    yes_scale: float,
) -> str:
    """Build responsive invitation UI with custom pointer and touch behavior."""
    invite_text = (
        f"Would {safe_visitor_name} be interested in going to watch the Spider-Man movie on "
        "31/07 evening? 🕷️❤️"
    )
    yes_scale_clamped = clamp_yes_scale(yes_scale)
    submitted_attr = "true" if response_submitted else "false"
    sent_note = "Your answer has been sent 🕷️" if email_sent else "Your answer was received ❤️"

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Spider Invite</title>
  <style>
    :root {{
      --red: #df3042;
      --blue: #1454d8;
      --ink: #0d121f;
      --paper: #fffaf2;
      --gold: #ffe082;
      --yes-scale: {yes_scale_clamped};
    }}

    * {{ box-sizing: border-box; }}

    html, body {{
      margin: 0;
      width: 100%;
      height: 100%;
      overflow-x: hidden;
      font-family: "Trebuchet MS", "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 18% 12%, #214174 0%, #111827 34%, #090d15 76%, #060910 100%);
      color: #f4f8ff;
    }}

    .stage {{
      min-height: 100dvh;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: clamp(8px, 2.2vw, 22px);
      overflow: hidden;
      position: relative;
      isolation: isolate;
    }}

    .stage::before {{
      content: "";
      position: absolute;
      inset: 0;
      opacity: 0.23;
      background-image: radial-gradient(rgba(255, 255, 255, 0.12) 1px, transparent 1px);
      background-size: 14px 14px;
      z-index: -6;
    }}

    .cityline {{
      position: absolute;
      inset: auto 0 0 0;
      height: 23dvh;
      min-height: 105px;
      background: linear-gradient(180deg, rgba(5, 8, 12, 0) 0%, rgba(5, 8, 12, 0.86) 45%, rgba(5, 8, 12, 1) 100%);
      z-index: -5;
    }}

    .cityline::before {{
      content: "";
      position: absolute;
      inset: auto 0 0 0;
      height: 100%;
      background:
        linear-gradient(to right,
          transparent 0 3%, #091221 3% 8%, transparent 8% 10%, #0b1528 10% 15%, transparent 15% 19%,
          #091221 19% 24%, transparent 24% 27%, #0b1628 27% 32%, transparent 32% 36%, #08111f 36% 41%,
          transparent 41% 44%, #0b1628 44% 49%, transparent 49% 52%, #091323 52% 58%, transparent 58% 62%,
          #0b1528 62% 67%, transparent 67% 72%, #08111f 72% 78%, transparent 78% 81%, #0b1628 81% 87%,
          transparent 87% 90%, #091321 90% 95%, transparent 95% 100%);
    }}

    .web {{
      position: absolute;
      width: clamp(70px, 12vw, 130px);
      opacity: 0.35;
      pointer-events: none;
      animation: drift 9s ease-in-out infinite;
      z-index: -4;
    }}

    .w1 {{ top: 2%; left: 2%; }}
    .w2 {{ top: 7%; right: 4%; animation-delay: 1s; }}
    .w3 {{ bottom: 21%; left: 6%; animation-delay: 2s; }}
    .w4 {{ bottom: 23%; right: 7%; animation-delay: 2.8s; }}

    @keyframes drift {{
      0%, 100% {{ transform: translateY(0) rotate(0deg); }}
      50% {{ transform: translateY(-10px) rotate(4deg); }}
    }}

    .sparkle {{
      position: absolute;
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #ffe596;
      box-shadow: 0 0 10px #ffe596;
      animation: twinkle 2.3s ease-in-out infinite;
      pointer-events: none;
      z-index: -3;
    }}

    @keyframes twinkle {{
      0%, 100% {{ transform: scale(0.7); opacity: 0.35; }}
      50% {{ transform: scale(1.35); opacity: 1; }}
    }}

    .card {{
      width: min(930px, 100%);
      min-height: min(760px, calc(100dvh - 16px));
      border-radius: clamp(18px, 3vw, 28px);
      border: 2px solid rgba(255, 255, 255, 0.14);
      background: linear-gradient(145deg, rgba(19, 30, 55, 0.96), rgba(19, 15, 32, 0.92));
      box-shadow: 0 24px 70px rgba(0, 0, 0, 0.4);
      padding: clamp(14px, 3.2vw, 34px);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      gap: clamp(10px, 2.2vw, 18px);
      animation: riseIn 760ms cubic-bezier(.2, 1, .2, 1);
    }}

    .card::before {{
      content: "";
      position: absolute;
      inset: -120% -20% auto -20%;
      height: 260%;
      background: linear-gradient(120deg, rgba(223, 48, 66, 0.22), rgba(20, 84, 216, 0.24), rgba(255, 224, 130, 0.14));
      transform: rotate(10deg);
      pointer-events: none;
    }}

    @keyframes riseIn {{
      from {{ opacity: 0; transform: translateY(24px) scale(0.98); }}
      to {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    .spider-wrap {{
      position: absolute;
      top: -14px;
      left: 50%;
      transform: translateX(-50%);
      width: 74px;
      height: 170px;
      pointer-events: none;
      animation: swing 2.9s ease-in-out infinite;
      transform-origin: top center;
      z-index: 2;
    }}

    .thread {{
      width: 2px;
      height: 108px;
      margin: 0 auto;
      background: linear-gradient(180deg, rgba(245, 248, 255, 0.82), rgba(255, 255, 255, 0.12));
    }}

    .spider {{
      width: 32px;
      height: 40px;
      margin: -2px auto 0;
      position: relative;
    }}

    .spider-body {{
      width: 24px;
      height: 27px;
      border-radius: 50% 50% 56% 56%;
      margin: 0 auto;
      background: #0d121f;
      border: 1px solid #30384b;
      position: relative;
    }}

    .spider-body::before {{
      content: "";
      position: absolute;
      left: 6px;
      top: -6px;
      width: 11px;
      height: 8px;
      border-radius: 50%;
      background: #151d2b;
      border: 1px solid #30384b;
    }}

    .leg {{
      position: absolute;
      width: 14px;
      height: 2px;
      background: #2c3447;
      top: 9px;
      transform-origin: 0% 50%;
    }}

    .l1 {{ left: -7px; transform: rotate(35deg); }}
    .l2 {{ left: -8px; top: 14px; transform: rotate(8deg); }}
    .l3 {{ right: -7px; transform: scaleX(-1) rotate(35deg); }}
    .l4 {{ right: -8px; top: 14px; transform: scaleX(-1) rotate(8deg); }}

    @keyframes swing {{
      0%, 100% {{ transform: translateX(-50%) rotate(-2.8deg); }}
      50% {{ transform: translateX(-50%) rotate(4deg); }}
    }}

    .chip {{
      align-self: flex-start;
      display: inline-flex;
      align-items: center;
      gap: 9px;
      padding: 9px 13px;
      border-radius: 999px;
      font-size: clamp(0.74rem, 2.4vw, 0.94rem);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      font-weight: 800;
      color: #ffeaa8;
      border: 1px solid rgba(255, 235, 167, 0.33);
      background: rgba(255, 220, 119, 0.13);
      z-index: 2;
    }}

    .chip-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #ffeaa8;
      box-shadow: 0 0 10px #ffeaa8;
    }}

    .bubble {{
      position: relative;
      z-index: 2;
      border-radius: clamp(14px, 3.3vw, 22px);
      border: 3px solid #121a2d;
      background: var(--paper);
      color: #131826;
      box-shadow: 6px 6px 0 #101623;
      padding: clamp(14px, 4vw, 28px);
      min-height: clamp(112px, 22vw, 170px);
      display: flex;
      align-items: center;
    }}

    .bubble::after {{
      content: "";
      position: absolute;
      left: 36px;
      bottom: -16px;
      width: 20px;
      height: 20px;
      background: var(--paper);
      border-left: 3px solid #121a2d;
      border-bottom: 3px solid #121a2d;
      transform: rotate(-45deg);
    }}

    .invite-text {{
      margin: 0;
      font-size: clamp(1.02rem, 3.7vw, 2.05rem);
      line-height: 1.35;
      font-weight: 900;
      text-wrap: pretty;
      overflow-wrap: break-word;
    }}

    .status {{
      min-height: 30px;
      font-size: clamp(0.95rem, 2.7vw, 1.05rem);
      color: #ffebad;
      font-weight: 800;
      z-index: 2;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.28);
    }}

    .arena {{
      position: relative;
      z-index: 2;
      border-radius: 18px;
      border: 1px dashed rgba(255, 255, 255, 0.28);
      background: rgba(7, 12, 23, 0.42);
      min-height: clamp(160px, 28vh, 255px);
      overflow: hidden;
    }}

    .action-btn {{
      position: absolute;
      border: 0;
      border-radius: 14px;
      min-height: clamp(52px, 8vw, 60px);
      min-width: clamp(130px, 26vw, 170px);
      padding: clamp(12px, 2.2vw, 16px) clamp(18px, 2.4vw, 24px);
      font-size: clamp(1.02rem, 3.5vw, 1.25rem);
      font-weight: 900;
      line-height: 1;
      color: #ffffff;
      border: 1px solid rgba(255, 255, 255, 0.3);
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
      user-select: none;
      cursor: pointer;
    }}

    .no-btn {{
      left: 70%;
      top: 45%;
      transform: translate(-50%, -50%) rotate(0deg);
      background: linear-gradient(130deg, #3f7dff, #1454d8);
      box-shadow: 0 10px 24px rgba(20, 84, 216, 0.4);
      transition: left 70ms linear, top 70ms linear, transform 70ms linear;
      z-index: 2;
    }}

    .no-btn.zap {{
      animation: zap 130ms linear;
    }}

    @keyframes zap {{
      0% {{ filter: brightness(1.05); }}
      30% {{ filter: brightness(1.35) saturate(1.2); }}
      60% {{ filter: brightness(0.95); }}
      100% {{ filter: brightness(1); }}
    }}

    .attempts {{
      position: absolute;
      right: clamp(8px, 2vw, 16px);
      bottom: clamp(8px, 2vw, 14px);
      border-radius: 999px;
      padding: 8px 12px;
      background: rgba(255, 255, 255, 0.09);
      border: 1px solid rgba(255, 255, 255, 0.2);
      font-size: clamp(0.78rem, 2.3vw, 0.9rem);
      color: #f9edc2;
      font-weight: 700;
      z-index: 1;
    }}

    .celebrate {{
      display: none;
      z-index: 2;
      border-radius: 18px;
      border: 1px solid rgba(255, 255, 255, 0.29);
      background: linear-gradient(145deg, rgba(223, 48, 66, 0.22), rgba(20, 84, 216, 0.24));
      text-align: center;
      padding: clamp(16px, 3.4vw, 26px);
      animation: popIn 450ms ease;
    }}

    .celebrate h2 {{
      margin: 0;
      color: #ffe8a8;
      font-size: clamp(1.35rem, 4.8vw, 2.4rem);
      line-height: 1.3;
    }}

    .sent-note {{
      text-align: center;
      font-size: clamp(0.92rem, 2.7vw, 1rem);
      color: #e9f2ff;
      font-weight: 700;
      margin-top: 8px;
    }}

    @keyframes popIn {{
      from {{ opacity: 0; transform: scale(0.95); }}
      to {{ opacity: 1; transform: scale(1); }}
    }}

    #confetti-layer, #heart-layer, #webburst-layer {{
      position: fixed;
      inset: 0;
      pointer-events: none;
      overflow: hidden;
      z-index: 1000;
    }}

    .confetti {{
      position: absolute;
      width: 10px;
      height: 16px;
      opacity: 0.95;
      animation: confettiFall linear forwards;
    }}

    @keyframes confettiFall {{
      from {{ transform: translate3d(0, -10vh, 0) rotate(0deg); }}
      to {{ transform: translate3d(var(--x-end), 110vh, 0) rotate(760deg); }}
    }}

    .heart {{
      position: absolute;
      font-size: clamp(18px, 3.5vw, 28px);
      animation: rise 3.8s ease-in forwards;
      filter: drop-shadow(0 3px 8px rgba(0, 0, 0, 0.34));
    }}

    @keyframes rise {{
      from {{ transform: translateY(0) scale(0.85); opacity: 0; }}
      14% {{ opacity: 1; }}
      to {{ transform: translateY(-92vh) translateX(var(--drift)) scale(1.28); opacity: 0; }}
    }}

    .webburst {{
      position: absolute;
      width: clamp(32px, 7vw, 58px);
      height: clamp(32px, 7vw, 58px);
      border-radius: 50%;
      border: 2px solid rgba(214, 236, 255, 0.85);
      opacity: 0;
      animation: webOut 860ms ease-out forwards;
    }}

    @keyframes webOut {{
      0% {{ transform: scale(0.35); opacity: 0.95; }}
      100% {{ transform: scale(2.3); opacity: 0; }}
    }}

    .answer-tag {{
      align-self: flex-start;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      background: rgba(255, 255, 255, 0.1);
      color: #ffe9aa;
      font-weight: 800;
      font-size: clamp(0.86rem, 2.6vw, 1rem);
      padding: 9px 13px;
      z-index: 2;
    }}

    .footer {{
      margin-top: auto;
      text-align: center;
      font-size: 0.9rem;
      color: rgba(255, 255, 255, 0.79);
      z-index: 2;
    }}

    @media (max-width: 760px) {{
      .card {{
        min-height: min(790px, calc(100dvh - 10px));
      }}
      .arena {{
        min-height: clamp(190px, 30vh, 300px);
      }}
      .no-btn {{
        left: 66%;
        top: 42%;
      }}
    }}

    @media (max-height: 690px) and (orientation: landscape) {{
      .stage {{
        align-items: flex-start;
      }}
      .card {{
        min-height: 620px;
      }}
      .arena {{
        min-height: 150px;
      }}
    }}
  </style>
</head>
<body>
  <div
    id="stage"
    class="stage"
    data-submitted="{submitted_attr}"
    data-answer="{submitted_answer}"
    data-email-sent="{'true' if email_sent else 'false'}"
    data-init-attempts="{no_escape_count}"
    data-init-scale="{yes_scale_clamped}"
  >
    <div class="cityline"></div>

    <svg class="web w1" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cfe7ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
    <svg class="web w2" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cfe7ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
    <svg class="web w3" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cfe7ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
    <svg class="web w4" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cfe7ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>

    <div class="sparkle" style="top:10%; left:18%; animation-delay:0.2s"></div>
    <div class="sparkle" style="top:16%; right:16%; animation-delay:1.2s"></div>
    <div class="sparkle" style="top:30%; left:7%; animation-delay:0.7s"></div>
    <div class="sparkle" style="top:34%; right:9%; animation-delay:1.8s"></div>
    <div class="sparkle" style="bottom:24%; left:14%; animation-delay:0.4s"></div>
    <div class="sparkle" style="bottom:18%; right:22%; animation-delay:1.5s"></div>

    <section class="card" role="main" aria-live="polite">
      <div class="spider-wrap" aria-hidden="true">
        <div class="thread"></div>
        <div class="spider">
          <div class="spider-body"></div>
          <span class="leg l1"></span><span class="leg l2"></span><span class="leg l3"></span><span class="leg l4"></span>
        </div>
      </div>

      <div class="chip"><span class="chip-dot"></span>Spider Invite Mission</div>

      <div class="bubble" id="bubble">
        <p class="invite-text" id="invite-text">{invite_text}</p>
      </div>

      <div class="status" id="status"></div>

      <div class="arena" id="arena">
        <button class="action-btn no-btn" id="no-btn" aria-label="No">No 🕸️</button>
        <div class="attempts" id="attempts">Escape attempts: {no_escape_count}</div>
      </div>

      <div class="celebrate" id="celebrate-panel">
        <h2>YAY!! ❤️ See you at the movie, {safe_visitor_name}! 🕷️🍿</h2>
        <div class="sent-note">{sent_note}</div>
      </div>

      <div class="answer-tag" id="answer-tag" style="display:none;">Selected answer: YES</div>
      <div class="footer">Made with original webs, skyline, sparkles and spider vibes.</div>
    </section>
  </div>

  <div id="confetti-layer"></div>
  <div id="heart-layer"></div>
  <div id="webburst-layer"></div>

  <script>
    const stage = document.getElementById("stage");
    const statusNode = document.getElementById("status");
    const noBtn = document.getElementById("no-btn");
    const arena = document.getElementById("arena");
    const bubble = document.getElementById("bubble");
    const celebratePanel = document.getElementById("celebrate-panel");
    const answerTag = document.getElementById("answer-tag");
    const attemptsNode = document.getElementById("attempts");

    const submitted = stage.dataset.submitted === "true";
    const initScale = Number(stage.dataset.initScale || "1") || 1;
    let yesScale = Math.max(1, Math.min(1.9, initScale));
    let escapeAttempts = Number(stage.dataset.initAttempts || "0") || 0;

    const playful = [
      "Nice try 😏",
      "Your Spider-Sense missed! 🕷️",
      "Nope, too slow 😂",
      "The No button escaped!",
      "Maybe press Yes instead? ❤️",
      "Not today, villain 🕸️",
      "The multiverse rejected that answer!"
    ];

    function rand(min, max) {{
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }}

    function setFrameHeight() {{
      const h = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight, 760);
      if (window.Streamlit && typeof window.Streamlit.setFrameHeight === "function") {{
        window.Streamlit.setFrameHeight(h);
      }} else {{
        window.parent.postMessage({{ isStreamlitMessage: true, type: "streamlit:setFrameHeight", height: h }}, "*");
      }}
    }}

    function sendValue(payload) {{
      if (window.Streamlit && typeof window.Streamlit.setComponentValue === "function") {{
        window.Streamlit.setComponentValue(payload);
      }} else {{
        window.parent.postMessage({{ isStreamlitMessage: true, type: "streamlit:setComponentValue", value: payload }}, "*");
      }}
    }}

    function updateAttemptsLabel() {{
      attemptsNode.textContent = `Escape attempts: ${{escapeAttempts}}`;
    }}

    function overlaps(rectA, rectB) {{
      return !(
        rectA.right <= rectB.left ||
        rectA.left >= rectB.right ||
        rectA.bottom <= rectB.top ||
        rectA.top >= rectB.bottom
      );
    }}

    function inflatedRect(rect, pixels) {{
      return {{
        left: rect.left - pixels,
        top: rect.top - pixels,
        right: rect.right + pixels,
        bottom: rect.bottom + pixels
      }};
    }}

    function chooseSafePosition() {{
      const arenaRect = arena.getBoundingClientRect();
      const noRect = noBtn.getBoundingClientRect();
      const noW = noRect.width;
      const noH = noRect.height;

      const pad = 8;
      const minX = pad;
      const minY = pad;
      const maxX = Math.max(minX, arenaRect.width - noW - pad);
      const maxY = Math.max(minY, arenaRect.height - noH - pad);

      const bubbleRect = inflatedRect(bubble.getBoundingClientRect(), 6);

      let candidate = {{ x: rand(minX, Math.floor(maxX)), y: rand(minY, Math.floor(maxY)) }};
      for (let i = 0; i < 90; i += 1) {{
        const x = rand(minX, Math.floor(maxX));
        const y = rand(minY, Math.floor(maxY));
        const projected = {{
          left: arenaRect.left + x,
          top: arenaRect.top + y,
          right: arenaRect.left + x + noW,
          bottom: arenaRect.top + y + noH
        }};

        const collides = overlaps(projected, bubbleRect);
        if (!collides) {{
          candidate = {{ x, y }};
          break;
        }}
      }}
      return candidate;
    }}

    function createConfetti() {{
      const colors = ["#ff4f67", "#ffd35c", "#45a4ff", "#ffffff", "#ff89aa"];
      const layer = document.getElementById("confetti-layer");
      for (let i = 0; i < 130; i += 1) {{
        const c = document.createElement("div");
        c.className = "confetti";
        c.style.left = rand(0, 100) + "vw";
        c.style.top = rand(-16, 6) + "vh";
        c.style.background = colors[rand(0, colors.length - 1)];
        c.style.animationDuration = (2.3 + Math.random() * 2.2) + "s";
        c.style.setProperty("--x-end", rand(-24, 24) + "vw");
        layer.appendChild(c);
        setTimeout(() => c.remove(), 5000);
      }}
    }}

    function createHearts() {{
      const layer = document.getElementById("heart-layer");
      for (let i = 0; i < 34; i += 1) {{
        const h = document.createElement("div");
        h.className = "heart";
        h.textContent = Math.random() > 0.5 ? "❤️" : "💙";
        h.style.left = rand(4, 96) + "vw";
        h.style.bottom = rand(-8, 10) + "vh";
        h.style.animationDelay = (Math.random() * 1.2) + "s";
        h.style.setProperty("--drift", rand(-10, 10) + "vw");
        layer.appendChild(h);
        setTimeout(() => h.remove(), 5200);
      }}
    }}

    function createWebBursts() {{
      const layer = document.getElementById("webburst-layer");
      for (let i = 0; i < 16; i += 1) {{
        const w = document.createElement("div");
        w.className = "webburst";
        w.style.left = rand(5, 95) + "vw";
        w.style.top = rand(8, 88) + "vh";
        w.style.animationDelay = (Math.random() * 0.8) + "s";
        layer.appendChild(w);
        setTimeout(() => w.remove(), 1400);
      }}
    }}

    function celebrate() {{
      celebratePanel.style.display = "block";
      answerTag.style.display = "inline-flex";
      createConfetti();
      createHearts();
      createWebBursts();
      setFrameHeight();
    }}

    function hideButtonsAfterYes() {{
      noBtn.style.display = "none";
      attemptsNode.style.display = "none";
      statusNode.textContent = "";
    }}

    function growYesSlightly() {{
      yesScale = Math.min(1.9, yesScale + 0.05);
    }}

    function teleportNo() {{
      if (submitted) return;

      const spot = chooseSafePosition();
      const rotate = rand(-15, 15);
      noBtn.style.left = `${{spot.x}}px`;
      noBtn.style.top = `${{spot.y}}px`;
      noBtn.style.transform = `rotate(${{rotate}}deg)`;
      noBtn.classList.remove("zap");
      void noBtn.offsetWidth;
      noBtn.classList.add("zap");

      escapeAttempts += 1;
      updateAttemptsLabel();
      growYesSlightly();
      statusNode.textContent = playful[rand(0, playful.length - 1)];
    }}

    function maybeEscapeFromPointer(event) {{
      if (submitted) return;
      const ex = event.clientX;
      const ey = event.clientY;
      if (typeof ex !== "number" || typeof ey !== "number") return;

      const rect = noBtn.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = ex - cx;
      const dy = ey - cy;
      const distance = Math.sqrt(dx * dx + dy * dy);
      const triggerRadius = Math.max(95, rect.width * 0.9);
      if (distance < triggerRadius) {{
        teleportNo();
      }}
    }}

    function sendProgress() {{
      if (submitted) return;
      sendValue({{
        type: "progress",
        attempts: escapeAttempts,
        yes_scale: yesScale,
        nonce: Date.now()
      }});
    }}

    function resetNoWithinBounds() {{
      const spot = chooseSafePosition();
      noBtn.style.left = `${{spot.x}}px`;
      noBtn.style.top = `${{spot.y}}px`;
      noBtn.style.transform = `rotate(${{rand(-10, 10)}}deg)`;
    }}

    function bindNoEscapes() {{
      const fastEvents = ["mouseenter", "mousedown", "pointerdown", "touchstart", "click"];
      fastEvents.forEach((name) => {{
        noBtn.addEventListener(name, (event) => {{
          event.preventDefault();
          teleportNo();
        }}, {{ passive: false }});
      }});

      arena.addEventListener("pointermove", maybeEscapeFromPointer, {{ passive: true }});
      arena.addEventListener("mousemove", maybeEscapeFromPointer, {{ passive: true }});

      arena.addEventListener("touchmove", (event) => {{
        if (!event.touches || !event.touches.length) return;
        const touch = event.touches[0];
        maybeEscapeFromPointer({{ clientX: touch.clientX, clientY: touch.clientY }});
      }}, {{ passive: true }});

      noBtn.addEventListener("keydown", (event) => {{
        if (event.key === "Enter" || event.key === " ") {{
          event.preventDefault();
          teleportNo();
        }}
      }});
    }}

    function initialize() {{
      document.documentElement.style.setProperty("--yes-scale", String(yesScale));
      updateAttemptsLabel();
      setFrameHeight();

      window.addEventListener("resize", () => {{
        resetNoWithinBounds();
        setFrameHeight();
      }});
      window.addEventListener("orientationchange", () => {{
        setTimeout(() => {{
          resetNoWithinBounds();
          setFrameHeight();
        }}, 120);
      }});

      if (submitted) {{
        hideButtonsAfterYes();
        celebrate();
        return;
      }}

      bindNoEscapes();

      resetNoWithinBounds();
      setInterval(sendProgress, 2200);
    }}

    initialize();
  </script>
</body>
</html>
"""


def main() -> None:
  init_session_state()
  inject_base_page_css()

  if "name_submitted" not in st.session_state:
    st.session_state.name_submitted = False

  if "visitor_name" not in st.session_state:
    st.session_state.visitor_name = ""

  if not st.session_state.name_submitted:
    render_name_entry_card()
    return

  safe_name = html.escape(str(st.session_state.visitor_name), quote=True)
  component_value = components.html(
    build_invitation_html(
      safe_visitor_name=safe_name,
      response_submitted=bool(st.session_state.response_submitted),
      submitted_answer=str(st.session_state.submitted_answer),
      email_sent=bool(st.session_state.email_sent),
      no_escape_count=int(st.session_state.no_escape_count),
      yes_scale=float(st.session_state.yes_scale),
    ),
    height=960,
    scrolling=False,
  )

  yes_clicked = False
  if not st.session_state.response_submitted:
    st.markdown('<div class="main-yes-anchor">', unsafe_allow_html=True)
    yes_clicked = st.button(
      "Yes ❤️",
      key="main_yes_button",
      use_container_width=True,
      type="primary",
    )
    st.markdown('</div>', unsafe_allow_html=True)

  if yes_clicked and not st.session_state.response_submitted:
    webhook_success = False

    if not st.session_state.yes_notification_sent:
      webhook_success = notify_backend(
        st.session_state.visitor_name,
        "YES",
      )

      if webhook_success:
        st.session_state.yes_notification_sent = True
    else:
      webhook_success = True

    st.session_state.webhook_success = webhook_success

    logged, save_error = log_yes_response_json(st.session_state.visitor_name)
    st.session_state.json_logged = logged
    st.session_state.last_save_error = save_error

    if not st.session_state.email_sent:
      st.session_state.email_sent = send_yes_email(st.session_state.visitor_name)

    st.session_state.response_submitted = True
    st.session_state.submitted_answer = "YES"
    st.rerun()

  if st.session_state.response_submitted:
    if not st.session_state.yes_notification_sent:
      st.warning("Webhook notification failed. You can retry.")
      if st.button("Retry notification", use_container_width=True):
        retry_notification()
        st.rerun()

    if st.session_state.json_logged:
      st.success(f"Saved to {RESPONSE_LOG_FILE}")
    else:
      st.error(
        "Could not save to JSON file. "
        f"Details: {st.session_state.last_save_error or 'Unknown error'}"
      )

  process_component_event(component_value)


if __name__ == "__main__":
    main()
