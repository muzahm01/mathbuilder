/**
 * Load a level JSON file by number.
 * Files are stored at /levels/world1/level01.json, etc.
 */
export async function loadLevel(levelNumber) {
  const paddedNum = String(levelNumber).padStart(2, '0');
  const url = `./levels/world1/level${paddedNum}.json`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to load level ${levelNumber}: ${response.status}`);
  }

  return response.json();
}
