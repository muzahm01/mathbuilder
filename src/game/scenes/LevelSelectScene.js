import Phaser from 'phaser';
import { loadSave } from '../systems/SaveManager.js';

export default class LevelSelectScene extends Phaser.Scene {
  constructor() {
    super('LevelSelect');
  }

  create() {
    const { width, height } = this.scale;
    const saveData = loadSave(localStorage);

    // ── Background ─────────────────────────────────
    this.add.image(width / 2, height / 2, 'sky');

    // ── Header ─────────────────────────────────────
    this.add.text(width / 2, 50, 'World 1: Grasslands', {
      fontSize: '32px',
      fontFamily: 'Fredoka One',
      color: '#ffffff',
      stroke: '#2c3e50',
      strokeThickness: 4
    }).setOrigin(0.5);

    // ── Level Grid (5 columns x 2 rows) ────────────
    const startX = 120;
    const startY = 140;
    const spacingX = 140;
    const spacingY = 200;

    for (let i = 0; i < 10; i++) {
      const col = i % 5;
      const row = Math.floor(i / 5);
      const x = startX + col * spacingX;
      const y = startY + row * spacingY;
      const levelNum = i + 1;
      const isUnlocked = levelNum <= saveData.levelsUnlocked;
      const levelKey = `level${levelNum}`;
      const stars = saveData.levelStars[levelKey] || 0;

      this.createLevelButton(x, y, levelNum, isUnlocked, stars);
    }

    // ── Back Button ────────────────────────────────
    const backText = this.add.text(60, height - 40, '< Back', {
      fontSize: '20px',
      fontFamily: 'Fredoka One',
      color: '#ffffff'
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });

    backText.on('pointerdown', () => this.scene.start('Menu'));
  }

  createLevelButton(x, y, levelNum, isUnlocked, stars) {
    const bg = this.add.rectangle(x, y, 100, 100, isUnlocked ? 0x3498db : 0x7f8c8d)
      .setStrokeStyle(3, isUnlocked ? 0x2980b9 : 0x636e72);

    if (isUnlocked) {
      bg.setInteractive({ useHandCursor: true });

      bg.on('pointerover', () => bg.setScale(1.1));
      bg.on('pointerout', () => bg.setScale(1));
      bg.on('pointerdown', () => {
        this.scene.start('Game', { levelNumber: levelNum });
      });
    }

    // Level Number
    const color = isUnlocked ? '#ffffff' : '#bdc3c7';
    this.add.text(x, y - 10, String(levelNum), {
      fontSize: '36px',
      fontFamily: 'Fredoka One',
      color: color
    }).setOrigin(0.5);

    // Stars
    if (isUnlocked) {
      for (let s = 0; s < 3; s++) {
        const starKey = s < stars ? 'star-filled' : 'star-empty';
        this.add.image(
          x - 24 + s * 24,
          y + 30,
          starKey
        ).setScale(0.7);
      }
    } else {
      this.add.text(x, y + 25, 'LOCKED', {
        fontSize: '12px',
        fontFamily: 'Fredoka One',
        color: '#bdc3c7'
      }).setOrigin(0.5);
    }
  }
}
