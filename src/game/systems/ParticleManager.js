export class ParticleManager {
  /**
   * Dust burst at a specific position.
   * Used when bridge blocks are placed.
   */
  static dustBurst(scene, x, y) {
    const emitter = scene.add.particles(x, y, 'dust', {
      speed: { min: 50, max: 150 },
      angle: { min: 200, max: 340 },
      lifespan: 400,
      quantity: 8,
      scale: { start: 1, end: 0 },
      alpha: { start: 0.8, end: 0 },
      gravityY: 100,
      emitting: false
    });

    emitter.explode();

    // Auto-cleanup after particles expire
    scene.time.delayedCall(500, () => emitter.destroy());
  }

  /**
   * Confetti rain across the screen.
   * Used on level complete scene.
   */
  static confetti(scene) {
    const emitter = scene.add.particles(400, -20, 'confetti', {
      x: { min: 0, max: 800 },
      speed: { min: 80, max: 250 },
      angle: { min: 75, max: 105 },
      lifespan: 3000,
      quantity: 3,
      frequency: 60,
      scale: { start: 1.5, end: 0.5 },
      rotate: { min: 0, max: 360 },
      tint: [0xff4444, 0x44ff44, 0x4444ff, 0xffff44, 0xff44ff, 0x44ffff],
      gravityY: 150
    });

    // Stop spawning after 2.5 seconds
    scene.time.delayedCall(2500, () => emitter.stop());

    // Destroy after all particles expire
    scene.time.delayedCall(6000, () => emitter.destroy());
  }

  /**
   * Small sparkle at a position.
   * Used when a filled star pops in on the level complete screen.
   */
  static sparkle(scene, x, y) {
    const emitter = scene.add.particles(x, y, 'confetti', {
      speed: { min: 30, max: 100 },
      angle: { min: 0, max: 360 },
      lifespan: 300,
      quantity: 6,
      scale: { start: 0.8, end: 0 },
      tint: 0xf1c40f, // Gold
      emitting: false
    });

    emitter.explode();
    scene.time.delayedCall(400, () => emitter.destroy());
  }
}
