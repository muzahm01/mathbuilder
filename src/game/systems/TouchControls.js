import Phaser from 'phaser';

export class TouchControls {
  constructor(scene) {
    this.left = false;
    this.right = false;
    this.jump = false;

    // Only show on touch devices
    if (!scene.sys.game.device.input.touch) return;

    const { width, height } = scene.scale;
    const btnY = height - 80;
    const padding = 70;

    this.createButton(scene, padding, btnY, 'arrow-left', 'left');
    this.createButton(scene, padding + 100, btnY, 'arrow-right', 'right');
    this.createButton(scene, width - padding, btnY, 'arrow-jump', 'jump');
  }

  createButton(scene, x, y, textureKey, direction) {
    const btn = scene.add.image(x, y, textureKey)
      .setScrollFactor(0)
      .setAlpha(0.4)
      .setDepth(1000)
      .setScale(1.2);

    // Use a larger hit area for small fingers (children aged 5-8)
    const hitPadding = 16;
    btn.setInteractive({
      hitArea: new Phaser.Geom.Rectangle(
        -hitPadding, -hitPadding,
        btn.width + hitPadding * 2,
        btn.height + hitPadding * 2
      ),
      hitAreaCallback: Phaser.Geom.Rectangle.Contains
    });

    // Handle multi-touch correctly
    btn.on('pointerdown', () => {
      this[direction] = true;
      btn.setAlpha(0.7);
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
