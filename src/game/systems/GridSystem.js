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

const GridSystem = {
  TILE_SIZE,
  tileToPixel,
  pixelToTile,
  tileToPixelCenter,
  snapToGrid
};

export default GridSystem;
