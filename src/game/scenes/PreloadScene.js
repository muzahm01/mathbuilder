import Phaser from 'phaser';

export default class PreloadScene extends Phaser.Scene {
  constructor() {
    super('Preload');
  }

  preload() {
    const width = this.scale.width;
    const height = this.scale.height;

    // Background bar
    const barBg = this.add.rectangle(width / 2, height / 2, 320, 30, 0x2c3e50);
    barBg.setStrokeStyle(2, 0xffffff);

    // Fill bar
    const barFill = this.add.rectangle(
      width / 2 - 150, height / 2, 0, 22, 0x27ae60
    ).setOrigin(0, 0.5);

    // Loading text
    const loadingText = this.add.text(width / 2, height / 2 - 40, 'Loading...', {
      fontSize: '24px',
      fontFamily: 'Fredoka One',
      color: '#ffffff'
    }).setOrigin(0.5);

    // Update bar on progress
    this.load.on('progress', (value) => {
      barFill.width = 300 * value;
    });

    this.load.on('complete', () => {
      loadingText.setText('Ready!');
    });

    // ── Tiles ────────────────────────────────────────
    this.load.image('grass-top', 'assets/images/tiles/grass-top.png');
    this.load.image('dirt', 'assets/images/tiles/dirt.png');
    this.load.image('stone', 'assets/images/tiles/stone.png');

    // ── Player Sprite Sheets ─────────────────────────
    this.load.spritesheet('botty-idle', 'assets/images/player/botty-idle.png', {
      frameWidth: 64,
      frameHeight: 64
    });
    this.load.spritesheet('botty-walk', 'assets/images/player/botty-walk.png', {
      frameWidth: 64,
      frameHeight: 64
    });
    this.load.spritesheet('botty-jump', 'assets/images/player/botty-jump.png', {
      frameWidth: 64,
      frameHeight: 64
    });

    // ── Backgrounds ──────────────────────────────────
    this.load.image('sky', 'assets/images/backgrounds/sky.png');
    this.load.image('clouds', 'assets/images/backgrounds/clouds.png');
    this.load.image('hills', 'assets/images/backgrounds/hills.png');

    // ── UI Elements ──────────────────────────────────
    this.load.image('btn-play', 'assets/images/ui/btn-play.png');
    this.load.image('btn-levels', 'assets/images/ui/btn-levels.png');
    this.load.image('star-filled', 'assets/images/ui/star-filled.png');
    this.load.image('star-empty', 'assets/images/ui/star-empty.png');

    // ── Objects ──────────────────────────────────────
    this.load.image('flag', 'assets/images/objects/flag.png');
    this.load.image('bridge-block', 'assets/images/objects/bridge-block.png');

    // ── Particles ────────────────────────────────────
    this.load.image('dust', 'assets/images/particles/dust.png');
    this.load.image('confetti', 'assets/images/particles/confetti.png');
  }

  create() {
    // ── Define Player Animations ─────────────────────
    this.anims.create({
      key: 'botty-idle',
      frames: this.anims.generateFrameNumbers('botty-idle', { start: 0, end: 3 }),
      frameRate: 6,
      repeat: -1
    });

    this.anims.create({
      key: 'botty-walk',
      frames: this.anims.generateFrameNumbers('botty-walk', { start: 0, end: 5 }),
      frameRate: 10,
      repeat: -1
    });

    this.anims.create({
      key: 'botty-jump',
      frames: this.anims.generateFrameNumbers('botty-jump', { start: 0, end: 1 }),
      frameRate: 4,
      repeat: 0
    });

    // ── Transition to Menu ───────────────────────────
    this.scene.start('Menu');
  }
}
