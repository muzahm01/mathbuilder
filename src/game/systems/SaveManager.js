/**
 * Manages game save data in LocalStorage.
 * Handles level stars, XP, unlocked levels, and title progression.
 */

const SAVE_KEY = 'mathbuilder_save';

const DEFAULT_SAVE = {
  xp: 0,
  levelsUnlocked: 1,
  levelStars: {},
  totalStars: 0
};

export function loadSave(storage) {
  try {
    const raw = storage.getItem(SAVE_KEY);
    if (!raw) return { ...DEFAULT_SAVE };
    const parsed = JSON.parse(raw);
    return { ...DEFAULT_SAVE, ...parsed };
  } catch {
    return { ...DEFAULT_SAVE };
  }
}

export function writeSave(storage, data) {
  storage.setItem(SAVE_KEY, JSON.stringify(data));
}

export function clearSave(storage) {
  storage.removeItem(SAVE_KEY);
}

export function calculateStars(wrongAnswers) {
  if (wrongAnswers === 0) return 3;
  if (wrongAnswers <= 2) return 2;
  return 1;
}

export function completeLevelAndSave(storage, levelNumber, wrongAnswers) {
  const save = loadSave(storage);
  const stars = calculateStars(wrongAnswers);
  const levelKey = `level${levelNumber}`;
  const previousStars = save.levelStars[levelKey] || 0;

  // Only update if new score is better
  if (stars > previousStars) {
    save.levelStars[levelKey] = stars;
  }

  // Recalculate total stars
  save.totalStars = Object.values(save.levelStars).reduce((sum, s) => sum + s, 0);

  // Unlock next level
  if (levelNumber >= save.levelsUnlocked) {
    save.levelsUnlocked = levelNumber + 1;
  }

  // Award XP (10 per star earned this attempt)
  save.xp += stars * 10;

  writeSave(storage, save);
  return { stars, save };
}

const SaveManager = {
  loadSave,
  writeSave,
  clearSave,
  calculateStars,
  completeLevelAndSave
};

export default SaveManager;
