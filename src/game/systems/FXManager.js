/**
 * FXManager — Applies Phaser 3.60+ built-in FX pipeline effects
 * to give game objects a shiny, 3D plastic-toy appearance.
 *
 * All methods gracefully no-op when WebGL / preFX is unavailable
 * (e.g. Canvas fallback on older devices).
 */
export class FXManager {

  // ── Availability check ─────────────────────────────────

  static isAvailable(gameObject) {
    return !!(gameObject && gameObject.preFX);
  }

  static isCameraFXAvailable(camera) {
    return !!(camera && camera.postFX);
  }

  // ── Individual effects ─────────────────────────────────

  /**
   * Drop shadow — gives objects a sense of elevation / depth.
   */
  static addShadow(gameObject, {
    x = 3, y = 3, decay = 0.05, power = 1.2,
    color = 0x000000, samples = 6, intensity = 0.6
  } = {}) {
    if (!this.isAvailable(gameObject)) return null;
    return gameObject.preFX.addShadow(x, y, decay, power, color, samples, intensity);
  }

  /**
   * Outer glow — bright halo around an object.
   */
  static addGlow(gameObject, {
    color = 0xffffff, outerStrength = 4, innerStrength = 0,
    knockout = false, quality = 0.1, distance = 10
  } = {}) {
    if (!this.isAvailable(gameObject)) return null;
    return gameObject.preFX.addGlow(color, outerStrength, innerStrength, knockout, quality, distance);
  }

  /**
   * Sweeping shine — mimics light reflecting off glossy/plastic surfaces.
   */
  static addShine(gameObject, {
    speed = 0.5, lineWidth = 0.5, gradient = 3, reveal = false
  } = {}) {
    if (!this.isAvailable(gameObject)) return null;
    return gameObject.preFX.addShine(speed, lineWidth, gradient, reveal);
  }

  // ── Animated / compound effects ────────────────────────

  /**
   * Pulsing glow — the outerStrength animates up and down via a tween.
   * Great for goal objects and collectibles.
   */
  static addPulsingGlow(scene, gameObject, {
    color = 0xffffff, minStrength = 2, maxStrength = 6, duration = 1500
  } = {}) {
    const glow = this.addGlow(gameObject, { color, outerStrength: minStrength });
    if (!glow) return null;

    scene.tweens.add({
      targets: glow,
      outerStrength: maxStrength,
      duration,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut'
    });

    return glow;
  }

  /**
   * "Shiny plastic" combo — shadow for depth + slow shine sweep.
   * The signature look for the soft-plastic-voxel art style.
   */
  static addPlastic3D(gameObject, {
    shadow = {},
    shine = {}
  } = {}) {
    if (!this.isAvailable(gameObject)) return;
    this.addShadow(gameObject, shadow);
    this.addShine(gameObject, { speed: 0.3, lineWidth: 0.3, gradient: 4, ...shine });
  }

  /**
   * Interactive button style — shadow for depth + glow that
   * can be toggled stronger on hover.
   * Returns { shadow, glow } refs so hover handlers can tweak them.
   */
  static addButtonFX(gameObject, { glowColor = 0x3498db } = {}) {
    if (!this.isAvailable(gameObject)) return null;

    const shadow = this.addShadow(gameObject, { x: 2, y: 2, intensity: 0.4 });
    const glow = this.addGlow(gameObject, {
      color: glowColor, outerStrength: 0, quality: 0.1, distance: 8
    });

    return { shadow, glow };
  }

  // ── Camera-level effects ───────────────────────────────

  /**
   * Subtle camera bloom — soft, warm overall glow for the entire scene.
   */
  static addCameraBloom(camera, {
    color = 0xffffff, offsetX = 1, offsetY = 1,
    blurStrength = 1, strength = 0.28, steps = 4
  } = {}) {
    if (!this.isCameraFXAvailable(camera)) return null;
    return camera.postFX.addBloom(color, offsetX, offsetY, blurStrength, strength, steps);
  }
}
