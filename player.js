// player.js — site-wide persistent music player
// Lives at the site root, referenced by every page via:
//   <script src="/player.js"></script>

(function () {

  // ============================================================
  // TRACKS START HERE. Can add playlists and individual tracks.
  // ============================================================
  var PLAYLISTS = {
    lofi: {
      label: "Lofi",
      tracks: [
        { title: "Daggerfall Tavern Lofi", src: "/music/daggerfalltavernlofi.mp3" },
        { title: "Peaceful Waters",        src: "/music/peacefulwaters.mp3" },
        { title: "Wings of Kynareth",      src: "/music/wingsofkynareth.mp3" },
        { title: "Dead Moon",              src: "/music/deadmoon.m4a" }
      ]
    }
  };

  var STORAGE_KEY = "scribeUnmooredPlayerState";
  var SAVE_INTERVAL_MS = 5000;

  var audio = new Audio();
  var state = {
    playlist: "lofi",
    trackIndex: 0,
    currentTime: 0,
    isPlaying: false,
    collapsed: false
  };

  var els = {}; // populated once the bar is built

  // ---------- persistence ----------

  function loadState() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      var saved = JSON.parse(raw);
      if (saved && typeof saved === "object") {
        Object.assign(state, saved);
      }
    } catch (e) {
      // Corrupt or missing state — just use the defaults.
    }
  }

  function saveState() {
    state.currentTime = audio.currentTime || 0;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {
      // Storage unavailable (private browsing, quota, etc) — non-fatal.
    }
  }

  // ---------- helpers ----------

  function currentTracks() {
    var pl = PLAYLISTS[state.playlist];
    return pl ? pl.tracks : [];
  }

  function currentTrack() {
    var tracks = currentTracks();
    return tracks[state.trackIndex] || null;
  }

  var ICON_PLAY = '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>';
  var ICON_PAUSE = '<svg viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>';

  function updateTrackLabel() {
    var track = currentTrack();
    els.title.textContent = track ? track.title : "No tracks in this playlist yet";
  }

  function updatePlayIcon() {
    els.playBtn.innerHTML = state.isPlaying ? ICON_PAUSE : ICON_PLAY;
    els.playBtn.setAttribute("aria-label", state.isPlaying ? "Pause" : "Play");
  }

  function updateCollapsedUI() {
    els.bar.classList.toggle("collapsed", state.collapsed);
    document.body.classList.toggle("player-collapsed", state.collapsed);
    els.handle.setAttribute("aria-expanded", state.collapsed ? "false" : "true");
  }

  // ---------- playback ----------

  function loadTrack(autoplay) {
    var track = currentTrack();
    updateTrackLabel();
    if (els.select.value !== state.playlist) els.select.value = state.playlist;

    if (!track) {
      audio.removeAttribute("src");
      state.isPlaying = false;
      updatePlayIcon();
      return;
    }

    audio.src = track.src;
    if (state.currentTime > 0) {
      // Only meaningful right after a page-load restore; cleared after use.
      audio.currentTime = state.currentTime;
    }

    if (autoplay) {
      var p = audio.play();
      if (p && p.catch) {
        p.catch(function () {
          // Autoplay blocked by the browser — fall back to paused.
          // This can happen on a fresh page load depending on the
          // browser's autoplay policy; the user just taps play again.
          state.isPlaying = false;
          updatePlayIcon();
        });
      }
    }
  }

  function play() {
    if (!currentTrack()) return;
    var p = audio.play();
    if (p && p.catch) p.catch(function () {});
    state.isPlaying = true;
    updatePlayIcon();
    saveState();
  }

  function pause() {
    audio.pause();
    state.isPlaying = false;
    updatePlayIcon();
    saveState();
  }

  function togglePlay() {
    if (state.isPlaying) pause(); else play();
  }

  function step(direction) {
    var tracks = currentTracks();
    if (!tracks.length) return;
    state.trackIndex = (state.trackIndex + direction + tracks.length) % tracks.length;
    state.currentTime = 0;
    loadTrack(state.isPlaying);
    saveState();
  }

  function switchPlaylist(key) {
    if (!PLAYLISTS[key] || key === state.playlist) return;
    state.playlist = key;
    state.trackIndex = 0;
    state.currentTime = 0;
    loadTrack(state.isPlaying);
    saveState();
  }

  function toggleCollapsed() {
    state.collapsed = !state.collapsed;
    updateCollapsedUI();
    saveState();
  }

  // ---------- build the bar ----------

  function buildBar() {
    var bar = document.createElement("div");
    bar.className = "player-bar";
    bar.innerHTML =
      '<div class="player-handle" id="player-handle" role="button" tabindex="0" ' +
        'aria-label="Toggle player" aria-expanded="true">' +
        'Player <span class="player-handle-arrow">&#9662;</span>' +
      '</div>' +
      '<div class="player-bar-inner">' +
        '<div class="player-controls">' +
          '<button class="player-btn" id="player-prev" aria-label="Previous track">' +
            '<svg viewBox="0 0 24 24"><path d="M6 6h2v12H6zm3.5 6 8.5 6V6z"/></svg>' +
          '</button>' +
          '<button class="player-btn player-play" id="player-play" aria-label="Play">' + ICON_PLAY + '</button>' +
          '<button class="player-btn" id="player-next" aria-label="Next track">' +
            '<svg viewBox="0 0 24 24"><path d="M6 18l8.5-6L6 6v12zm2-8.14 5.14 2.14L8 14.14V9.86zM16 6h2v12h-2z"/></svg>' +
          '</button>' +
        '</div>' +
        '<div class="player-divider"></div>' +
        '<div class="player-track-info">' +
          '<div class="player-track-title" id="player-track-title">&mdash;</div>' +
          '<div class="player-track-sub">THE SCRIBE UNMOORED &mdash; SOUNDTRACK</div>' +
        '</div>' +
        '<div class="player-playlist-select">' +
          '<select id="player-playlist-select" aria-label="Choose playlist"></select>' +
        '</div>' +
      '</div>';

    document.body.appendChild(bar);

    els.bar = bar;
    els.handle = bar.querySelector("#player-handle");
    els.playBtn = bar.querySelector("#player-play");
    els.prevBtn = bar.querySelector("#player-prev");
    els.nextBtn = bar.querySelector("#player-next");
    els.title = bar.querySelector("#player-track-title");
    els.select = bar.querySelector("#player-playlist-select");

    Object.keys(PLAYLISTS).forEach(function (key) {
      var opt = document.createElement("option");
      opt.value = key;
      opt.textContent = PLAYLISTS[key].label;
      els.select.appendChild(opt);
    });

    els.handle.addEventListener("click", toggleCollapsed);
    els.handle.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggleCollapsed(); }
    });
    els.playBtn.addEventListener("click", togglePlay);
    els.prevBtn.addEventListener("click", function () { step(-1); });
    els.nextBtn.addEventListener("click", function () { step(1); });
    els.select.addEventListener("change", function () { switchPlaylist(els.select.value); });

    audio.addEventListener("ended", function () { step(1); });
  }

  // ---------- init ----------

  document.addEventListener("DOMContentLoaded", function () {
    loadState();
    buildBar();
    els.select.value = state.playlist;
    updateCollapsedUI();

    // Restore whatever was loaded/playing on the previous page.
    var wasPlaying = state.isPlaying;
    loadTrack(wasPlaying);
    updatePlayIcon();

    // Periodic save so a hard refresh / crash doesn't lose much progress.
    setInterval(function () {
      if (state.isPlaying) saveState();
    }, SAVE_INTERVAL_MS);

    window.addEventListener("pagehide", saveState);
  });

})();
