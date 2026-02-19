/**
 * Validates level JSON data against the expected schema.
 * Used in tests to catch malformed level files early.
 *
 * Level JSON format:
 *   { name, gridWidth, gridHeight, start: {gridX, gridY}, goal: {gridX, gridY},
 *     platforms: [{gridX, gridY, width, tile}], gaps: [{gridX, gridY, width, correctAnswer}] }
 */

export function validateLevel(data) {
  const errors = [];

  if (!data || typeof data !== 'object') {
    return { valid: false, errors: ['Level data must be an object'] };
  }

  // Required top-level fields
  if (typeof data.name !== 'string' || data.name.length === 0) {
    errors.push('Level must have a non-empty "name" string');
  }

  if (typeof data.gridWidth !== 'number' || data.gridWidth < 1 || !Number.isInteger(data.gridWidth)) {
    errors.push('"gridWidth" must be a positive integer');
  }

  if (typeof data.gridHeight !== 'number' || data.gridHeight < 1 || !Number.isInteger(data.gridHeight)) {
    errors.push('"gridHeight" must be a positive integer');
  }

  // Platforms
  if (!Array.isArray(data.platforms) || data.platforms.length === 0) {
    errors.push('"platforms" must be a non-empty array');
  } else {
    data.platforms.forEach((p, i) => {
      if (typeof p.gridX !== 'number') errors.push(`platforms[${i}].gridX must be a number`);
      if (typeof p.gridY !== 'number') errors.push(`platforms[${i}].gridY must be a number`);
      if (typeof p.width !== 'number' || p.width < 1) {
        errors.push(`platforms[${i}].width must be a positive number`);
      }
      if (typeof p.tile !== 'string') errors.push(`platforms[${i}].tile must be a string`);
    });
  }

  // Gaps
  if (!Array.isArray(data.gaps)) {
    errors.push('"gaps" must be an array');
  } else {
    data.gaps.forEach((g, i) => {
      if (typeof g.gridX !== 'number') errors.push(`gaps[${i}].gridX must be a number`);
      if (typeof g.gridY !== 'number') errors.push(`gaps[${i}].gridY must be a number`);
      if (typeof g.width !== 'number' || g.width < 1) {
        errors.push(`gaps[${i}].width must be a positive number`);
      }
      if (typeof g.correctAnswer !== 'number' || g.correctAnswer < 1) {
        errors.push(`gaps[${i}].correctAnswer must be a positive number`);
      }
      // Answer should match gap width
      if (typeof g.width === 'number' && typeof g.correctAnswer === 'number' && g.width !== g.correctAnswer) {
        errors.push(`gaps[${i}].correctAnswer (${g.correctAnswer}) does not match width (${g.width})`);
      }
    });
  }

  // Player spawn
  if (!data.start || typeof data.start.gridX !== 'number' || typeof data.start.gridY !== 'number') {
    errors.push('"start" must have numeric gridX and gridY coordinates');
  }

  // Goal
  if (!data.goal || typeof data.goal.gridX !== 'number' || typeof data.goal.gridY !== 'number') {
    errors.push('"goal" must have numeric gridX and gridY coordinates');
  }

  // Goal should be to the right of player
  if (data.start && data.goal && data.goal.gridX <= data.start.gridX) {
    errors.push('Goal gridX should be greater than start gridX');
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

export default { validateLevel };
