export class TouchControls {
  constructor(scene) {
    this.left = false;
    this.right = false;
    this.jump = false;

    // Only show on touch devices
    if (!scene.sys.game.device.input.touch) return;

    this.createButton(scene, 80, 520, 'arrow-left', 'left');
    this.createButton(scene, 180, 520, 'arrow-right', 'right');
    this.createButton(scene, 720, 520, 'arrow-jump', 'jump');
  }

  createButton(scene, x, y, textureKey, direction) {
    const btn = scene.add.image(x, y, textureKey)
      .setScrollFactor(0)      // Stay fixed on screen
      .setAlpha(0.4)           // Semi-transparent
      .setInteractive()
      .setDepth(1000);         // Always on top

    // Handle multi-touch correctly
    btn.on('pointerdown', () => {
      this[direction] = true;
      btn.setAlpha(0.7);       // Visual press feedback
    });
    btn.on('pointerup', () => {
      this[direction] = false;
      btn.setAlpha(0.4);
    });
    btn.on('pointerout', () => {
      this[direction] = false;
      btn.setAlpha(0.4);
    });
  }
}
