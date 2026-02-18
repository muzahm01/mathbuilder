import { describe, it, expect } from 'vitest';
import { validateLevel } from '../src/game/systems/LevelValidator.js';

const VALID_LEVEL = {
  name: 'Test Level',
  gridWidth: 25,
  gridHeight: 9,
  platforms: [
    { gridX: 0, gridY: 8, width: 5, tile: 'grass-top' },
    { gridX: 8, gridY: 8, width: 7, tile: 'grass-top' }
  ],
  gaps: [
    { gridX: 5, gridY: 8, width: 3, correctAnswer: 3 }
  ],
  start: { gridX: 1, gridY: 7 },
  goal: { gridX: 14, gridY: 7 }
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

  describe('gridWidth validation', () => {
    it('rejects missing gridWidth', () => {
      const level = { ...VALID_LEVEL };
      delete level.gridWidth;
      const result = validateLevel(level);
      expect(result.valid).toBe(false);
    });

    it('rejects non-integer gridWidth', () => {
      const result = validateLevel({ ...VALID_LEVEL, gridWidth: 15.5 });
      expect(result.valid).toBe(false);
    });

    it('rejects zero gridWidth', () => {
      const result = validateLevel({ ...VALID_LEVEL, gridWidth: 0 });
      expect(result.valid).toBe(false);
    });
  });

  describe('gridHeight validation', () => {
    it('rejects missing gridHeight', () => {
      const level = { ...VALID_LEVEL };
      delete level.gridHeight;
      const result = validateLevel(level);
      expect(result.valid).toBe(false);
    });

    it('rejects non-integer gridHeight', () => {
      const result = validateLevel({ ...VALID_LEVEL, gridHeight: 9.5 });
      expect(result.valid).toBe(false);
    });
  });

  describe('platforms validation', () => {
    it('rejects empty platforms array', () => {
      const result = validateLevel({ ...VALID_LEVEL, platforms: [] });
      expect(result.valid).toBe(false);
    });

    it('rejects platform with missing gridX', () => {
      const result = validateLevel({
        ...VALID_LEVEL,
        platforms: [{ gridY: 8, width: 5, tile: 'grass-top' }]
      });
      expect(result.valid).toBe(false);
    });

    it('rejects platform with missing tile', () => {
      const result = validateLevel({
        ...VALID_LEVEL,
        platforms: [{ gridX: 0, gridY: 8, width: 5 }]
      });
      expect(result.valid).toBe(false);
    });
  });

  describe('gaps validation', () => {
    it('accepts level with no gaps', () => {
      const result = validateLevel({ ...VALID_LEVEL, gaps: [] });
      expect(result.valid).toBe(true);
    });

    it('rejects gap with mismatched correctAnswer and width', () => {
      const result = validateLevel({
        ...VALID_LEVEL,
        gaps: [{ gridX: 5, gridY: 8, width: 3, correctAnswer: 5 }]
      });
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.includes('does not match'))).toBe(true);
    });

    it('rejects gap with zero width', () => {
      const result = validateLevel({
        ...VALID_LEVEL,
        gaps: [{ gridX: 5, gridY: 8, width: 0, correctAnswer: 0 }]
      });
      expect(result.valid).toBe(false);
    });
  });

  describe('start/goal validation', () => {
    it('rejects missing start', () => {
      const level = { ...VALID_LEVEL };
      delete level.start;
      const result = validateLevel(level);
      expect(result.valid).toBe(false);
    });

    it('rejects missing goal', () => {
      const level = { ...VALID_LEVEL };
      delete level.goal;
      const result = validateLevel(level);
      expect(result.valid).toBe(false);
    });

    it('rejects goal to the left of start', () => {
      const result = validateLevel({
        ...VALID_LEVEL,
        start: { gridX: 10, gridY: 7 },
        goal: { gridX: 5, gridY: 7 }
      });
      expect(result.valid).toBe(false);
      expect(result.errors.some(e => e.includes('Goal gridX'))).toBe(true);
    });
  });
});
