import Phaser from 'phaser';
import { TILE_SIZE, gridToPixel } from '../systems/GridSystem.js';
import { FXManager } from '../systems/FXManager.js';

export default class GoalFlag extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, gridX, gridY) {
    const { x, y } = gridToPixel(gridX, gridY);

    super(scene, x + TILE_SIZE / 2, y + TILE_SIZE / 2, 'flag');

    scene.add.existing(this);
    scene.physics.add.existing(this, true); // Static body

    // 3D effects: pulsing golden glow + shine sweep + shadow
    FXManager.addPulsingGlow(scene, this, {
      color: 0xf1c40f, minStrength: 2, maxStrength: 5, duration: 1200
    });
    FXManager.addShine(this, { speed: 0.4, lineWidth: 0.4, gradient: 3 });
    FXManager.addShadow(this, { x: 2, y: 3, intensity: 0.5 });

    // Gentle floating animation
    scene.tweens.add({
      targets: this,
      y: this.y - 8,
      duration: 1000,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut'
    });
  }
}
