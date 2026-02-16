import Phaser from 'phaser';
import { TILE_SIZE, gridToPixel } from '../systems/GridSystem.js';
import { loadLevel } from '../systems/LevelLoader.js';
import { MathInputUI } from '../systems/MathInputUI.js';
import { buildBridge } from '../objects/Bridge.js';
import Player from '../objects/Player.js';
import GoalFlag from '../objects/GoalFlag.js';
import { completeLevelAndSave } from '../systems/SaveManager.js';
import { getTitleForXP } from '../systems/TitleSystem.js';
import { TouchControls } from '../systems/TouchControls.js';
import { addFullscreenButton } from '../systems/FullscreenButton.js';

export default class GameScene extends Phaser.Scene {
  constructor() {
    super('Game');
  }

  init(data) {
    this.levelNumber = data.levelNumber || 1;
    this.wrongAttempts = 0;
    this.levelComplete = false;
  }

  async create() {
    // ── Load Level Data ──────────────────────────────
    let levelData;
    try {
      levelData = await loadLevel(this.levelNumber);
    } catch (err) {
      console.error(err);
      this.scene.start('LevelSelect');
      return;
    }

    // ── Set World Bounds ─────────────────────────────
    const worldWidth = levelData.gridWidth * TILE_SIZE;
    const worldHeight = levelData.gridHeight * TILE_SIZE;
    this.physics.world.setBounds(0, 0, worldWidth, worldHeight);

    // ── Parallax Background ──────────────────────────
    this.add.image(400, 300, 'sky')
      .setScrollFactor(0)
      .setDepth(-3);

    this.cloudLayer = this.add.tileSprite(400, 100, 800, 200, 'clouds')
      .setScrollFactor(0)
      .setDepth(-2);

    this.hillLayer = this.add.tileSprite(400, 450, 800, 200, 'hills')
      .setScrollFactor(0)
      .setDepth(-1);

    // ── Build Platforms ──────────────────────────────
    this.platforms = this.physics.add.staticGroup();

    for (const p of levelData.platforms) {
      const { x: baseX, y: baseY } = gridToPixel(p.gridX, p.gridY);

      for (let i = 0; i < p.width; i++) {
        const tileKey = p.tile || 'grass-top';

        const block = this.platforms.create(
          baseX + i * TILE_SIZE + TILE_SIZE / 2,
          baseY + TILE_SIZE / 2,
          tileKey
        );
        block.setSize(TILE_SIZE, TILE_SIZE);
        block.refreshBody();
      }
    }

    // ── Build Gap Trigger Zones ──────────────────────
    this.gapZones = [];

    for (const g of levelData.gaps) {
      const { x, y } = gridToPixel(g.gridX, g.gridY);

      // The zone sits one tile above the gap floor
      const zone = this.add.zone(
        x + (g.width * TILE_SIZE) / 2,
        y - TILE_SIZE / 2,
        g.width * TILE_SIZE,
        TILE_SIZE
      );
      this.physics.add.existing(zone, true);

      zone.gapData = g;
      zone.solved = false;

      this.gapZones.push(zone);

      // Counting aid: faint vertical lines to help children count tiles
      const graphics = this.add.graphics();
      graphics.lineStyle(1, 0xffffff, 0.2);
      for (let i = 1; i < g.width; i++) {
        const lineX = x + i * TILE_SIZE;
        graphics.moveTo(lineX, y);
        graphics.lineTo(lineX, y + TILE_SIZE);
      }
      graphics.strokePath();
    }

    // ── Create Player ────────────────────────────────
    this.player = new Player(
      this,
      levelData.start.gridX,
      levelData.start.gridY
    );

    // ── Collisions ───────────────────────────────────
    this.physics.add.collider(this.player, this.platforms);

    // Gap overlap detection
    for (const zone of this.gapZones) {
      this.physics.add.overlap(this.player, zone, () => {
        if (!zone.solved && !this.mathInputActive) {
          this.openMathInput(zone);
        }
      });
    }

    // ── Goal Flag ────────────────────────────────────
    this.goalFlag = new GoalFlag(
      this,
      levelData.goal.gridX,
      levelData.goal.gridY
    );
    this.physics.add.overlap(this.player, this.goalFlag, () => {
      this.completeLevel();
    });

    // ── Camera ───────────────────────────────────────
    this.cameras.main.setBounds(0, 0, worldWidth, worldHeight);
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);

    // ── Fullscreen Button ──────────────────────────
    addFullscreenButton(this, 770, 30);

    // ── Touch Controls ──────────────────────────────
    this.touchControls = new TouchControls(this);
    this.player.touchControls = this.touchControls;

    // ── Math Input UI ────────────────────────────────
    this.mathInputActive = false;
    this.mathUI = new MathInputUI((gapData, correct) => {
      if (correct) {
        this.onCorrectAnswer(gapData);
      } else {
        this.wrongAttempts++;
        this.sound.play('sfx-wrong', { volume: 0.4 });
      }
    });

    // ── Store level data for later reference ─────────
    this.levelData = levelData;

    // ── Fade in ───────────────────────────────────────
    this.cameras.main.fadeIn(300, 0, 0, 0);
  }

  update() {
    if (!this.player) return;

    this.player.update();

    // Fall death detection
    if (this.player.y > this.levelData.gridHeight * TILE_SIZE + 100) {
      this.restartLevel();
    }

    // Parallax scrolling
    if (this.cloudLayer) {
      this.cloudLayer.tilePositionX = this.cameras.main.scrollX * 0.1;
    }
    if (this.hillLayer) {
      this.hillLayer.tilePositionX = this.cameras.main.scrollX * 0.3;
    }
  }

  // ── Math Input ───────────────────────────────────────

  openMathInput(zone) {
    this.mathInputActive = true;
    this.physics.pause();
    this.mathUI.show(zone.gapData);
  }

  onCorrectAnswer(gapData) {
    const zone = this.gapZones.find(z => z.gapData === gapData);
    if (zone) zone.solved = true;

    this.sound.play('sfx-correct', { volume: 0.7 });
    buildBridge(this, gapData, this.platforms);

    this.mathInputActive = false;
    this.physics.resume();
  }

  // ── Level Flow ───────────────────────────────────────

  completeLevel() {
    if (this.levelComplete) return;
    this.levelComplete = true;

    this.physics.pause();
    this.sound.play('sfx-win', { volume: 0.8 });

    // Calculate stars
    let stars;
    if (this.wrongAttempts === 0) stars = 3;
    else if (this.wrongAttempts <= 2) stars = 2;
    else stars = 1;

    // Calculate XP
    const gapCount = this.levelData.gaps.length;
    const xpEarned = (gapCount * 10) + (stars * 5);

    // Save progress
    const { save } = completeLevelAndSave(localStorage, this.levelNumber, this.wrongAttempts);
    const title = getTitleForXP(save.xp);

    // Brief celebration delay, then fade transition
    this.time.delayedCall(500, () => {
      this.cameras.main.fadeOut(300, 0, 0, 0);
      this.cameras.main.once('camerafadeoutcomplete', () => {
        this.scene.start('LevelComplete', {
          levelNumber: this.levelNumber,
          stars: stars,
          xpEarned: xpEarned,
          totalXP: save.xp,
          title: title
        });
      });
    });
  }

  restartLevel() {
    this.mathUI.hide();
    this.scene.restart({ levelNumber: this.levelNumber });
  }
}
