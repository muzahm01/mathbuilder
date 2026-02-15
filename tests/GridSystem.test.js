import { describe, it, expect } from 'vitest';
import {
  TILE_SIZE,
  tileToPixel,
  pixelToTile,
  tileToPixelCenter,
  snapToGrid
} from '../src/game/systems/GridSystem.js';

describe('GridSystem', () => {
  describe('TILE_SIZE', () => {
    it('should be 64', () => {
      expect(TILE_SIZE).toBe(64);
    });
  });

  describe('tileToPixel', () => {
    it('converts tile 0 to pixel 0', () => {
      expect(tileToPixel(0)).toBe(0);
    });

    it('converts tile 1 to pixel 64', () => {
      expect(tileToPixel(1)).toBe(64);
    });

    it('converts tile 5 to pixel 320', () => {
      expect(tileToPixel(5)).toBe(320);
    });
  });

  describe('pixelToTile', () => {
    it('converts pixel 0 to tile 0', () => {
      expect(pixelToTile(0)).toBe(0);
    });

    it('converts pixel 64 to tile 1', () => {
      expect(pixelToTile(64)).toBe(1);
    });

    it('floors mid-tile pixel values', () => {
      expect(pixelToTile(100)).toBe(1); // 100/64 = 1.5625 -> floor to 1
    });

    it('converts pixel 63 to tile 0', () => {
      expect(pixelToTile(63)).toBe(0);
    });
  });

  describe('tileToPixelCenter', () => {
    it('returns center of tile 0 at pixel 32', () => {
      expect(tileToPixelCenter(0)).toBe(32);
    });

    it('returns center of tile 1 at pixel 96', () => {
      expect(tileToPixelCenter(1)).toBe(96);
    });
  });

  describe('snapToGrid', () => {
    it('snaps pixel 100 to pixel 64 (tile 1 boundary)', () => {
      expect(snapToGrid(100)).toBe(64);
    });

    it('snaps pixel 0 to pixel 0', () => {
      expect(snapToGrid(0)).toBe(0);
    });

    it('snaps pixel 63 to pixel 0', () => {
      expect(snapToGrid(63)).toBe(0);
    });

    it('snaps pixel 128 to pixel 128 (exact boundary)', () => {
      expect(snapToGrid(128)).toBe(128);
    });
  });
});
