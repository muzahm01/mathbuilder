/**
 * Maps accumulated XP to player titles.
 * Titles provide positive reinforcement and a sense of progression.
 */

const TITLES = [
  { xp: 0,   title: 'Newbie' },
  { xp: 50,  title: 'Math Cadet' },
  { xp: 120, title: 'Number Ninja' },
  { xp: 200, title: 'Bridge Builder' },
  { xp: 300, title: 'Team Leader' },
  { xp: 450, title: 'Math Hero' },
  { xp: 600, title: 'Grand Master' },
  { xp: 800, title: 'Legend' }
];

export function getTitleForXP(xp) {
  let current = TITLES[0];
  for (const entry of TITLES) {
    if (xp >= entry.xp) {
      current = entry;
    } else {
      break;
    }
  }
  return current.title;
}

export function getNextTitle(xp) {
  for (const entry of TITLES) {
    if (xp < entry.xp) {
      return { title: entry.title, xpNeeded: entry.xp };
    }
  }
  return null; // Already at max title
}

export function getAllTitles() {
  return TITLES.map(t => ({ ...t }));
}

const TitleSystem = {
  getTitleForXP,
  getNextTitle,
  getAllTitles
};

export default TitleSystem;
