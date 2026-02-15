import { describe, it, expect, beforeEach } from 'vitest';
import {
  loadSave,
  writeSave,
  clearSave,
  calculateStars,
  completeLevelAndSave
} from '../src/game/systems/SaveManager.js';

/**
 * Simple in-memory mock of the Storage interface.
 */
function createMockStorage() {
  const store = {};
  return {
    getItem(key) { return store[key] ?? null; },
    setItem(key, value) { store[key] = String(value); },
    removeItem(key) { delete store[key]; },
    _store: store
  };
}

describe('SaveManager', () => {
  let storage;

  beforeEach(() => {
    storage = createMockStorage();
  });

  describe('calculateStars', () => {
    it('returns 3 stars for 0 wrong answers', () => {
      expect(calculateStars(0)).toBe(3);
    });

    it('returns 2 stars for 1 wrong answer', () => {
      expect(calculateStars(1)).toBe(2);
    });

    it('returns 2 stars for 2 wrong answers', () => {
      expect(calculateStars(2)).toBe(2);
    });

    it('returns 1 star for 3 wrong answers', () => {
      expect(calculateStars(3)).toBe(1);
    });

    it('returns 1 star for many wrong answers (always positive)', () => {
      expect(calculateStars(100)).toBe(1);
    });
  });

  describe('loadSave', () => {
    it('returns default save when no data exists', () => {
      const save = loadSave(storage);
      expect(save).toEqual({
        xp: 0,
        levelsUnlocked: 1,
        levelStars: {},
        totalStars: 0
      });
    });

    it('loads existing save data', () => {
      storage.setItem('mathbuilder_save', JSON.stringify({
        xp: 100,
        levelsUnlocked: 3,
        levelStars: { level1: 3, level2: 2 },
        totalStars: 5
      }));
      const save = loadSave(storage);
      expect(save.xp).toBe(100);
      expect(save.levelsUnlocked).toBe(3);
    });

    it('returns default save for corrupted data', () => {
      storage.setItem('mathbuilder_save', 'not-json{{{');
      const save = loadSave(storage);
      expect(save.xp).toBe(0);
    });
  });

  describe('writeSave / clearSave', () => {
    it('writes and reads back save data', () => {
      const data = { xp: 50, levelsUnlocked: 2, levelStars: { level1: 3 }, totalStars: 3 };
      writeSave(storage, data);
      const loaded = loadSave(storage);
      expect(loaded).toEqual(data);
    });

    it('clears save data', () => {
      writeSave(storage, { xp: 50 });
      clearSave(storage);
      const loaded = loadSave(storage);
      expect(loaded.xp).toBe(0);
    });
  });

  describe('completeLevelAndSave', () => {
    it('saves stars and unlocks next level', () => {
      const { stars, save } = completeLevelAndSave(storage, 1, 0);
      expect(stars).toBe(3);
      expect(save.levelsUnlocked).toBe(2);
      expect(save.levelStars.level1).toBe(3);
      expect(save.xp).toBe(30); // 3 stars * 10 XP
    });

    it('keeps better star score on replay', () => {
      completeLevelAndSave(storage, 1, 0); // 3 stars
      completeLevelAndSave(storage, 1, 5); // 1 star (worse)
      const save = loadSave(storage);
      expect(save.levelStars.level1).toBe(3); // Kept best
    });

    it('upgrades star score on better replay', () => {
      completeLevelAndSave(storage, 1, 5); // 1 star
      completeLevelAndSave(storage, 1, 0); // 3 stars (better)
      const save = loadSave(storage);
      expect(save.levelStars.level1).toBe(3);
    });

    it('accumulates XP across levels', () => {
      completeLevelAndSave(storage, 1, 0); // 30 XP
      completeLevelAndSave(storage, 2, 1); // 20 XP
      const save = loadSave(storage);
      expect(save.xp).toBe(50);
    });

    it('recalculates total stars', () => {
      completeLevelAndSave(storage, 1, 0); // 3 stars
      completeLevelAndSave(storage, 2, 2); // 2 stars
      const save = loadSave(storage);
      expect(save.totalStars).toBe(5);
    });
  });
});
