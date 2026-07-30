import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hero Movie Invite", page_icon="🕷️", layout="wide")

html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Superhero Invite</title>
  <style>
    :root {
      --hero-red: #d7263d;
      --hero-blue: #0f4cdb;
      --hero-black: #0d1117;
      --hero-ink: #12131a;
      --hero-cream: #fff7e6;
      --hero-yellow: #ffd447;
      --bubble: #fffdf8;
    }

    * {
      box-sizing: border-box;
    }

    html,
    body {
      width: 100%;
      height: 100%;
      margin: 0;
      padding: 0;
      overflow-x: hidden;
      font-family: "Nunito", "Segoe UI", sans-serif;
      color: var(--hero-cream);
      background: radial-gradient(circle at 15% 20%, #1c2440 0%, #101521 35%, #090d14 70%, #05070b 100%);
    }

    .stage {
      position: relative;
      min-height: 100vh;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 18px;
      overflow: hidden;
      isolation: isolate;
    }

    .comic-dots {
      position: absolute;
      inset: 0;
      background-image: radial-gradient(rgba(255, 255, 255, 0.085) 1px, transparent 1px);
      background-size: 16px 16px;
      opacity: 0.28;
      z-index: -3;
    }

    .cityline {
      position: absolute;
      inset: auto 0 0 0;
      height: 150px;
      background: linear-gradient(180deg, rgba(12, 14, 23, 0) 0%, rgba(10, 13, 20, 0.9) 38%, rgba(6, 8, 12, 1) 100%);
      z-index: -2;
    }

    .cityline::before,
    .cityline::after {
      content: "";
      position: absolute;
      inset: auto 0 0 0;
      height: 100%;
      background-repeat: repeat-x;
      background-position: bottom;
      opacity: 0.8;
    }

    .cityline::before {
      background-image:
        linear-gradient(to right,
          transparent 0 2%, #0a0f17 2% 6%, transparent 6% 7%, #08111f 7% 12%, transparent 12% 14%,
          #070d16 14% 19%, transparent 19% 20%, #0b1423 20% 23%, transparent 23% 24%, #08101d 24% 30%,
          transparent 30% 31%, #091321 31% 36%, transparent 36% 38%, #08111f 38% 45%, transparent 45% 47%,
          #0a1524 47% 51%, transparent 51% 52%, #091120 52% 58%, transparent 58% 60%, #091321 60% 66%,
          transparent 66% 67%, #08101c 67% 72%, transparent 72% 73%, #0b1423 73% 78%, transparent 78% 79%,
          #080f1b 79% 86%, transparent 86% 88%, #091221 88% 94%, transparent 94% 95%, #0b1524 95% 100%);
    }

    .cityline::after {
      opacity: 0.5;
      transform: translateY(8px);
      filter: blur(1px);
      background-image:
        linear-gradient(to right,
          transparent 0 4%, #050a10 4% 9%, transparent 9% 11%, #060b12 11% 17%, transparent 17% 19%,
          #05090f 19% 24%, transparent 24% 26%, #05080e 26% 33%, transparent 33% 35%, #05090f 35% 40%,
          transparent 40% 42%, #060b13 42% 49%, transparent 49% 51%, #050a10 51% 58%, transparent 58% 60%,
          #05080e 60% 68%, transparent 68% 70%, #050a10 70% 76%, transparent 76% 78%, #05090f 78% 84%,
          transparent 84% 86%, #050a10 86% 92%, transparent 92% 94%, #060b13 94% 100%);
    }

    .float-web,
    .sparkle {
      position: absolute;
      pointer-events: none;
    }

    .float-web {
      width: 110px;
      opacity: 0.35;
      animation: driftWeb 11s ease-in-out infinite;
      z-index: -1;
    }

    .w1 { top: 6%; left: 4%; animation-delay: 0.2s; }
    .w2 { top: 15%; right: 6%; animation-delay: 1.1s; transform: scale(0.9); }
    .w3 { bottom: 22%; left: 9%; animation-delay: 2.4s; transform: scale(0.8); }
    .w4 { bottom: 32%; right: 11%; animation-delay: 3.1s; transform: scale(1.05); }

    @keyframes driftWeb {
      0%, 100% { transform: translateY(0) rotate(0deg); }
      50% { transform: translateY(-14px) rotate(3deg); }
    }

    .sparkle {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #ffe799;
      box-shadow: 0 0 14px rgba(255, 238, 158, 0.9);
      animation: twinkle 2.8s ease-in-out infinite;
      z-index: 0;
    }

    @keyframes twinkle {
      0%, 100% { transform: scale(0.7); opacity: 0.25; }
      50% { transform: scale(1.35); opacity: 1; }
    }

    .spider-wrap {
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%);
      width: 70px;
      height: 180px;
      pointer-events: none;
      animation: swing 3.2s ease-in-out infinite;
      transform-origin: top center;
      z-index: 3;
    }

    .thread {
      width: 1.5px;
      height: 120px;
      background: linear-gradient(180deg, rgba(210, 220, 240, 0.7), rgba(255, 255, 255, 0.12));
      margin: 0 auto;
    }

    .spider {
      width: 30px;
      height: 38px;
      margin: -2px auto 0;
      position: relative;
    }

    .spider-body {
      width: 22px;
      height: 25px;
      background: #0a0c12;
      border: 1px solid #29303d;
      border-radius: 45% 45% 55% 55%;
      margin: 0 auto;
      position: relative;
    }

    .spider-body::before {
      content: "";
      position: absolute;
      width: 10px;
      height: 8px;
      border-radius: 50%;
      background: #151a24;
      top: -6px;
      left: 5px;
      border: 1px solid #2d3443;
    }

    .leg {
      position: absolute;
      width: 14px;
      height: 2px;
      background: #202636;
      top: 9px;
      transform-origin: 0% 50%;
    }

    .l1 { left: -7px; transform: rotate(35deg); }
    .l2 { left: -8px; top: 14px; transform: rotate(8deg); }
    .l3 { right: -7px; transform: scaleX(-1) rotate(35deg); }
    .l4 { right: -8px; top: 14px; transform: scaleX(-1) rotate(8deg); }

    @keyframes swing {
      0%, 100% { transform: translateX(-50%) rotate(-3deg); }
      50% { transform: translateX(-50%) rotate(4deg); }
    }

    .card {
      width: min(920px, 100%);
      border-radius: 28px;
      padding: clamp(20px, 4vw, 42px);
      background: linear-gradient(140deg, rgba(17, 27, 53, 0.94), rgba(28, 20, 40, 0.87));
      border: 2px solid rgba(255, 255, 255, 0.09);
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.45);
      position: relative;
      overflow: hidden;
      animation: cardIn 900ms cubic-bezier(.19, 1, .22, 1);
      backdrop-filter: blur(3px);
      z-index: 2;
    }

    .card::before {
      content: "";
      position: absolute;
      inset: -120% -20% auto -20%;
      height: 280%;
      background: linear-gradient(120deg, rgba(215, 38, 61, 0.23), rgba(15, 76, 219, 0.25), rgba(255, 212, 71, 0.15));
      transform: rotate(10deg);
      pointer-events: none;
    }

    @keyframes cardIn {
      from { opacity: 0; transform: translateY(36px) scale(0.97); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    .title-chip {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 10px 16px;
      border-radius: 999px;
      background: rgba(255, 212, 71, 0.14);
      border: 1px solid rgba(255, 212, 71, 0.28);
      color: #ffe48f;
      font-weight: 800;
      letter-spacing: 0.02em;
      text-transform: uppercase;
      font-size: 0.86rem;
      margin-bottom: 16px;
      position: relative;
      z-index: 1;
    }

    .chip-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #ffe48f;
      box-shadow: 0 0 14px #ffe48f;
      animation: twinkle 1.8s ease-in-out infinite;
    }

    .speech-wrap {
      position: relative;
      z-index: 2;
      margin-bottom: 18px;
    }

    .speech {
      position: relative;
      background: var(--bubble);
      color: #1a1f2f;
      border-radius: 24px;
      border: 3px solid #10131f;
      padding: clamp(20px, 3vw, 28px);
      box-shadow: 8px 8px 0 #10131f;
      min-height: 134px;
    }

    .speech::after {
      content: "";
      position: absolute;
      left: 46px;
      bottom: -20px;
      width: 24px;
      height: 24px;
      background: var(--bubble);
      border-left: 3px solid #10131f;
      border-bottom: 3px solid #10131f;
      transform: rotate(-45deg);
    }

    #main-text {
      margin: 0;
      font-size: clamp(1.16rem, 3.1vw, 2rem);
      font-weight: 800;
      line-height: 1.35;
      letter-spacing: 0.01em;
      min-height: 2.7em;
    }

    .cursor {
      display: inline-block;
      width: 2px;
      height: 1.1em;
      background: #1f2538;
      margin-left: 4px;
      animation: blink 0.8s step-end infinite;
      vertical-align: -2px;
    }

    @keyframes blink {
      50% { opacity: 0; }
    }

    .status-bubble {
      margin-top: 20px;
      min-height: 34px;
      font-size: 1.04rem;
      font-weight: 700;
      color: #ffe89d;
      text-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
    }

    .btn-zone {
      position: relative;
      margin-top: 28px;
      min-height: 190px;
      border-radius: 18px;
      border: 1px dashed rgba(255, 255, 255, 0.2);
      background: rgba(7, 12, 20, 0.25);
      overflow: hidden;
      padding: 14px;
      z-index: 2;
    }

    .button-track {
      position: absolute;
      inset: 0;
      pointer-events: none;
    }

    .action-btn {
      border: 0;
      border-radius: 14px;
      padding: 14px 22px;
      font-size: clamp(0.98rem, 2.6vw, 1.14rem);
      font-weight: 800;
      cursor: pointer;
      transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease;
      user-select: none;
      -webkit-tap-highlight-color: transparent;
      touch-action: manipulation;
      position: absolute;
    }

    .action-btn:active {
      transform: translateY(1px) scale(0.98);
    }

    #yes-btn {
      left: 22px;
      top: 50%;
      transform: translateY(-50%);
      color: white;
      background: linear-gradient(135deg, #f2455b, #d7263d);
      box-shadow: 0 10px 24px rgba(215, 38, 61, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.25);
    }

    #yes-btn:hover {
      filter: brightness(1.06);
      transform: translateY(-52%) scale(1.03);
    }

    #no-btn {
      right: 22px;
      top: 50%;
      transform: translateY(-50%);
      color: #fff6fb;
      background: linear-gradient(135deg, #2b5bdd, #0f4cdb);
      box-shadow: 0 10px 24px rgba(15, 76, 219, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.25);
    }

    #no-btn.runaway {
      animation: wobble 260ms ease;
    }

    @keyframes wobble {
      0% { transform: scale(1) rotate(0deg); }
      25% { transform: scale(1.05) rotate(-5deg); }
      50% { transform: scale(0.98) rotate(4deg); }
      75% { transform: scale(1.04) rotate(-2deg); }
      100% { transform: scale(1) rotate(0deg); }
    }

    .tool-row {
      margin-top: 20px;
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
      z-index: 2;
      position: relative;
    }

    .sound-btn {
      border: 1px solid rgba(255, 255, 255, 0.28);
      background: rgba(10, 15, 26, 0.6);
      color: #dce8ff;
      padding: 10px 14px;
      border-radius: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: all 180ms ease;
    }

    .sound-btn:hover {
      transform: translateY(-1px);
      background: rgba(15, 22, 38, 0.92);
      box-shadow: 0 6px 14px rgba(0, 0, 0, 0.24);
    }

    .sound-note {
      font-size: 0.9rem;
      color: #bdd0ff;
      opacity: 0.85;
    }

    .celebrate {
      display: none;
      margin-top: 24px;
      position: relative;
      z-index: 2;
      border-radius: 20px;
      background: linear-gradient(145deg, rgba(215, 38, 61, 0.2), rgba(15, 76, 219, 0.24));
      border: 1px solid rgba(255, 255, 255, 0.24);
      padding: clamp(20px, 3.2vw, 28px);
      text-align: center;
      animation: popIn 500ms ease;
      overflow: hidden;
    }

    @keyframes popIn {
      from { opacity: 0; transform: scale(0.92); }
      to { opacity: 1; transform: scale(1); }
    }

    .celebrate h2 {
      margin: 0;
      font-size: clamp(1.6rem, 4vw, 2.6rem);
      color: #ffe69d;
      text-shadow: 0 2px 12px rgba(0, 0, 0, 0.32);
    }

    #confetti-layer,
    #heart-layer,
    #web-burst-layer {
      position: fixed;
      inset: 0;
      pointer-events: none;
      overflow: hidden;
      z-index: 999;
    }

    .confetti {
      position: absolute;
      width: 10px;
      height: 16px;
      opacity: 0.95;
      animation: confettiDrop linear forwards;
    }

    @keyframes confettiDrop {
      from { transform: translate3d(0, -12vh, 0) rotate(0deg); opacity: 1; }
      to { transform: translate3d(var(--x-end), 112vh, 0) rotate(720deg); opacity: 0.95; }
    }

    .float-heart {
      position: absolute;
      font-size: 24px;
      animation: heartRise 3.8s ease-in forwards;
      filter: drop-shadow(0 3px 8px rgba(0, 0, 0, 0.35));
    }

    @keyframes heartRise {
      from {
        transform: translateY(0) scale(0.9);
        opacity: 0;
      }
      14% { opacity: 1; }
      to {
        transform: translateY(-90vh) scale(1.38) translateX(var(--drift));
        opacity: 0;
      }
    }

    .web-streak {
      position: absolute;
      width: 140px;
      height: 140px;
      opacity: 0.46;
      animation: webSwipe 2.5s ease forwards;
    }

    @keyframes webSwipe {
      from {
        transform: translate(-15vw, 15vh) rotate(-20deg) scale(0.5);
        opacity: 0;
      }
      30% { opacity: 0.6; }
      to {
        transform: translate(110vw, -25vh) rotate(24deg) scale(1.15);
        opacity: 0;
      }
    }

    .footer {
      margin-top: 20px;
      text-align: center;
      color: rgba(255, 255, 255, 0.76);
      font-size: 0.88rem;
      letter-spacing: 0.02em;
      z-index: 2;
      position: relative;
    }

    @media (max-width: 760px) {
      .stage {
        padding: 10px;
      }

      .card {
        border-radius: 22px;
        padding: 16px;
      }

      .btn-zone {
        min-height: 210px;
      }

      #yes-btn,
      #no-btn {
        min-width: 116px;
      }

      .speech {
        box-shadow: 6px 6px 0 #10131f;
      }
    }
  </style>
</head>
<body>
  <div class="stage">
    <div class="comic-dots"></div>
    <div class="cityline"></div>

    <svg class="float-web w1" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cae2ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
    <svg class="float-web w2" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cae2ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
    <svg class="float-web w3" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cae2ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>
    <svg class="float-web w4" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90" stroke="#cae2ff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>

    <div class="sparkle" style="top:10%; left:21%; animation-delay:0.1s"></div>
    <div class="sparkle" style="top:18%; right:18%; animation-delay:1.2s"></div>
    <div class="sparkle" style="top:30%; left:8%; animation-delay:0.8s"></div>
    <div class="sparkle" style="top:35%; right:9%; animation-delay:1.9s"></div>
    <div class="sparkle" style="bottom:28%; left:16%; animation-delay:0.3s"></div>
    <div class="sparkle" style="bottom:20%; right:22%; animation-delay:1.6s"></div>

    <div class="spider-wrap" aria-hidden="true">
      <div class="thread"></div>
      <div class="spider">
        <div class="spider-body"></div>
        <span class="leg l1"></span><span class="leg l2"></span><span class="leg l3"></span><span class="leg l4"></span>
      </div>
    </div>

    <div class="card" role="main" aria-live="polite">
      <div class="title-chip"><span class="chip-dot"></span>Hero Movie Mission</div>

      <div class="speech-wrap">
        <div class="speech">
          <p id="main-text"></p><span class="cursor" id="cursor"></span>
        </div>
      </div>

      <div class="status-bubble" id="status-msg"></div>

      <div class="btn-zone" id="btn-zone">
        <button class="action-btn" id="yes-btn" aria-label="Yes button">❤️ Yes!</button>
        <button class="action-btn" id="no-btn" aria-label="No button">🕸️ No</button>
      </div>

      <div class="tool-row">
        <button class="sound-btn" id="sound-btn">Enable Sound</button>
        <span class="sound-note">Soft ambient tune starts only after click.</span>
      </div>

      <div class="celebrate" id="celebrate-panel">
        <h2>YAY!! ❤️ See you tomorrow! Can't wait 🕷️🍿</h2>
      </div>

      <div class="footer">Made with ❤️</div>
    </div>
  </div>

  <div id="confetti-layer"></div>
  <div id="heart-layer"></div>
  <div id="web-burst-layer"></div>

  <script>
    const message = "Will you come with me to watch the Spider-Man movie tomorrow, 01/08 evening? 🕷️❤️";
    const textNode = document.getElementById("main-text");
    const cursor = document.getElementById("cursor");
    const statusNode = document.getElementById("status-msg");
    const yesBtn = document.getElementById("yes-btn");
    const noBtn = document.getElementById("no-btn");
    const btnZone = document.getElementById("btn-zone");
    const celebratePanel = document.getElementById("celebrate-panel");
    const confettiLayer = document.getElementById("confetti-layer");
    const heartLayer = document.getElementById("heart-layer");
    const webBurstLayer = document.getElementById("web-burst-layer");

    const playful = [
      "Nice try 😏",
      "Spider-Sense says no isn't an option!",
      "You missed! 🕷️",
      "Try again 😂"
    ];

    let typed = 0;
    function typeWriter() {
      if (typed < message.length) {
        textNode.textContent += message.charAt(typed);
        typed += 1;
        setTimeout(typeWriter, 38 + Math.random() * 22);
      } else {
        cursor.style.display = "none";
      }
    }
    typeWriter();

    function randomInt(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function moveNoButton() {
      const zoneRect = btnZone.getBoundingClientRect();
      const btnRect = noBtn.getBoundingClientRect();
      const maxX = Math.max(6, zoneRect.width - btnRect.width - 6);
      const maxY = Math.max(6, zoneRect.height - btnRect.height - 6);
      const x = randomInt(6, Math.floor(maxX));
      const y = randomInt(6, Math.floor(maxY));

      noBtn.style.left = x + "px";
      noBtn.style.top = y + "px";
      noBtn.style.right = "auto";
      noBtn.style.transform = "none";

      noBtn.classList.remove("runaway");
      void noBtn.offsetWidth;
      noBtn.classList.add("runaway");

      statusNode.textContent = playful[randomInt(0, playful.length - 1)];
    }

    ["mouseenter", "touchstart", "click"].forEach((eventName) => {
      noBtn.addEventListener(eventName, (ev) => {
        ev.preventDefault();
        moveNoButton();
      }, { passive: false });
    });

    function createConfettiBurst() {
      const colors = ["#ff4d6d", "#ffd447", "#39a0ff", "#ffffff", "#8df7c0"];
      for (let i = 0; i < 130; i += 1) {
        const c = document.createElement("div");
        c.className = "confetti";
        c.style.left = randomInt(0, 100) + "vw";
        c.style.top = randomInt(-15, 5) + "vh";
        c.style.background = colors[randomInt(0, colors.length - 1)];
        c.style.animationDuration = (2.4 + Math.random() * 2.2) + "s";
        c.style.setProperty("--x-end", randomInt(-25, 25) + "vw");
        c.style.transform = "rotate(" + randomInt(0, 360) + "deg)";
        confettiLayer.appendChild(c);
        setTimeout(() => c.remove(), 4700);
      }
    }

    function createHeartStream() {
      for (let i = 0; i < 34; i += 1) {
        const h = document.createElement("div");
        h.className = "float-heart";
        h.textContent = Math.random() > 0.5 ? "❤️" : "💙";
        h.style.left = randomInt(5, 95) + "vw";
        h.style.bottom = randomInt(-8, 8) + "vh";
        h.style.animationDelay = (Math.random() * 1.3) + "s";
        h.style.setProperty("--drift", randomInt(-10, 10) + "vw");
        heartLayer.appendChild(h);
        setTimeout(() => h.remove(), 5200);
      }
    }

    function createWebRush() {
      const webPath = "M50 5L50 95M5 50L95 50M18 18L82 82M82 18L18 82M10 35C32 44 68 44 90 35M10 65C32 56 68 56 90 65M35 10C44 32 44 68 35 90M65 10C56 32 56 68 65 90";
      for (let i = 0; i < 12; i += 1) {
        const wrap = document.createElement("div");
        wrap.className = "web-streak";
        wrap.style.top = randomInt(0, 85) + "vh";
        wrap.style.left = randomInt(-20, 10) + "vw";
        wrap.style.animationDelay = (Math.random() * 0.8) + "s";

        const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.setAttribute("viewBox", "0 0 100 100");
        svg.setAttribute("width", "100%");
        svg.setAttribute("height", "100%");

        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        path.setAttribute("d", webPath);
        path.setAttribute("stroke", "#cfe7ff");
        path.setAttribute("stroke-width", "2");
        path.setAttribute("fill", "none");
        path.setAttribute("stroke-linecap", "round");

        svg.appendChild(path);
        wrap.appendChild(svg);
        webBurstLayer.appendChild(wrap);
        setTimeout(() => wrap.remove(), 3200);
      }
    }

    yesBtn.addEventListener("click", () => {
      statusNode.textContent = "Heroic choice unlocked!";
      createConfettiBurst();
      createHeartStream();
      createWebRush();
      celebratePanel.style.display = "block";
      yesBtn.disabled = true;
      noBtn.disabled = true;
      yesBtn.style.opacity = "0.7";
      noBtn.style.opacity = "0.5";
    });

    let audioCtx = null;
    let gainNode = null;
    let oscillators = [];
    let soundEnabled = false;
    const soundBtn = document.getElementById("sound-btn");

    function startAmbientSound() {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      gainNode = audioCtx.createGain();
      gainNode.gain.value = 0.03;
      gainNode.connect(audioCtx.destination);

      const baseFreqs = [164.81, 220.0, 261.63];

      oscillators = baseFreqs.map((freq, idx) => {
        const osc = audioCtx.createOscillator();
        const oscGain = audioCtx.createGain();
        osc.type = idx === 1 ? "triangle" : "sine";
        osc.frequency.value = freq;
        oscGain.gain.value = idx === 1 ? 0.26 : 0.18;
        osc.connect(oscGain);
        oscGain.connect(gainNode);
        osc.start();
        return { osc, oscGain };
      });

      let t = 0;
      const lfo = setInterval(() => {
        if (!audioCtx || !gainNode) {
          clearInterval(lfo);
          return;
        }
        t += 0.12;
        const softPulse = 0.026 + (Math.sin(t) + 1) * 0.006;
        gainNode.gain.setTargetAtTime(softPulse, audioCtx.currentTime, 0.12);
      }, 160);

      soundBtn.dataset.lfo = String(lfo);
    }

    function stopAmbientSound() {
      if (!audioCtx) return;
      oscillators.forEach(({ osc }) => {
        try { osc.stop(); } catch (err) {}
      });
      oscillators = [];

      const lfo = Number(soundBtn.dataset.lfo || "0");
      if (lfo) {
        clearInterval(lfo);
      }

      audioCtx.close();
      audioCtx = null;
      gainNode = null;
    }

    soundBtn.addEventListener("click", async () => {
      if (!soundEnabled) {
        startAmbientSound();
        soundEnabled = true;
        soundBtn.textContent = "Sound On";
        statusNode.textContent = "Ambient soundtrack enabled.";
      } else {
        stopAmbientSound();
        soundEnabled = false;
        soundBtn.textContent = "Enable Sound";
        statusNode.textContent = "Sound paused.";
      }
    });
  </script>
</body>
</html>
"""

st.markdown(
    """
    <style>
      /* Hide Streamlit chrome for a clean landing-page feel */
      .stAppHeader, [data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer {
        visibility: hidden;
        height: 0;
        position: fixed;
      }
      .block-container {
        padding: 0 !important;
        max-width: 100% !important;
      }
      iframe {
        border: 0 !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(html, height=980, scrolling=False)
