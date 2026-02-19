/**
 * Load a level JSON file by number.
 * Files are stored at /levels/world1/level01.json, etc.
 */
export async function loadLevel(levelNumber) {
  // Validate levelNumber is an integer in the expected range (1-10)
  const num = Number(levelNumber);
  if (!Number.isInteger(num) || num < 1 || num > 10) {
    throw new Error(`Invalid level number: ${levelNumber}`);
  }

  const paddedNum = String(num).padStart(2, '0');
  const url = `./levels/world1/level${paddedNum}.json`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to load level ${num}: ${response.status}`);
  }

  return response.json();
}
