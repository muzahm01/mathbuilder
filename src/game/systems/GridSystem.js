/**
 * Grid system for converting between tile and pixel coordinates.
 * All game positions are based on a 64x64 tile grid.
 */

export const TILE_SIZE = 64;

export function tileToPixel(tileCoord) {
  return tileCoord * TILE_SIZE;
}

export function pixelToTile(pixelCoord) {
  return Math.floor(pixelCoord / TILE_SIZE);
}

export function tileToPixelCenter(tileCoord) {
  return tileCoord * TILE_SIZE + TILE_SIZE / 2;
}

export function snapToGrid(pixelCoord) {
  return pixelToTile(pixelCoord) * TILE_SIZE;
}

/**
 * Convert grid coordinates to pixel coordinates (top-left of the tile).
 */
export function gridToPixel(gridX, gridY) {
  return {
    x: gridX * TILE_SIZE,
    y: gridY * TILE_SIZE
  };
}

/**
 * Draw a debug grid overlay.
 */
export function drawDebugGrid(scene, widthInTiles, heightInTiles) {
  const graphics = scene.add.graphics();
  graphics.lineStyle(1, 0xffffff, 0.15);

  for (let x = 0; x <= widthInTiles; x++) {
    graphics.moveTo(x * TILE_SIZE, 0);
    graphics.lineTo(x * TILE_SIZE, heightInTiles * TILE_SIZE);
  }
  for (let y = 0; y <= heightInTiles; y++) {
    graphics.moveTo(0, y * TILE_SIZE);
    graphics.lineTo(widthInTiles * TILE_SIZE, y * TILE_SIZE);
  }

  graphics.strokePath();
  graphics.setDepth(1000);
  return graphics;
}

const GridSystem = {
  TILE_SIZE,
  tileToPixel,
  pixelToTile,
  tileToPixelCenter,
  snapToGrid,
  gridToPixel,
  drawDebugGrid
};

export default GridSystem;
