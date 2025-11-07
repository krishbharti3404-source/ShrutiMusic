<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>YouTube-style Thumbnail / Mini Player</title>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700;900&display=swap" rel="stylesheet">
  <style>
    :root{
      --bg:#0f0f10;
      --card-bg: rgba(255,255,255,0.06);
      --accent: #ffd166;
      --muted: rgba(255,255,255,0.75);
    }
    *{box-sizing:border-box}
    html,body{height:100%;margin:0;background:var(--bg);font-family:Montserrat,system-ui,Arial}

    /* Container that mimics the blurred player background */
    .stage{
      position:relative;
      min-height:100vh;
      display:flex;
      align-items:center;
      justify-content:center;
      padding:48px 20px;
      overflow:hidden;
      background:linear-gradient(180deg,#0000,rgba(0,0,0,0.45));
    }

    /* background image blurred and dimmed */
    .bg-image{
      position:absolute;inset:0;z-index:0;background-size:cover;background-position:center;filter:blur(14px) brightness(30%);transform:scale(1.06);
    }

    .center-col{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;gap:26px;width:100%;max-width:820px}

    /* thumbnail card (rounded) */
    .thumb{
      width:560px;height:320px;border-radius:28px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,0.6);position:relative;background:#111;
      background-size:cover;background-position:center;display:flex;align-items:flex-start;justify-content:flex-end;padding:22px;
    }

    /* the white text badge top-left */
    .views-badge{position:absolute;left:20px;top:18px;font-weight:800;color:white;font-size:28px;letter-spacing:0.5px}
    .views-badge small{display:block;font-weight:700;color:var(--accent);font-size:18px}

    /* Title inside the thumbnail */
    .thumb h2{margin:0;color:#eaeaea;font-weight:700;font-size:38px;line-height:0.95;text-align:left}
    .thumb .meta{position:absolute;left:24px;bottom:18px;color:rgba(255,255,255,0.75);font-size:12px}

    /* Illustration overlay to the right (we'll just use the background image) */
    .thumb::after{content:'';position:absolute;inset:0; background:linear-gradient(90deg, rgba(0,0,0,0.55) 30%, rgba(0,0,0,0) 80%);}

    /* Title and duration below the card */
    .title{color:#fff;font-size:28px;font-weight:700;text-align:center}
    .duration{color:rgba(255,255,255,0.8);margin-top:6px;font-weight:600}

    /* player controls */
    .controls{
      margin-top:18px;background:var(--card-bg);backdrop-filter:blur(6px);border-radius:28px;padding:18px 28px;display:flex;align-items:center;gap:18px;box-shadow:0 10px 30px rgba(0,0,0,0.6)
    }
    .icon-btn{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;cursor:pointer}
    .icon-btn.small{width:36px;height:36px}
    .play{width:64px;height:64px;border-radius:999px;background:linear-gradient(180deg,#fff,#f1f1f1);display:grid;place-items:center;box-shadow:0 6px 20px rgba(0,0,0,0.35)}

    /* responsive tweaks */
    @media (max-width:720px){
      .thumb{width:92%;height:220px;border-radius:18px}
      .title{font-size:20px}
      .views-badge{font-size:20px}
      .play{width:54px;height:54px}
    }

    /* simple svg icon styles */
    svg{display:block;width:22px;height:22px}
    .muted{opacity:0.85}
  </style>
</head>
<body>
  <div class="stage">
    <!-- background: replace 'code.jpg' with your image file placed next to this HTML -->
    <div class="bg-image" style="background-image:url('code.jpg')"></div>

    <div class="center-col">

      <div class="thumb" style="background-image:url('code.jpg')">
        <div class="views-badge">70000000+ <small>VIEWS</small></div>

        <div style="width:50%;padding:8px 12px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start">
          <h2>SAMAY<br/>SAMJHAYEGA</h2>
        </div>

        <div class="meta">Singer: Mohit Lalwani<br/>Music: Bharat Kamal</div>
      </div>

      <div style="text-align:center;">
        <div class="title">Samay Samjhayega Full Song Tum...</div>
        <div class="duration">3:19</div>
      </div>

      <div class="controls" role="region" aria-label="player controls">
        <button class="icon-btn small" title="repeat">
          <!-- repeat icon -->
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"></polyline><path d="M3 11v-1a4 4 0 0 1 4-4h14"></path><polyline points="7 23 3 19 7 15"></polyline><path d="M21 13v1a4 4 0 0 1-4 4H3"></path></svg>
        </button>

        <button class="icon-btn" title="previous">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><polygon points="19 20 9 12 19 4 19 20"></polygon><line x1="5" y1="19" x2="5" y2="5"></line></svg>
        </button>

        <div class="play" title="play/pause">
          <svg viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
        </div>

        <button class="icon-btn" title="next">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 4 15 12 5 20 5 4"></polygon><line x1="19" y1="5" x2="19" y2="19"></line></svg>
        </button>

        <button class="icon-btn small" title="shuffle">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line></svg>
        </button>
      </div>

    </div>
  </div>

  <script>
    // small interactivity: toggle play/pause
    const playBtn = document.querySelector('.play');
    let playing = false;
    playBtn.addEventListener('click', ()=>{
      playing = !playing;
      if(playing){
        playBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16" rx="1"></rect><rect x="14" y="4" width="4" height="16" rx="1"></rect></svg>'
      } else {
        playBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>'
      }
    })
  </script>
</body>
</html>
