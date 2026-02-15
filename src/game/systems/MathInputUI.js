export class MathInputUI {
  /**
   * @param {Function} onResult - Called with (gapData, isCorrect) on each submission
   */
  constructor(onResult) {
    this.overlay = document.getElementById('math-input-overlay');
    this.input = document.getElementById('math-answer-input');
    this.feedback = document.getElementById('math-feedback');
    this.submitBtn = document.getElementById('math-submit-btn');
    this.onResult = onResult;
    this.currentGap = null;

    // Bind event listeners
    this.submitBtn.addEventListener('click', () => this.handleSubmit());
    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') this.handleSubmit();
    });
  }

  /**
   * Show the math input overlay for a specific gap.
   */
  show(gapData) {
    this.currentGap = gapData;
    this.input.value = '';
    this.feedback.textContent = '';
    this.feedback.style.color = '';
    this.overlay.style.display = 'flex';

    // Focus the input after a short delay (allows overlay to render)
    setTimeout(() => this.input.focus(), 100);
  }

  /**
   * Hide the math input overlay.
   */
  hide() {
    this.overlay.style.display = 'none';
    this.currentGap = null;
  }

  /**
   * Process the player's answer.
   */
  handleSubmit() {
    if (!this.currentGap) return;

    const answer = parseInt(this.input.value, 10);

    // Ignore empty or non-numeric input
    if (isNaN(answer) || answer < 1) {
      this.input.value = '';
      return;
    }

    const correct = this.currentGap.correctAnswer;

    if (answer === correct) {
      this.feedback.textContent = 'Correct!';
      this.feedback.style.color = '#27ae60';
      this.onResult(this.currentGap, true);

      // Brief pause to show "Correct!" then hide
      setTimeout(() => this.hide(), 600);

    } else if (answer < correct) {
      this.feedback.textContent = 'Too Short! Try again.';
      this.feedback.style.color = '#e74c3c';
      this.input.value = '';
      this.input.focus();
      this.onResult(this.currentGap, false);

    } else {
      this.feedback.textContent = 'Too Long! Try again.';
      this.feedback.style.color = '#e74c3c';
      this.input.value = '';
      this.input.focus();
      this.onResult(this.currentGap, false);
    }
  }
}
