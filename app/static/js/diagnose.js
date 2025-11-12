// diagnose.js
// Handles drag/drop, batch uploads, per-file progress, prediction display, session history

const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const resultsContainer = document.getElementById("results-container");
const historyList = document.getElementById("history-list");
const clearHistoryBtn = document.getElementById("clear-history");

const PREDICT_URL = "/predict"; // your FastAPI endpoint

// Utility: create element from HTML string
function el(html) {
  const template = document.createElement('template');
  template.innerHTML = html.trim();
  return template.content.firstChild;
}

// Initialize
function init() {
  // drag events
  ;["dragenter", "dragover"].forEach(evt =>
    dropZone.addEventListener(evt, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add("dragover");
    })
  );
  ;["dragleave", "drop"].forEach(evt =>
    dropZone.addEventListener(evt, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove("dragover");
    })
  );

  dropZone.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    if (!dt) return;
    const files = dt.files;
    handleFiles(files);
  });

  fileInput.addEventListener("change", (e) => {
    handleFiles(fileInput.files);
    fileInput.value = ""; // reset
  });

  clearHistoryBtn.addEventListener("click", () => {
    sessionStorage.removeItem("neuroscan_history");
    renderHistory();
  });

  renderHistory();
}

// Handle FileList
function handleFiles(fileList) {
  // clear previous results on each call
  resultsContainer.innerHTML = "";

  if (!fileList || fileList.length === 0) return;
  const files = Array.from(fileList);
  files.forEach(file => {
    if (!file.type.startsWith("image/")) {
      alert(`Skipping ${file.name}: not an image.`);
      return;
    }
    renderPendingCard(file);
  });
}

// Render a pending card, start upload
function renderPendingCard(file) {
  const card = el(`
    <div class="result-card" id="card-${escapeId(file.name + "-" + Date.now())}">
      <img class="thumb" src="" alt="thumb" />
      <div class="result-meta">
        <div class="filename">${escapeHtml(file.name)}</div>
        <div class="progress mb-2">
          <div class="bar1 progress-bar progress-bar-striped progress-bar-animated" style="width:0%">0%</div>
          <div class="bar2 progress-bar " style="width:0%">0%</div>
        </div>
        <div class="small text-muted">Waiting for upload...</div>
      </div>
      <div class="text-end">
        <div class="badge-status bg-secondary text-white">Pending</div>
      </div>
    </div>
  `);
  resultsContainer.prepend(card);

  // set thumbnail
  const imgEl = card.querySelector(".thumb");
  const reader = new FileReader();
  reader.onload = (ev) => imgEl.src = ev.target.result;
  reader.readAsDataURL(file);

  // start upload/predict
  uploadAndPredict(file, card);
}

// Upload using XMLHttpRequest to get progress events
function uploadAndPredict(file, card) {
  const progressBar = card.querySelector(".bar1");
  const progressBar2 = card.querySelector(".bar2");
  const statusText = card.querySelector(".result-meta .small");
  const badge = card.querySelector(".badge-status");

  const xhr = new XMLHttpRequest();
  const form = new FormData();
  form.append("file", file);

  xhr.open("POST", PREDICT_URL, true);

  // upload progress
  xhr.upload.onprogress = function(e) {
    if (e.lengthComputable) {
      const pct = Math.round((e.loaded / e.total) * 100);
      progressBar.style.width = pct + "%";
      progressBar.textContent = pct + "%";
    }
  };

  // response
  xhr.onload = function() {
    if (xhr.status >= 200 && xhr.status < 300) {
      try {
        const resp = JSON.parse(xhr.responseText);
        const prediction = resp.prediction || "Unknown";
        let confidence = resp.confidence;
        confidence = Number(confidence); // ensure number

        // update UI
        progressBar.classList.remove("progress-bar-striped","progress-bar-animated");
        progressBar.classList.add("bg-success");
        progressBar2.classList.add("bg-danger");
        const inverse = (100 - Number(confidence)).toFixed(2);
        progressBar.style.width = inverse + "%";
        progressBar.textContent = inverse + "%";
        progressBar2.style.width = confidence + "%";
        progressBar2.textContent = confidence + "%";
        statusText.textContent = `${prediction} (${confidence > 50 ? confidence : 100 - confidence}%)`;

        // color badge
        badge.textContent = prediction;
        badge.classList.remove("bg-secondary","bg-success","bg-warning","bg-danger");
        if (prediction.toLowerCase().includes("malign")) badge.classList.add("bg-danger");
        else badge.classList.add("bg-success");

        // save to session history
        saveToHistory({
          filename: file.name,
          prediction,
          confidence,
          timestamp: new Date().toLocaleString(),
          thumb: card.querySelector(".thumb").src
        });

      } catch (err) {
        statusText.textContent = "Invalid response";
        badge.textContent = "Error";
        badge.classList.remove("bg-secondary");
        badge.classList.add("bg-danger");
      }
    } else {
      statusText.textContent = `Upload failed (${xhr.status})`;
      badge.textContent = "Error";
      badge.classList.remove("bg-secondary");
      badge.classList.add("bg-danger");
    }
  };

  xhr.onerror = function() {
    statusText.textContent = "Network error";
    badge.textContent = "Error";
    badge.classList.remove("bg-secondary");
    badge.classList.add("bg-danger");
  };

  xhr.send(form);
}

// Save record in sessionStorage
function saveToHistory(record) {
  const key = "neuroscan_history";
  const existing = JSON.parse(sessionStorage.getItem(key) || "[]");
  existing.unshift(record); // newest first
  // optionally limit history length
  const trimmed = existing.slice(0, 200);
  sessionStorage.setItem(key, JSON.stringify(trimmed));
  renderHistory();
}

// Render history list
function renderHistory() {
  const key = "neuroscan_history";
  const list = JSON.parse(sessionStorage.getItem(key) || "[]");
  if (!list.length) {
    historyList.innerHTML = `<div class="text-muted small">No predictions during this session.</div>`;
    return;
  }

  historyList.innerHTML = list.map(item => `
    <div class="history-item d-flex gap-2 align-items-center">
      <img src="${item.thumb || '/static/img/brain-illustration.png'}" style="width:48px;height:48px;object-fit:cover;border-radius:6px;border:1px solid #eee" alt="thumb" />
      <div class="flex-fill">
        <div class="small"><strong>${escapeHtml(item.filename)}</strong> — <span class="text-muted">${escapeHtml(item.prediction)}</span></div>
        <div class="d-flex gap-2 align-items-center mt-1">
          <div class="progress flex-grow-1" style="height:10px;">
            <div class="progress-bar ${Number(item.confidence) >= 80 ? 'bg-danger' : (Number(item.confidence) >= 60 ? 'bg-warning' : 'bg-success')}" style="width:${item.confidence}%"></div>
          </div>
          <div class="small text-muted" style="min-width:90px;text-align:right">${item.confidence}%</div>
        </div>
        <div class="small text-muted mt-1">${escapeHtml(item.timestamp)}</div>
      </div>
    </div>
  `).join("");
}

// Helpers to avoid XSS and invalid ids
function escapeHtml(s="") {
  if (s === null || s === undefined) return "";
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}
function escapeId(s="") {
  return btoa(s).replace(/=/g,'');
}

// Initialize once DOM loaded
document.addEventListener("DOMContentLoaded", init);
