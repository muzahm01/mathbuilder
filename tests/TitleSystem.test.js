import { describe, it, expect } from 'vitest';
import {
  getTitleForXP,
  getNextTitle,
  getAllTitles
} from '../src/game/systems/TitleSystem.js';

describe('TitleSystem', () => {
  describe('getTitleForXP', () => {
    it('returns Newbie for 0 XP', () => {
      expect(getTitleForXP(0)).toBe('Newbie');
    });

    it('returns Math Cadet at 50 XP', () => {
      expect(getTitleForXP(50)).toBe('Math Cadet');
    });

    it('returns Number Ninja at 120 XP', () => {
      expect(getTitleForXP(120)).toBe('Number Ninja');
    });

    it('returns Bridge Builder at 200 XP', () => {
      expect(getTitleForXP(200)).toBe('Bridge Builder');
    });

    it('returns Team Leader at 300 XP', () => {
      expect(getTitleForXP(300)).toBe('Team Leader');
    });

    it('returns Math Hero at 450 XP', () => {
      expect(getTitleForXP(450)).toBe('Math Hero');
    });

    it('returns Grand Master at 600 XP', () => {
      expect(getTitleForXP(600)).toBe('Grand Master');
    });

    it('returns Legend at 800 XP', () => {
      expect(getTitleForXP(800)).toBe('Legend');
    });

    it('returns Legend for XP well above 800', () => {
      expect(getTitleForXP(9999)).toBe('Legend');
    });

    it('stays at current title between thresholds', () => {
      expect(getTitleForXP(49)).toBe('Newbie');
      expect(getTitleForXP(119)).toBe('Math Cadet');
    });
  });

  describe('getNextTitle', () => {
    it('returns Math Cadet as next title for 0 XP', () => {
      const next = getNextTitle(0);
      expect(next.title).toBe('Math Cadet');
      expect(next.xpNeeded).toBe(50);
    });

    it('returns Number Ninja as next title for 50 XP', () => {
      const next = getNextTitle(50);
      expect(next.title).toBe('Number Ninja');
      expect(next.xpNeeded).toBe(120);
    });

    it('returns null when at max title', () => {
      expect(getNextTitle(800)).toBeNull();
      expect(getNextTitle(9999)).toBeNull();
    });
  });

  describe('getAllTitles', () => {
    it('returns 8 titles', () => {
      expect(getAllTitles()).toHaveLength(8);
    });

    it('starts with Newbie and ends with Legend', () => {
      const titles = getAllTitles();
      expect(titles[0].title).toBe('Newbie');
      expect(titles[titles.length - 1].title).toBe('Legend');
    });

    it('XP thresholds are in ascending order', () => {
      const titles = getAllTitles();
      for (let i = 1; i < titles.length; i++) {
        expect(titles[i].xp).toBeGreaterThan(titles[i - 1].xp);
      }
    });
  });
});
