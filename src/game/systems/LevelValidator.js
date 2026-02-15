/**
 * Validates level JSON data against the expected schema.
 * Used in tests to catch malformed level files early.
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

  if (typeof data.width !== 'number' || data.width < 1 || !Number.isInteger(data.width)) {
    errors.push('"width" must be a positive integer');
  }

  // Platforms
  if (!Array.isArray(data.platforms) || data.platforms.length === 0) {
    errors.push('"platforms" must be a non-empty array');
  } else {
    data.platforms.forEach((p, i) => {
      if (typeof p.x !== 'number') errors.push(`platforms[${i}].x must be a number`);
      if (typeof p.y !== 'number') errors.push(`platforms[${i}].y must be a number`);
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
      if (typeof g.x !== 'number') errors.push(`gaps[${i}].x must be a number`);
      if (typeof g.y !== 'number') errors.push(`gaps[${i}].y must be a number`);
      if (typeof g.width !== 'number' || g.width < 1) {
        errors.push(`gaps[${i}].width must be a positive number`);
      }
      if (typeof g.answer !== 'number' || g.answer < 1) {
        errors.push(`gaps[${i}].answer must be a positive number`);
      }
      // Answer should match gap width
      if (typeof g.width === 'number' && typeof g.answer === 'number' && g.width !== g.answer) {
        errors.push(`gaps[${i}].answer (${g.answer}) does not match width (${g.width})`);
      }
    });
  }

  // Player spawn
  if (!data.player || typeof data.player.x !== 'number' || typeof data.player.y !== 'number') {
    errors.push('"player" must have numeric x and y coordinates');
  }

  // Goal
  if (!data.goal || typeof data.goal.x !== 'number' || typeof data.goal.y !== 'number') {
    errors.push('"goal" must have numeric x and y coordinates');
  }

  // Goal should be to the right of player
  if (data.player && data.goal && data.goal.x <= data.player.x) {
    errors.push('Goal x should be greater than player x');
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

export default { validateLevel };
