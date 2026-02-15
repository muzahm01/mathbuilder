import { TILE_SIZE, gridToPixel } from '../systems/GridSystem.js';

/**
 * Build a bridge of N blocks at the gap position.
 * Blocks are added to the existing platform static group.
 */
export function buildBridge(scene, gapData, platformGroup) {
  const { x: baseX, y: baseY } = gridToPixel(gapData.gridX, gapData.gridY);

  for (let i = 0; i < gapData.width; i++) {
    const block = platformGroup.create(
      baseX + i * TILE_SIZE + TILE_SIZE / 2,
      baseY + TILE_SIZE / 2,
      'bridge-block'
    );
    block.setSize(TILE_SIZE, TILE_SIZE);
    block.refreshBody();

    // Pop-in animation for each block
    block.setScale(0);
    scene.tweens.add({
      targets: block,
      scale: 1,
      duration: 200,
      delay: i * 80,
      ease: 'Back.easeOut'
    });
  }
}
