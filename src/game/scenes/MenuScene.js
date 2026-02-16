import Phaser from 'phaser';
import { loadSave } from '../systems/SaveManager.js';
import { getTitleForXP } from '../systems/TitleSystem.js';
import { addFullscreenButton } from '../systems/FullscreenButton.js';
import { FXManager } from '../systems/FXManager.js';

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

    // 3D effects on title: shine sweep + golden glow
    FXManager.addShine(title, { speed: 0.3, lineWidth: 0.5, gradient: 3 });
    FXManager.addGlow(title, { color: 0xf39c12, outerStrength: 3, quality: 0.1, distance: 12 });
    FXManager.addShadow(title, { x: 4, y: 4, intensity: 0.5 });

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

    // 3D effects on Botty: shadow + subtle glow
    FXManager.addShadow(botty, { x: 4, y: 5, intensity: 0.5 });
    FXManager.addGlow(botty, { color: 0x66ccff, outerStrength: 2, quality: 0.1, distance: 10 });

    // ── Play Button ────────────────────────────────
    const playBtn = this.add.image(width / 2, 420, 'btn-play')
      .setInteractive({ useHandCursor: true });

    // 3D effects on button: shadow + glow on hover
    FXManager.addShadow(playBtn, { x: 3, y: 3, intensity: 0.5 });
    FXManager.addShine(playBtn, { speed: 0.4, lineWidth: 0.3, gradient: 4 });
    const playGlow = FXManager.addGlow(playBtn, {
      color: 0x27ae60, outerStrength: 0, quality: 0.1, distance: 10
    });

    playBtn.on('pointerover', () => {
      playBtn.setScale(1.1);
      if (playGlow) playGlow.outerStrength = 4;
    });
    playBtn.on('pointerout', () => {
      playBtn.setScale(1);
      if (playGlow) playGlow.outerStrength = 0;
    });
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

    // ── Fullscreen Button ────────────────────────
    addFullscreenButton(this, 40, 30);

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

    // ── Camera bloom for warm overall look ──────────
    FXManager.addCameraBloom(this.cameras.main, { strength: 0.3, blurStrength: 0.8 });
  }
}
