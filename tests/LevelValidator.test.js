import { describe, it, expect } from 'vitest';
import { validateLevel } from '../src/game/systems/LevelValidator.js';

const VALID_LEVEL = {
  name: 'Test Level',
  width: 15,
  platforms: [
    { x: 0, y: 8, width: 5, tile: 'grass-top' },
    { x: 8, y: 8, width: 7, tile: 'grass-top' }
  ],
  gaps: [
    { x: 5, y: 8, width: 3, answer: 3 }
  ],
  player: { x: 1, y: 7 },
  goal: { x: 14, y: 7 }
};

describe('LevelValidator', () => {
  it('accepts a valid level', () => {
    const result = validateLevel(VALID_LEVEL);
    expect(result.valid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  it('rejects null input', () => {
    const result = validateLevel(null);
    expect(result.valid).toBe(false);
  });

  it('rejects non-object input', () => {
    const result = validateLevel('not an object');
    expect(result.valid).toBe(false);
  });

  describe('name validation', () => {
    it('rejects missing name', () => {
      const level = { ...VALID_LEVEL };
      delete level.name;
      const result = validateLevel(level);
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.includes('name'))).toBe(true);
    });

    it('rejects empty name', () => {
      const result = validateLevel({ ...VALID_LEVEL, name: '' });
      expect(result.valid).toBe(false);
    });
  });

  describe('width validation', () => {
    it('rejects missing width', () => {
      const level = { ...VALID_LEVEL };
      delete level.width;
      const result = validateLevel(level);
      expect(result.valid).toBe(false);
    });

    it('rejects non-integer width', () => {
      const result = validateLevel({ ...VALID_LEVEL, width: 15.5 });
      expect(result.valid).toBe(false);
    });

    it('rejects zero width', () => {
      const result = validateLevel({ ...VALID_LEVEL, width: 0 });
      expect(result.valid).toBe(false);
    });
  });

  describe('platforms validation', () => {
    it('rejects empty platforms array', () => {
      const result = validateLevel({ ...VALID_LEVEL, platforms: [] });
      expect(result.valid).toBe(false);
    });

    it('rejects platform with missing x', () => {
      const result = validateLevel({
        ...VALID_LEVEL,
        platforms: [{ y: 8, width: 5, tile: 'grass-top' }]
      });
      expect(result.valid).toBe(false);
    });

    it('rejects platform with missing tile', () => {
      const result = validateLevel({
        ...VALID_LEVEL,
        platforms: [{ x: 0, y: 8, width: 5 }]
      });
      expect(result.valid).toBe(false);
    });
  });

  describe('gaps validation', () => {
    it('accepts level with no gaps', () => {
      const result = validateLevel({ ...VALID_LEVEL, gaps: [] });
      expect(result.valid).toBe(true);
    });

    it('rejects gap with mismatched answer and width', () => {
      const result = validateLevel({
        ...VALID_LEVEL,
        gaps: [{ x: 5, y: 8, width: 3, answer: 5 }]
      });
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.includes('does not match'))).toBe(true);
    });

    it('rejects gap with zero width', () => {
      const result = validateLevel({
        ...VALID_LEVEL,
        gaps: [{ x: 5, y: 8, width: 0, answer: 0 }]
      });
      expect(result.valid).toBe(false);
    });
  });

  describe('player/goal validation', () => {
    it('rejects missing player', () => {
      const level = { ...VALID_LEVEL };
      delete level.player;
      const result = validateLevel(level);
      expect(result.valid).toBe(false);
    });

    it('rejects missing goal', () => {
      const level = { ...VALID_LEVEL };
      delete level.goal;
      const result = validateLevel(level);
      expect(result.valid).toBe(false);
    });

    it('rejects goal to the left of player', () => {
      const result = validateLevel({
        ...VALID_LEVEL,
        player: { x: 10, y: 7 },
        goal: { x: 5, y: 7 }
      });
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.includes('Goal x'))).toBe(true);
    });
  });
});
