/**
 * Adds a fullscreen toggle button to a Phaser scene.
 * Draws a universally recognizable four-corners icon using Graphics.
 */
export function addFullscreenButton(scene, x = 40, y = 30) {
  const size = 28;
  const half = size / 2;
  const corner = 7;
  const lineWidth = 2.5;

  // Background circle for touch target
  const hitArea = scene.add.circle(x, y, 20, 0x000000, 0.3)
    .setScrollFactor(0)
    .setDepth(1001)
    .setInteractive({ useHandCursor: true });

  // Icon drawn with graphics
  const gfx = scene.add.graphics()
    .setScrollFactor(0)
    .setDepth(1002);

  function drawIcon() {
    gfx.clear();
    gfx.lineStyle(lineWidth, 0xffffff, 0.9);

    const isFullscreen = scene.scale.isFullscreen;

    if (!isFullscreen) {
      // Expand icon: four outward-pointing corners
      // Top-left
      gfx.moveTo(x - half + corner, y - half);
      gfx.lineTo(x - half, y - half);
      gfx.lineTo(x - half, y - half + corner);
      // Top-right
      gfx.moveTo(x + half - corner, y - half);
      gfx.lineTo(x + half, y - half);
      gfx.lineTo(x + half, y - half + corner);
      // Bottom-left
      gfx.moveTo(x - half, y + half - corner);
      gfx.lineTo(x - half, y + half);
      gfx.lineTo(x - half + corner, y + half);
      // Bottom-right
      gfx.moveTo(x + half, y + half - corner);
      gfx.lineTo(x + half, y + half);
      gfx.lineTo(x + half - corner, y + half);
    } else {
      // Collapse icon: four inward-pointing corners
      const inset = 4;
      // Top-left
      gfx.moveTo(x - half + inset + corner, y - half + inset);
      gfx.lineTo(x - half + inset, y - half + inset);
      gfx.lineTo(x - half + inset, y - half + inset + corner);
      // Top-right
      gfx.moveTo(x + half - inset - corner, y - half + inset);
      gfx.lineTo(x + half - inset, y - half + inset);
      gfx.lineTo(x + half - inset, y - half + inset + corner);
      // Bottom-left
      gfx.moveTo(x - half + inset, y + half - inset - corner);
      gfx.lineTo(x - half + inset, y + half - inset);
      gfx.lineTo(x - half + inset + corner, y + half - inset);
      // Bottom-right
      gfx.moveTo(x + half - inset, y + half - inset - corner);
      gfx.lineTo(x + half - inset, y + half - inset);
      gfx.lineTo(x + half - inset - corner, y + half - inset);
    }

    gfx.strokePath();
  }

  drawIcon();

  hitArea.on('pointerdown', () => {
    if (scene.scale.isFullscreen) {
      scene.scale.stopFullscreen();
    } else {
      scene.scale.startFullscreen();
    }
  });

  hitArea.on('pointerover', () => hitArea.setAlpha(1));
  hitArea.on('pointerout', () => hitArea.setAlpha(0.7));
  hitArea.setAlpha(0.7);

  // Redraw icon when fullscreen state changes
  scene.scale.on('enterfullscreen', drawIcon);
  scene.scale.on('leavefullscreen', drawIcon);

  // Clean up listeners when scene shuts down
  scene.events.on('shutdown', () => {
    scene.scale.off('enterfullscreen', drawIcon);
    scene.scale.off('leavefullscreen', drawIcon);
  });

  return { hitArea, gfx };
}
