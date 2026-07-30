from __future__ import annotations

import logging
import smtplib
from datetime import datetime
from email.message import EmailMessage
from zoneinfo import ZoneInfo

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Spider Invite", page_icon="🕷️", layout="wide")

LOGGER = logging.getLogger("spider_invite")
MELBOURNE_TZ = ZoneInfo("Australia/Melbourne")
INVITE_TEXT = "Will you come with me to watch the Spider-Man movie on 31/07 evening? 🕷️❤️"


def init_session_state() -> None:
    """Initialize session flags used to prevent duplicate submissions and emails."""
    if "response_submitted" not in st.session_state:
        st.session_state.response_submitted = False
    if "submitted_answer" not in st.session_state:
        st.session_state.submitted_answer = None
    if "email_sent" not in st.session_state:
        st.session_state.email_sent = False


def get_answer_from_query() -> str | None:
    """Read and normalize answer query param coming from the front-end buttons."""
    raw_value = st.query_params.get("answer")
    if raw_value is None:
        return None

    if isinstance(raw_value, list):
        answer = raw_value[0].strip().lower() if raw_value else ""
    else:
        answer = str(raw_value).strip().lower()

    # Only "yes" can be submitted. "No" is intentionally impossible in UI.
    if answer == "yes":
        return answer
    return None


def send_response_email(answer: str) -> bool:
    """Send response notification email through Gmail SMTP SSL using Streamlit secrets."""
    required_keys = ("EMAIL_SENDER", "EMAIL_RECIPIENT", "EMAIL_APP_PASSWORD")
    missing_keys = [key for key in required_keys if key not in st.secrets]
    if missing_keys:
        LOGGER.warning("Missing Streamlit email secret keys: %s", ", ".join(missing_keys))
        return False

    sender = st.secrets["EMAIL_SENDER"]
    recipient = st.secrets["EMAIL_RECIPIENT"]
    app_password = st.secrets["EMAIL_APP_PASSWORD"]

    response_time = datetime.now(MELBOURNE_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")

    if answer != "yes":
      return False

    subject = "Spider-Man invitation response: YES ❤️"
    body_intro = "Someone clicked YES on your Spider-Man movie invitation! ❤️🕷️"

    body = (
        f"{body_intro}\n\n"
        f"Response: {answer.upper()}\n"
        f"Response time (Australia/Melbourne): {response_time}\n"
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
        # Safe log only: no secret values are included.
        LOGGER.warning("Email send failed for invitation response. Error type: %s", type(exc).__name__)
        return False


def process_submission_if_needed() -> None:
    """Handle first valid response per session and send at most one email."""
    answer = get_answer_from_query()
    if not answer:
        return

    # Avoid duplicate processing after reruns in the same browser session.
    if st.session_state.response_submitted:
        st.query_params.clear()
        return

    st.session_state.response_submitted = True
    st.session_state.submitted_answer = answer
    st.session_state.email_sent = send_response_email(answer)
    st.query_params.clear()


def build_app_html(*, response_submitted: bool, submitted_answer: str | None) -> str:
    """Render responsive comic-themed UI and animated interactions."""
    is_yes = response_submitted and submitted_answer == "yes"
    is_no = response_submitted and submitted_answer == "no"

    selected_label = "Yes ❤️" if is_yes else ("No 🕸️" if is_no else "")

    # The dynamic state is embedded in HTML attributes for client-side animation control.
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Spider Invite</title>
  <style>
    :root {{
      --red: #dc2f3f;
      --blue: #1454d8;
      --ink: #0c111b;
      --black: #06090f;
      --white: #fffaf2;
      --cream: #fff2d9;
      --glow: #ffd35c;
      --panel: rgba(13, 18, 29, 0.9);
    }}

    * {{ box-sizing: border-box; }}

    html, body {{
      margin: 0;
      width: 100%;
      height: 100%;
      overflow-x: hidden;
      font-family: "Trebuchet MS", "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 20% 12%, #223464 0%, #111827 35%, #090d15 70%, #070a11 100%);
      color: var(--white);
    }}

    .stage {{
      min-height: 100dvh;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 14px;
      position: relative;
      overflow: hidden;
      isolation: isolate;
    }}

    .comic-dots {{
      position: absolute;
      inset: 0;
      opacity: 0.25;
      background-image: radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px);
      background-size: 15px 15px;
      z-index: -5;
    }}

    .cityline {{
      position: absolute;
      inset: auto 0 0 0;
      height: 22dvh;
      min-height: 110px;
      background: linear-gradient(180deg, rgba(5, 7, 11, 0) 0%, rgba(4, 6, 9, 0.84) 45%, rgba(3, 4, 7, 1) 100%);
      z-index: -4;
    }}

    .cityline::before {{
      content: "";
      position: absolute;
      inset: auto 0 0 0;
      height: 100%;
      background:
        linear-gradient(to right,
          transparent 0 3%, #090f1a 3% 7%, transparent 7% 9%, #0b1526 9% 14%, transparent 14% 17%,
          #081220 17% 21%, transparent 21% 23%, #0b1628 23% 29%, transparent 29% 32%, #091322 32% 37%,
          transparent 37% 39%, #0c1729 39% 44%, transparent 44% 47%, #091323 47% 53%, transparent 53% 56%,
          #0b1528 56% 62%, transparent 62% 65%, #08111f 65% 70%, transparent 70% 72%, #0b1628 72% 77%,
          transparent 77% 80%, #091321 80% 86%, transparent 86% 88%, #0b1527 88% 93%, transparent 93% 100%);
      opacity: 0.9;
    }}

    .web {{
      position: absolute;
      width: clamp(70px, 15vw, 130px);
      opacity: 0.38;
      animation: drift 10s ease-in-out infinite;
      pointer-events: none;
      z-index: -3;
    }}

    .web.w1 {{ top: 2.5%; left: 2.2%; animation-delay: 0.2s; }}
    .web.w2 {{ top: 8%; right: 4%; animation-delay: 1.2s; }}
    .web.w3 {{ bottom: 20%; left: 6%; animation-delay: 2.1s; }}
    .web.w4 {{ bottom: 24%; right: 7%; animation-delay: 2.9s; }}

    @keyframes drift {{
      0%, 100% {{ transform: translateY(0) rotate(0deg); }}
      50% {{ transform: translateY(-13px) rotate(4deg); }}
    }}

    .sparkle {{
      position: absolute;
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #ffe48d;
      box-shadow: 0 0 12px #ffe48d;
      animation: twinkle 2.4s ease-in-out infinite;
      pointer-events: none;
      z-index: -2;
    }}

    @keyframes twinkle {{
      0%, 100% {{ transform: scale(0.72); opacity: 0.35; }}
      50% {{ transform: scale(1.35); opacity: 1; }}
    }}

    .card {{
      width: min(900px, 100%);
      min-height: min(720px, calc(100dvh - 28px));
      border-radius: 26px;
      position: relative;
      overflow: hidden;
      padding: clamp(16px, 4.2vw, 38px);
      background: linear-gradient(140deg, rgba(17, 28, 51, 0.95), rgba(22, 15, 35, 0.91));
      border: 2px solid rgba(255, 255, 255, 0.12);
      box-shadow: 0 24px 66px rgba(0, 0, 0, 0.42);
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 14px;
      animation: enter 800ms cubic-bezier(.2, 1, .2, 1);
    }}

    .card::before {{
      content: "";
      position: absolute;
      inset: -140% -30% auto -30%;
      height: 290%;
      transform: rotate(11deg);
      background: linear-gradient(120deg, rgba(220, 47, 63, 0.2), rgba(20, 84, 216, 0.24), rgba(255, 211, 92, 0.15));
      pointer-events: none;
    }}

    @keyframes enter {{
      from {{ opacity: 0; transform: translateY(26px) scale(0.98); }}
      to {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    .spider-wrap {{
      position: absolute;
      top: -10px;
      left: 50%;
      transform: translateX(-50%);
      width: 74px;
      height: 170px;
      transform-origin: top center;
      pointer-events: none;
      animation: swing 3.1s ease-in-out infinite;
      z-index: 2;
    }}

    .thread {{
      width: 2px;
      height: 108px;
      margin: 0 auto;
      background: linear-gradient(180deg, rgba(240, 246, 255, 0.8), rgba(255, 255, 255, 0.12));
    }}

    .spider {{
      width: 31px;
      height: 41px;
      margin: -2px auto 0;
      position: relative;
    }}

    .spider-body {{
      width: 24px;
      height: 26px;
      margin: 0 auto;
      border-radius: 46% 46% 56% 56%;
      border: 1px solid #2f3441;
      background: #0d1118;
      position: relative;
    }}

    .spider-body::before {{
      content: "";
      width: 11px;
      height: 8px;
      border-radius: 50%;
      border: 1px solid #2f3441;
      background: #161c27;
      position: absolute;
      top: -6px;
      left: 6px;
    }}

    .leg {{
      position: absolute;
      width: 14px;
      height: 2px;
      background: #2a3041;
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
      gap: 10px;
      border-radius: 999px;
      font-size: clamp(0.75rem, 2.6vw, 0.92rem);
      padding: 9px 13px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      font-weight: 800;
      color: #ffe694;
      border: 1px solid rgba(255, 230, 148, 0.3);
      background: rgba(255, 218, 111, 0.13);
      position: relative;
      z-index: 2;
    }}

    .chip-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #ffe694;
      box-shadow: 0 0 10px #ffe694;
    }}

    .bubble {{
      position: relative;
      z-index: 2;
      background: var(--white);
      color: #141824;
      border: 3px solid #111726;
      border-radius: 22px;
      box-shadow: 7px 7px 0 #101624;
      padding: clamp(16px, 4vw, 28px);
      min-height: clamp(115px, 22vw, 160px);
      display: flex;
      align-items: center;
    }}

    .bubble::after {{
      content: "";
      position: absolute;
      left: 36px;
      bottom: -18px;
      width: 22px;
      height: 22px;
      background: var(--white);
      border-left: 3px solid #111726;
      border-bottom: 3px solid #111726;
      transform: rotate(-45deg);
    }}

    .invite-text {{
      margin: 0;
      width: 100%;
      font-size: clamp(1.02rem, 3.9vw, 2rem);
      line-height: 1.35;
      font-weight: 800;
      text-wrap: pretty;
      word-break: normal;
      overflow-wrap: break-word;
    }}

    .status {{
      min-height: 30px;
      z-index: 2;
      color: #ffe8a9;
      font-weight: 800;
      font-size: clamp(0.95rem, 2.9vw, 1.08rem);
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.28);
    }}

    .button-zone {{
      position: relative;
      z-index: 2;
      border-radius: 16px;
      border: 1px dashed rgba(255, 255, 255, 0.24);
      background: rgba(9, 13, 22, 0.3);
      min-height: clamp(150px, 25vh, 220px);
      overflow: hidden;
      padding: 12px;
    }}

    .action-btn {{
      position: absolute;
      border: 0;
      border-radius: 14px;
      font-size: clamp(1rem, 3.8vw, 1.18rem);
      font-weight: 800;
      padding: 14px 22px;
      min-height: 52px;
      min-width: 130px;
      cursor: pointer;
      transition: transform 180ms ease, filter 180ms ease, box-shadow 180ms ease;
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
      user-select: none;
    }}

    .action-btn:active {{ transform: translateY(1px) scale(0.98); }}

    .yes-btn {{
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: #fff;
      border: 1px solid rgba(255, 255, 255, 0.25);
      background: linear-gradient(130deg, #f24f5e, #dc2f3f);
      box-shadow: 0 11px 22px rgba(220, 47, 63, 0.38);
    }}

    .yes-btn:hover {{
      transform: translateY(-52%) scale(1.03);
      filter: brightness(1.04);
    }}

    .no-btn {{
      right: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: #fff;
      border: 1px solid rgba(255, 255, 255, 0.25);
      background: linear-gradient(130deg, #3272ff, #1454d8);
      box-shadow: 0 11px 22px rgba(20, 84, 216, 0.38);
    }}

    .no-btn.runaway {{ animation: jumpy 240ms ease; }}

    @keyframes jumpy {{
      0% {{ transform: scale(1) rotate(0deg); }}
      30% {{ transform: scale(1.04) rotate(-4deg); }}
      60% {{ transform: scale(0.97) rotate(3deg); }}
      100% {{ transform: scale(1) rotate(0deg); }}
    }}

    .answer-tag {{
      z-index: 2;
      align-self: flex-start;
      padding: 9px 14px;
      border-radius: 999px;
      font-size: clamp(0.88rem, 2.8vw, 1.02rem);
      font-weight: 800;
      border: 1px solid rgba(255, 255, 255, 0.3);
      background: rgba(255, 255, 255, 0.08);
      color: #fbe9af;
    }}

    .sent-note {{
      z-index: 2;
      font-size: clamp(0.9rem, 2.6vw, 1rem);
      color: #d9ebff;
      opacity: 0.94;
      font-weight: 700;
    }}

    .celebrate {{
      display: none;
      z-index: 2;
      border-radius: 18px;
      border: 1px solid rgba(255, 255, 255, 0.25);
      background: linear-gradient(145deg, rgba(220, 47, 63, 0.2), rgba(20, 84, 216, 0.22));
      text-align: center;
      padding: clamp(18px, 3.5vw, 26px);
      animation: pop 450ms ease;
    }}

    .celebrate h2 {{
      margin: 0;
      font-size: clamp(1.45rem, 5vw, 2.5rem);
      color: #ffe8a0;
      line-height: 1.3;
      text-wrap: balance;
    }}

    @keyframes pop {{
      from {{ opacity: 0; transform: scale(0.94); }}
      to {{ opacity: 1; transform: scale(1); }}
    }}

    #confetti-layer, #heart-layer {{
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
      animation: confettiFall linear forwards;
      opacity: 0.95;
    }}

    @keyframes confettiFall {{
      from {{ transform: translate3d(0, -12vh, 0) rotate(0deg); opacity: 1; }}
      to {{ transform: translate3d(var(--x-end), 110vh, 0) rotate(760deg); opacity: 0.95; }}
    }}

    .heart {{
      position: absolute;
      font-size: 24px;
      filter: drop-shadow(0 3px 8px rgba(0, 0, 0, 0.35));
      animation: rise 3.8s ease-in forwards;
    }}

    @keyframes rise {{
      from {{ transform: translateY(0) scale(0.9); opacity: 0; }}
      14% {{ opacity: 1; }}
      to {{ transform: translateY(-90vh) translateX(var(--drift)) scale(1.35); opacity: 0; }}
    }}

    .footer {{
      z-index: 2;
      margin-top: auto;
      text-align: center;
      font-size: 0.9rem;
      color: rgba(255, 255, 255, 0.8);
    }}

    @media (max-width: 900px) {{
      .card {{
        min-height: min(740px, calc(100dvh - 20px));
      }}
    }}

    @media (max-width: 680px) {{
      .stage {{ padding: 8px; }}

      .card {{
        border-radius: 20px;
        min-height: min(760px, calc(100dvh - 14px));
        padding: 14px;
      }}

      .bubble {{ box-shadow: 5px 5px 0 #101624; }}

      .button-zone {{ min-height: 220px; }}

      .yes-btn {{ left: 10px; }}
      .no-btn {{ right: 10px; }}
    }}

    @media (max-height: 680px) and (orientation: landscape) {{
      .stage {{
        align-items: flex-start;
        padding-top: 8px;
        padding-bottom: 8px;
      }}

      .card {{ min-height: 600px; }}
      .button-zone {{ min-height: 145px; }}
    }}
  </style>
</head>
<body>
  <div class="stage" data-submitted="{str(response_submitted).lower()}" data-answer="{submitted_answer or ''}">
    <div class="comic-dots"></div>
    <div class="cityline"></div>

    <svg class="web w1" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cfe7ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
    <svg class="web w2" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cfe7ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
    <svg class="web w3" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cfe7ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
    <svg class="web w4" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cfe7ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>

    <div class="sparkle" style="top:9%; left:20%; animation-delay:0.2s"></div>
    <div class="sparkle" style="top:16%; right:16%; animation-delay:1.2s"></div>
    <div class="sparkle" style="top:29%; left:7%; animation-delay:0.6s"></div>
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

      <div class="bubble">
        <p class="invite-text">{INVITE_TEXT}</p>
      </div>

      <div id="status" class="status"></div>

      <div class="button-zone" id="button-zone">
        <button class="action-btn yes-btn" id="yes-btn" {'disabled' if response_submitted else ''}>Yes ❤️</button>
        <button class="action-btn no-btn" id="no-btn" {'disabled' if response_submitted else ''}>No 🕸️</button>
      </div>

      <div class="answer-tag" {'style="display:none;"' if not response_submitted else ''}>Selected response: {selected_label}</div>
      <div class="sent-note" {'style="display:none;"' if not response_submitted else ''}>Your answer has been sent 🕷️</div>

      <div class="celebrate" id="celebrate-panel">
        <h2>YAY!! ❤️ See you at the movie! 🕷️🍿</h2>
      </div>

      <div class="footer">Made with ❤️</div>
    </section>
  </div>

  <div id="confetti-layer"></div>
  <div id="heart-layer"></div>

  <script>
    const stage = document.querySelector(".stage");
    const statusNode = document.getElementById("status");
    const yesBtn = document.getElementById("yes-btn");
    const noBtn = document.getElementById("no-btn");
    const zone = document.getElementById("button-zone");
    const celebratePanel = document.getElementById("celebrate-panel");

    const submitted = stage.dataset.submitted === "true";
    const answer = (stage.dataset.answer || "").toLowerCase();

    const playful = [
      "Nice try 😏",
      "Spider-Sense says no isn't an option!",
      "You missed! 🕷️",
      "Try again 😂"
    ];

    function rand(min, max) {{
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }}

    function createConfetti() {{
      const colors = ["#ff4f67", "#ffd35c", "#45a4ff", "#ffffff", "#ff89aa"];
      const layer = document.getElementById("confetti-layer");
      for (let i = 0; i < 130; i += 1) {{
        const c = document.createElement("div");
        c.className = "confetti";
        c.style.left = rand(0, 100) + "vw";
        c.style.top = rand(-14, 5) + "vh";
        c.style.background = colors[rand(0, colors.length - 1)];
        c.style.animationDuration = (2.3 + Math.random() * 2.1) + "s";
        c.style.setProperty("--x-end", rand(-24, 24) + "vw");
        layer.appendChild(c);
        setTimeout(() => c.remove(), 4600);
      }}
    }}

    function createHearts() {{
      const layer = document.getElementById("heart-layer");
      for (let i = 0; i < 36; i += 1) {{
        const h = document.createElement("div");
        h.className = "heart";
        h.textContent = Math.random() > 0.5 ? "❤️" : "💙";
        h.style.left = rand(4, 96) + "vw";
        h.style.bottom = rand(-10, 8) + "vh";
        h.style.animationDelay = (Math.random() * 1.25) + "s";
        h.style.setProperty("--drift", rand(-9, 9) + "vw");
        layer.appendChild(h);
        setTimeout(() => h.remove(), 5100);
      }}
    }}

    function moveNoButton() {{
      if (!noBtn || noBtn.disabled) return;

      const zoneRect = zone.getBoundingClientRect();
      const btnRect = noBtn.getBoundingClientRect();
      const maxX = Math.max(8, zoneRect.width - btnRect.width - 8);
      const maxY = Math.max(8, zoneRect.height - btnRect.height - 8);
      const x = rand(8, Math.floor(maxX));
      const y = rand(8, Math.floor(maxY));

      noBtn.style.left = x + "px";
      noBtn.style.top = y + "px";
      noBtn.style.right = "auto";
      noBtn.style.transform = "none";

      noBtn.classList.remove("runaway");
      void noBtn.offsetWidth;
      noBtn.classList.add("runaway");
      statusNode.textContent = playful[rand(0, playful.length - 1)];
    }}

    function submitAnswer(answerValue) {{
      const url = new URL(window.location.href);
      url.searchParams.set("answer", answerValue);
      window.location.href = url.toString();
    }}

    if (!submitted) {{
      yesBtn?.addEventListener("click", (event) => {{
        event.preventDefault();
        yesBtn.disabled = true;
        noBtn.disabled = true;
        statusNode.textContent = "Heroic choice unlocked!";
        celebratePanel.style.display = "block";
        createConfetti();
        createHearts();
        setTimeout(() => submitAnswer("yes"), 850);
      }});

      ["mouseenter", "touchstart", "pointerdown", "click"].forEach((evtName) => {{
        noBtn?.addEventListener(evtName, (event) => {{
          event.preventDefault();
          moveNoButton();
        }}, {{ passive: false }});
      }});

      // Extra guard: keyboard activation also never submits "No".
      noBtn?.addEventListener("keydown", (event) => {{
        if (event.key === "Enter" || event.key === " ") {{
          event.preventDefault();
          moveNoButton();
        }}
      }});
    }} else {{
      yesBtn.disabled = true;
      noBtn.disabled = true;
      yesBtn.style.opacity = "0.65";
      noBtn.style.opacity = "0.45";

      if (answer === "yes") {{
        celebratePanel.style.display = "block";
        createConfetti();
        createHearts();
      }} else if (answer === "no") {{
        statusNode.textContent = "Response received.";
      }}
    }}
  </script>
</body>
</html>
"""


def main() -> None:
    init_session_state()
    process_submission_if_needed()

    st.markdown(
        """
        <style>
          .stAppHeader, [data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer {
            visibility: hidden;
            height: 0;
            position: fixed;
          }
          .block-container {
            max-width: 100% !important;
            padding: 0 !important;
          }
          iframe {
            border: 0 !important;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    app_html = build_app_html(
        response_submitted=st.session_state.response_submitted,
        submitted_answer=st.session_state.submitted_answer,
    )
    components.html(app_html, height=980, scrolling=False)

    # Keep recipient feedback friendly and private.
    if st.session_state.response_submitted and not st.session_state.email_sent:
        st.info("Your answer was recorded. Notification is being retried safely on the next fresh response session.")


if __name__ == "__main__":
    main()
