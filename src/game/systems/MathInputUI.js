export class MathInputUI {
  /**
   * @param {Function} onResult - Called with (gapData, isCorrect) on each submission
   */
  constructor(onResult) {
    this.overlay = document.getElementById('math-input-overlay');
    this.panel = document.getElementById('math-input-panel');
    this.input = document.getElementById('math-answer-input');
    this.feedback = document.getElementById('math-feedback');
    this.submitBtn = document.getElementById('math-submit-btn');
    this.onResult = onResult;
    this.currentGap = null;

    // Named handlers so they can be removed on destroy()
    this._onSubmitClick = () => this.handleSubmit();
    this._onKeydown = (e) => { if (e.key === 'Enter') this.handleSubmit(); };
    this._onPointerDown = (e) => e.stopPropagation();

    this.submitBtn.addEventListener('click', this._onSubmitClick);
    this.input.addEventListener('keydown', this._onKeydown);
    this.overlay.addEventListener('pointerdown', this._onPointerDown);
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

    // Re-trigger the pop-in animation
    this.panel.style.animation = 'none';
    void this.panel.offsetHeight;
    this.panel.style.animation = '';

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
   * Remove all event listeners. Call when the owning scene shuts down
   * to prevent listener accumulation across level transitions.
   */
  destroy() {
    this.hide();
    this.submitBtn.removeEventListener('click', this._onSubmitClick);
    this.input.removeEventListener('keydown', this._onKeydown);
    this.overlay.removeEventListener('pointerdown', this._onPointerDown);
  }

  /**
   * Shake the panel briefly for wrong-answer feedback.
   */
  shakePanel() {
    this.panel.style.animation = 'none';
    void this.panel.offsetHeight;
    this.panel.style.animation = 'shake 0.3s ease-out';
  }

  /**
   * Process the player's answer.
   */
  handleSubmit() {
    if (!this.currentGap) return;

    // Sanitize: trim whitespace, limit length to prevent abuse
    const raw = this.input.value.trim().slice(0, 4);
    const answer = parseInt(raw, 10);

    // Ignore empty, non-numeric, or out-of-range input
    if (isNaN(answer) || answer < 1 || answer > 20) {
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
      this.feedback.textContent = 'Too small! Try again.';
      this.feedback.style.color = '#e74c3c';
      this.input.value = '';
      this.input.focus();
      this.shakePanel();
      this.onResult(this.currentGap, false);

    } else {
      this.feedback.textContent = 'Too big! Try again.';
      this.feedback.style.color = '#e74c3c';
      this.input.value = '';
      this.input.focus();
      this.shakePanel();
      this.onResult(this.currentGap, false);
    }
  }
}
