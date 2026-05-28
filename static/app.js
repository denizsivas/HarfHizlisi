const startScreen = document.getElementById("start-screen");
const gameScreen = document.getElementById("game-screen");
const startBtn = document.getElementById("start-btn");
const guessForm = document.getElementById("guess-form");
const guessInput = document.getElementById("guess-input");
const nextBtn = document.getElementById("next-btn");
const restartBtn = document.getElementById("restart-btn");
const feedbackEl = document.getElementById("feedback");

const questionLabel = document.getElementById("question-label");
const totalScoreEl = document.getElementById("total-score");
const potentialPointsEl = document.getElementById("potential-points");
const roundTitleEl = document.getElementById("round-title");
const categoryBadgeEl = document.getElementById("category-badge");
const runSummaryEl = document.getElementById("run-summary");
const hintEl = document.getElementById("hint");
const maskedWordEl = document.getElementById("masked-word");
const timerFillEl = document.getElementById("timer-fill");
const timerTextEl = document.getElementById("timer-text");

let gameId = null;
let pollTimer = null;
let uiTimer = null;
let latestState = null;
let pollGeneration = 0;
let roundEpoch = 0;

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Bir hata oluştu");
  }

  return response.json();
}

function showFeedback(message, tone = "neutral") {
  feedbackEl.textContent = message;
  feedbackEl.className = `feedback ${tone}`;
}

function extractRoundEpoch(state) {
  return `${state.question_number}:${state.round.round_elapsed_seconds}:${state.round.hint}`;
}

function renderRunSummary(state) {
  const history = state.round_history || [];
  if (!history.length) {
    runSummaryEl.classList.add("hidden");
    runSummaryEl.innerHTML = "";
    return;
  }

  runSummaryEl.classList.remove("hidden");
  runSummaryEl.innerHTML = `
    <h3>${state.category_label} turu — cevapların</h3>
    <ul>
      ${history
        .map(
          (item) => `
        <li>
          <span>S${item.question_number}: ${item.word}</span>
          <span class="points${item.points > 0 ? "" : " zero"}">${item.points > 0 ? `+${item.points}` : "0"}</span>
        </li>`
        )
        .join("")}
    </ul>
  `;
}

function renderState(state, epoch = null) {
  if (epoch !== null && epoch < roundEpoch) {
    return;
  }
  if (epoch !== null) {
    roundEpoch = epoch;
  }

  latestState = state;
  const round = state.round;

  questionLabel.textContent = `${state.question_number} / ${state.total_questions}`;
  totalScoreEl.textContent = state.total_score;
  potentialPointsEl.textContent = round.potential_points;
  roundTitleEl.textContent = round.label;
  categoryBadgeEl.textContent = `${state.category_label} · ${state.category_description}`;
  hintEl.textContent = round.hint;
  maskedWordEl.textContent = round.masked_word;

  const interval = round.reveal_interval_seconds;
  const remaining = round.seconds_until_next_reveal;
  const progress = round.hidden_count > 0 ? remaining / interval : 0;

  timerFillEl.style.transform = `scaleX(${Math.max(0, Math.min(1, progress))})`;
  timerTextEl.textContent =
    round.hidden_count > 0 ? `${Math.ceil(remaining)}s` : "—";

  const gameDone = state.game_status === "finished";

  guessInput.disabled = gameDone;
  guessForm.querySelector("button").disabled = gameDone;

  if (gameDone) {
    maskedWordEl.textContent = state.revealed_word || round.last_guess || round.masked_word;
    restartBtn.classList.remove("hidden");
    renderRunSummary(state);
  } else {
    restartBtn.classList.add("hidden");
    runSummaryEl.classList.add("hidden");
    runSummaryEl.innerHTML = "";
  }

  nextBtn.classList.add("hidden");
}

let timeoutInFlight = false;

async function handleTimeout() {
  if (!gameId || timeoutInFlight) return;

  timeoutInFlight = true;
  stopPolling();

  try {
    const result = await api(`/api/game/${gameId}/timeout`, { method: "POST" });
    const nextEpoch = Date.now();
    renderState(result, nextEpoch);
    guessInput.value = "";

    if (result.game_status === "finished") {
      showFeedback(result.message, "error");
    } else {
      showFeedback(result.message, "error");
      guessInput.focus();
      startPolling();
    }
  } catch (error) {
    showFeedback(error.message, "error");
    startPolling();
  } finally {
    timeoutInFlight = false;
  }
}

async function refreshState() {
  if (!gameId) return;

  const generation = pollGeneration;
  const state = await api(`/api/game/${gameId}`);

  if (generation !== pollGeneration) return;

  if (state.game_status !== "finished" && state.round.timed_out) {
    await handleTimeout();
    return;
  }

  renderState(state);
}

function startPolling() {
  stopPolling();
  pollTimer = window.setInterval(refreshState, 1000);
  uiTimer = window.setInterval(() => {
    if (!latestState || latestState.game_status === "finished") return;
    if (latestState.round.status !== "playing") return;

    const round = latestState.round;
    const interval = round.reveal_interval_seconds;
    const remaining = Math.max(0, round.seconds_until_next_reveal - 1);
    latestState.round.seconds_until_next_reveal = remaining;
    const progress = round.hidden_count > 0 ? remaining / interval : 0;
    timerFillEl.style.transform = `scaleX(${Math.max(0, Math.min(1, progress))})`;
    timerTextEl.textContent =
      round.hidden_count > 0 ? `${Math.ceil(remaining)}s` : "—";
  }, 1000);
}

function stopPolling() {
  pollGeneration += 1;
  if (pollTimer) window.clearInterval(pollTimer);
  if (uiTimer) window.clearInterval(uiTimer);
  pollTimer = null;
  uiTimer = null;
}

async function startGame() {
  startBtn.disabled = true;
  try {
    const data = await api("/api/game/start", { method: "POST" });
    gameId = data.game_id;
    roundEpoch = 0;
    startScreen.classList.add("hidden");
    gameScreen.classList.remove("hidden");
    renderState(data.state, Date.now());
    guessInput.value = "";
    guessInput.focus();
    showFeedback(`${data.state.category_label} temasıyla başlıyorsun!`, "neutral");
    runSummaryEl.classList.add("hidden");
    runSummaryEl.innerHTML = "";
    startPolling();
  } catch (error) {
    showFeedback(error.message, "error");
  } finally {
    startBtn.disabled = false;
  }
}

guessForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const guess = guessInput.value.trim();
  if (!guess || !gameId) return;

  stopPolling();

  try {
    const result = await api(`/api/game/${gameId}/guess`, {
      method: "POST",
      body: JSON.stringify({ guess }),
    });

    const nextEpoch = Date.now();
    renderState(result, nextEpoch);

    if (result.correct) {
      guessInput.value = "";

      if (result.game_status === "finished") {
        showFeedback(
          `${result.revealed_word} — +${result.points_awarded} puan. Oyun bitti! Toplam: ${result.total_score}`,
          "success"
        );
      } else {
        showFeedback(
          `${result.revealed_word} — +${result.points_awarded} puan. Sonraki soru!`,
          "success"
        );
        guessInput.focus();
        startPolling();
      }
    } else {
      showFeedback(result.message, "error");
      guessInput.select();
      startPolling();
    }
  } catch (error) {
    showFeedback(error.message, "error");
    startPolling();
  }
});

restartBtn.addEventListener("click", () => {
  stopPolling();
  gameId = null;
  latestState = null;
  roundEpoch = 0;
  gameScreen.classList.add("hidden");
  startScreen.classList.remove("hidden");
  runSummaryEl.classList.add("hidden");
  runSummaryEl.innerHTML = "";
  showFeedback("", "neutral");
});

startBtn.addEventListener("click", startGame);
