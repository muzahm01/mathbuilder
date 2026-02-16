import Phaser from 'phaser';
import { TILE_SIZE, gridToPixel } from '../systems/GridSystem.js';
import { FXManager } from '../systems/FXManager.js';

export default class Player extends Phaser.Physics.Arcade.Sprite {
  constructor(scene, gridX, gridY) {
    const { x, y } = gridToPixel(gridX, gridY);
    super(scene, x + TILE_SIZE / 2, y + TILE_SIZE / 2, 'botty-idle');

    scene.add.existing(this);
    scene.physics.add.existing(this);

    // Physics body setup
    this.setCollideWorldBounds(false); // Allow falling off-screen (death)
    this.setBounce(0.1);
    this.body.setSize(TILE_SIZE - 8, TILE_SIZE - 4);
    this.body.setOffset(4, 4);

    // 3D effects: shadow for depth + subtle glow highlight
    FXManager.addShadow(this, { x: 3, y: 4, intensity: 0.5 });
    FXManager.addGlow(this, { color: 0x66ccff, outerStrength: 1.5, quality: 0.1, distance: 8 });

    // Movement constants
    this.MOVE_SPEED = 200;
    this.JUMP_VELOCITY = -450;

    // Input
    this.cursors = scene.input.keyboard.createCursorKeys();

    // Reference to touch controls (set from GameScene if available)
    this.touchControls = null;
  }

  update() {
    // Skip movement when physics is paused
    if (this.scene.physics.world.isPaused) return;

    const moveLeft = this.cursors.left.isDown ||
      (this.touchControls && this.touchControls.left);
    const moveRight = this.cursors.right.isDown ||
      (this.touchControls && this.touchControls.right);
    const doJump = this.cursors.up.isDown ||
      (this.touchControls && this.touchControls.jump);

    // Horizontal movement
    if (moveLeft) {
      this.setVelocityX(-this.MOVE_SPEED);
      this.setFlipX(true);
    } else if (moveRight) {
      this.setVelocityX(this.MOVE_SPEED);
      this.setFlipX(false);
    } else {
      this.setVelocityX(0);
    }

    // Jumping (only when on the ground)
    if (doJump && this.body.blocked.down) {
      this.setVelocityY(this.JUMP_VELOCITY);
      this.scene.sound.play('sfx-jump', { volume: 0.5 });
    }

    // Animation state
    if (!this.body.blocked.down) {
      this.anims.play('botty-jump', true);
    } else if (Math.abs(this.body.velocity.x) > 10) {
      this.anims.play('botty-walk', true);
    } else {
      this.anims.play('botty-idle', true);
    }
  }
}
