import Phaser from 'phaser';
import { loadSave } from '../systems/SaveManager.js';
import { getTitleForXP } from '../systems/TitleSystem.js';

export default class MenuScene extends Phaser.Scene {
  constructor() {
    super('Menu');
  }

  create() {
    const { width, height } = this.scale;

    // ── Background ─────────────────────────────────
    this.add.image(width / 2, height / 2, 'sky');

    // ── Title ──────────────────────────────────────
    const title = this.add.text(width / 2, 140, 'MathBuilder', {
      fontSize: '56px',
      fontFamily: 'Fredoka One',
      color: '#ffffff',
      stroke: '#2c3e50',
      strokeThickness: 8
    }).setOrigin(0.5);

    // Gentle floating animation
    this.tweens.add({
      targets: title,
      y: title.y - 10,
      duration: 2000,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut'
    });

    // ── Botty (idle animation) ─────────────────────
    const botty = this.add.sprite(width / 2, 280, 'botty-idle');
    botty.play('botty-idle');
    botty.setScale(2);

    // ── Play Button ────────────────────────────────
    const playBtn = this.add.image(width / 2, 420, 'btn-play')
      .setInteractive({ useHandCursor: true });

    playBtn.on('pointerover', () => playBtn.setScale(1.1));
    playBtn.on('pointerout', () => playBtn.setScale(1));
    playBtn.on('pointerdown', () => {
      this.scene.start('LevelSelect');
    });

    // ── Current Rank ───────────────────────────────
    const saveData = loadSave(localStorage);
    const currentTitle = getTitleForXP(saveData.xp);

    this.add.text(width / 2, 520, `Rank: ${currentTitle}`, {
      fontSize: '22px',
      fontFamily: 'Fredoka One',
      color: '#f39c12'
    }).setOrigin(0.5);

    this.add.text(width / 2, 555, `${saveData.xp} XP`, {
      fontSize: '16px',
      fontFamily: 'Fredoka One',
      color: '#bdc3c7'
    }).setOrigin(0.5);

    // ── Mute Button ──────────────────────────────
    let muted = this.sound.mute;
    const muteBtn = this.add.text(760, 30, muted ? '🔇' : '🔊', {
      fontSize: '24px'
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });

    muteBtn.on('pointerdown', () => {
      muted = !muted;
      this.sound.mute = muted;
      muteBtn.setText(muted ? '🔇' : '🔊');
    });
  }
}
