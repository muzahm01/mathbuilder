import Phaser from 'phaser';
import { ParticleManager } from '../systems/ParticleManager.js';

export default class LevelCompleteScene extends Phaser.Scene {
  constructor() {
    super('LevelComplete');
  }

  init(data) {
    this.levelNumber = data.levelNumber;
    this.stars = data.stars;
    this.xpEarned = data.xpEarned;
    this.totalXP = data.totalXP;
    this.title = data.title;
  }

  create() {
    const { width, height } = this.scale;

    // ── Fade in ──────────────────────────────────────
    this.cameras.main.fadeIn(300, 0, 0, 0);

    // ── Background ─────────────────────────────────
    this.add.image(width / 2, height / 2, 'sky');

    // ── Semi-transparent overlay ────────────────────
    this.add.rectangle(width / 2, height / 2, width, height, 0x000000, 0.4);

    // ── Header ─────────────────────────────────────
    const header = this.add.text(width / 2, 100, 'Level Complete!', {
      fontSize: '42px',
      fontFamily: 'Fredoka One',
      color: '#f1c40f',
      stroke: '#2c3e50',
      strokeThickness: 6
    }).setOrigin(0.5).setScale(0);

    this.tweens.add({
      targets: header,
      scale: 1,
      duration: 400,
      ease: 'Back.easeOut'
    });

    // ── Stars (animate in sequentially) ─────────────
    const starY = 220;
    const starSpacing = 80;
    const starStartX = width / 2 - starSpacing;

    for (let i = 0; i < 3; i++) {
      const isFilled = i < this.stars;
      const starKey = isFilled ? 'star-filled' : 'star-empty';

      const star = this.add.image(
        starStartX + i * starSpacing,
        starY,
        starKey
      ).setScale(0);

      this.tweens.add({
        targets: star,
        scale: 2.5,
        duration: 400,
        delay: 500 + i * 300,
        ease: 'Back.easeOut',
        onComplete: () => {
          if (isFilled) {
            ParticleManager.sparkle(this, star.x, star.y);
          }
        }
      });
    }

    // ── Confetti after stars finish animating ─────────
    this.time.delayedCall(1500, () => {
      ParticleManager.confetti(this);
    });

    // ── XP Earned ──────────────────────────────────
    const xpText = this.add.text(width / 2, 320, `+${this.xpEarned} XP`, {
      fontSize: '28px',
      fontFamily: 'Fredoka One',
      color: '#27ae60'
    }).setOrigin(0.5).setAlpha(0);

    this.tweens.add({
      targets: xpText,
      alpha: 1,
      y: xpText.y - 10,
      duration: 400,
      delay: 1800
    });

    // ── Title Display ──────────────────────────────
    const titleText = this.add.text(width / 2, 370, `Rank: ${this.title}`, {
      fontSize: '22px',
      fontFamily: 'Fredoka One',
      color: '#f39c12'
    }).setOrigin(0.5).setAlpha(0);

    this.tweens.add({
      targets: titleText,
      alpha: 1,
      duration: 400,
      delay: 2100
    });

    // ── Buttons (appear after animations) ───────────
    const btnDelay = 2500;

    // Next Level button
    if (this.levelNumber < 10) {
      const nextBtnBg = this.add.rectangle(width / 2, 460, 240, 50, 0x27ae60)
        .setStrokeStyle(3, 0x1e8449)
        .setAlpha(0)
        .setInteractive({ useHandCursor: true });

      const nextBtnText = this.add.text(width / 2, 460, 'Next Level >', {
        fontSize: '26px',
        fontFamily: 'Fredoka One',
        color: '#ffffff'
      }).setOrigin(0.5).setAlpha(0);

      this.tweens.add({
        targets: [nextBtnBg, nextBtnText],
        alpha: 1,
        duration: 300,
        delay: btnDelay
      });

      nextBtnBg.on('pointerover', () => {
        nextBtnBg.setScale(1.1);
        nextBtnText.setScale(1.1);
      });
      nextBtnBg.on('pointerout', () => {
        nextBtnBg.setScale(1);
        nextBtnText.setScale(1);
      });
      nextBtnBg.on('pointerdown', () => {
        this.scene.start('Game', { levelNumber: this.levelNumber + 1 });
      });
    }

    // Level Select button
    const selectBtnBg = this.add.rectangle(width / 2, 520, 200, 40, 0x34495e)
      .setStrokeStyle(2, 0x2c3e50)
      .setAlpha(0)
      .setInteractive({ useHandCursor: true });

    const selectBtnText = this.add.text(width / 2, 520, 'Level Select', {
      fontSize: '20px',
      fontFamily: 'Fredoka One',
      color: '#bdc3c7'
    }).setOrigin(0.5).setAlpha(0);

    this.tweens.add({
      targets: [selectBtnBg, selectBtnText],
      alpha: 1,
      duration: 300,
      delay: btnDelay + 200
    });

    selectBtnBg.on('pointerover', () => {
      selectBtnBg.setScale(1.1);
      selectBtnText.setScale(1.1);
    });
    selectBtnBg.on('pointerout', () => {
      selectBtnBg.setScale(1);
      selectBtnText.setScale(1);
    });
    selectBtnBg.on('pointerdown', () => {
      this.scene.start('LevelSelect');
    });
  }
}
