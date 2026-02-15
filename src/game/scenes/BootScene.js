import Phaser from 'phaser';

export default class BootScene extends Phaser.Scene {
  constructor() {
    super('Boot');
  }

  create() {
    this.add.text(
      this.scale.width / 2,
      this.scale.height / 2,
      'MathBuilder',
      {
        fontSize: '48px',
        fontFamily: 'Fredoka One',
        color: '#ffffff',
        stroke: '#2c3e50',
        strokeThickness: 6
      }
    ).setOrigin(0.5);
  }
}
