document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('estimation-form');
  const userStoryInput = document.getElementById('user-story');
  const submitBtn = document.getElementById('submit-btn');
  const btnText = document.getElementById('btn-text');
  const btnSpinner = document.getElementById('btn-spinner');
  const errorMsg = document.getElementById('error-msg');

  // Result elements
  // Result elements
  const resultContainer = document.getElementById('result-container');
  const pointsValue = document.getElementById('points-value');
  // const modelValue = document.getElementById('model-value'); // Removed as not in HTML
  const confidenceBadge = document.getElementById('confidence-badge');

  // Feedback & History
  const feedbackButtonsContainer = document.getElementById('feedback-buttons');
  const historyList = document.getElementById('history-list');

  let currentPredictionId = null;
  let currentStory = "";

  const AGILE_POINTS = [1, 2, 3, 5, 8, 13];

  // Load history on start
  loadHistory();

  // Example Chips Logic
  const exampleChips = document.querySelectorAll('.example-chip');
  exampleChips.forEach(chip => {
    chip.addEventListener('click', () => {
      userStoryInput.value = chip.dataset.story;
      userStoryInput.focus();
      // Optional highlight effect
      userStoryInput.style.borderColor = 'var(--color-accent)';
      setTimeout(() => userStoryInput.style.borderColor = '', 300);
    });
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const story = userStoryInput.value.trim();
    if (!story) return;

    currentStory = story;

    // Reset UI
    errorMsg.style.display = 'none';
    resultContainer.style.display = 'none';
    setLoading(true);

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_story: story }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to get prediction');
      }

      const data = await response.json();
      currentPredictionId = data.id;
      displayResult(data);
      generateFeedbackButtons(data.predicted_story_points);

      // Refresh history
      loadHistory();

    } catch (error) {
      console.error(error);
      errorMsg.textContent = error.message || 'An error occurred. Please try again.';
      errorMsg.style.display = 'block';
    } finally {
      setLoading(false);
    }
  });

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    if (isLoading) {
      btnText.style.display = 'none';
      btnSpinner.style.display = 'inline-block';
    } else {
      btnText.style.display = 'inline-block';
      btnSpinner.style.display = 'none';
    }
  }

  function displayResult(data) {
    pointsValue.textContent = data.predicted_story_points;
    // modelValue.textContent = data.model_used;

    // Confidence
    confidenceBadge.textContent = data.confidence + ' Confidence';
    confidenceBadge.className = 'confidence-badge'; // reset
    confidenceBadge.classList.add(`confidence-${data.confidence.toLowerCase()}`);

    resultContainer.style.display = 'block';
    // smooth scroll to results
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function generateFeedbackButtons(predictedPoint) {
    feedbackButtonsContainer.innerHTML = '';

    AGILE_POINTS.forEach(point => {
      const btn = document.createElement('button');
      btn.className = 'btn-feedback';
      btn.textContent = point;

      if (point === predictedPoint) {
        btn.classList.add('active');
      }

      btn.onclick = () => sendFeedback(point, btn);
      feedbackButtonsContainer.appendChild(btn);
    });
  }

  async function sendFeedback(actualPoints, btnElement) {
    if (!currentPredictionId) return;

    // UI feedback
    const allBtns = feedbackButtonsContainer.querySelectorAll('.btn-feedback');
    allBtns.forEach(b => b.classList.remove('active'));
    btnElement.classList.add('active');

    try {
      await fetch('/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prediction_id: currentPredictionId,
          user_story: currentStory,
          actual_points: actualPoints
        })
      });
      console.log('Feedback sent');
    } catch (e) {
      console.error('Failed to send feedback', e);
    }
  }

  async function loadHistory() {
    try {
      const res = await fetch('/history');
      const data = await res.json();

      historyList.innerHTML = '';

      if (data.length === 0) {
        historyList.innerHTML = '<p style="text-align:center; color: #94a3b8;">No recent history.</p>';
        return;
      }

      data.forEach(item => {
        const el = document.createElement('div');
        el.className = 'history-item';
        el.innerHTML = `
                    <div class="history-story" title="${item.user_story}">${item.user_story}</div>
                    <div class="history-points">${item.predicted_points}</div>
                `;
        historyList.appendChild(el);
      });
    } catch (e) {
      console.error("Failed to load history", e);
    }
  }

  // Clear History Logic
  const clearHistoryBtn = document.getElementById('clear-history-btn');
  if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener('click', async () => {
      if (!confirm('Are you sure you want to clear the history?')) return;

      try {
        await fetch('/history', { method: 'DELETE' });
        loadHistory();
      } catch (e) {
        console.error("Failed to clear history", e);
      }
    });
  }
});
