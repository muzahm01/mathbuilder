import Phaser from 'phaser';
import { TILE_SIZE, gridToPixel } from '../systems/GridSystem.js';

export default class GoalFlag extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, gridX, gridY) {
    const { x, y } = gridToPixel(gridX, gridY);

    super(scene, x + TILE_SIZE / 2, y + TILE_SIZE / 2, 'flag');

    scene.add.existing(this);
    scene.physics.add.existing(this, true); // Static body

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
