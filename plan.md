MathBuilder - The Game
Target Audience: 7-Year-Olds | Platform: Web (Phaser.js) | Hosting: Vercel

1. Project Overview
A web-based 2D platformer where math builds the world.

Core Loop: "Pass-and-Play." The child builds a level with math gaps; the parent plays it by solving the math.

Visual Style: 2.5D "Soft Plastic Voxel" (Minecraft meets Mario).

Tech Stack: HTML5, Phaser 3, LocalStorage.

Phase 1: The Foundation (Setup)
Goal: Get a blank game running on the web.

1.1 Repository Setup
[ ] Create a GitHub Account (if needed).

[ ] Create a new Repo: mathbuilder.

[ ] Connect Repo to Vercel (Free Tier).

[ ] Verify: Push a basic index.html file and see it live at mathbuilder.vercel.app.

1.2 The Engine (Phaser 3)
Prompt for Claude:

"Create a basic HTML5 boilerplate for a Phaser 3 game. Include index.html, style.css, and a game.js file. The game config should be 800x600, use Arcade Physics, and scale to fit a tablet screen."

[ ] Commit code to GitHub.

[ ] Verify the black game screen loads on your device.

Phase 2: Core Mechanics (The Logic)
Goal: A square (Botty) can move, jump, and interact with a gap.

2.1 The "Grid" System
Prompt for Claude:

"I need a grid system for my Phaser game. The tile size is 64x64 pixels. Write a function to draw a debug grid over the background so I can see the squares. Also, set up a simple player sprite (use a placeholder red square) that can move left/right and jump using arrow keys."

[ ] Test: Can you move the square? Do you see the grid lines?

2.2 The "Math Tool" Logic (The Bridge)
Prompt for Claude:

"Implement the 'Bridge Tool'. When the player clicks a specific 'gap' area, pause the game and open a simple HTML input prompt asking for a number. If the input matches the gap width (in grid units), spawn a platform of that length. If wrong, show a 'Too Short/Long' message."

Phase 3: Visuals & Art Assets (The Look)
Goal: Replace placeholder squares with "Soft Plastic Voxel" art.

3.1 Asset Generation Strategy
Prompt for Gemini (Nano Banana):

"Generate a 2.5D game asset: A seamless texture of a cartoon grass block. It should look like a smooth, soft plastic toy block. Vibrant green top, cartoon dirt side. Iso-metric view but flattened for 2D platformer use."

Prompt for Gemini (Nano Banana):

"Generate a game character sprite: A cute, chunky blue robot named Botty. He looks like a high-quality vinyl toy. Front view and Side view. Simple shapes, bright primary colors."

3.2 UI Design
Prompt for Gemini:

"Generate a UI set for a kids' game: A glossy 'Play' button (green), a 'Build' button (hammer icon), and a 'Math Input' box background (looks like a blueprint). Style: Candy-like, rounded corners."

3.3 Integrating Art
Prompt for Claude:

"Here are my image files: ground.png, player.png, background.png. Help me update the preload() function in Phaser to load these, and replace the red square and debug grid with these actual images."

Phase 4: The Game Loop & Progression
Goal: Turning mechanics into a real game.

4.1 Win/Loss States
Prompt for Claude:

"Add a 'Goal Flag' object. When the player touches it, show a 'Level Complete' popup. If the player falls below the bottom of the screen (Y > 600), restart the scene."

4.2 The LocalStorage Save System
Prompt for Claude:

"Write a SaveManager class using browser LocalStorage. It needs to save: 1. Current Level (Integer), 2. Stars earned per level (Array), 3. Current Title/Rank (String). It should automatically load this data when the game starts."

4.3 The "Title" System
Prompt for Claude:

"Create a logic check: After every level, check the total XP. Update the player's 'Title' text based on this list: Level 1='Newbie', Level 10='Team Leader', Level 40='Grand Master'. Display this title on the main menu."

Phase 5: Level Design (The Content)
Goal: Building World 1 (The Grasslands).

5.1 Level Data Structure
Prompt for Claude:

"I want to store level designs in a JSON file instead of hard-coding them. Define a JSON structure that holds: Platform positions, Gap locations, Correct Math Answer for each gap, and Start/End coordinates."

5.2 Building Levels 1-10
Action: You (the human) will map out the 10 levels on graph paper first.

Level 1: One gap (Answer: 3).

Level 5: Two gaps (Answers: 4 and 2).

Level 10 (Boss): The "Mega Bridge." A gap of 10 blocks that requires scrolling to count.

Phase 6: Polish & Launch
Goal: Making it feel professional.

6.1 Sound Effects
Resource: Use sfxr.me (a free chiptune sound generator) to make:

Jump.wav

CorrectAnswer.wav (A ding!)

WrongAnswer.wav (A buzzer)

Build.wav (A construction noise)

6.2 The "Juice"
Prompt for Claude:

"Add particle effects. When a bridge is built, I want small dust particles to poof out from the blocks. When the player wins, launch confetti particles."

6.3 Final Deploy
[ ] Push final code to GitHub.

[ ] Check Vercel for the live link.

[ ] Test on Tablet: Ensure touch controls work (Claude can help add on-screen arrow buttons if the physical keyboard isn't available).

Technical Appendix: Prompt Strategy
When asking Claude for Code:

Be specific about the library: "Using Phaser 3..."

Be specific about the physics: "Using Arcade Physics..."

Paste your current code first so it knows the context.

When asking Gemini for Art:

Use keywords: "Isometric," "Voxel," "Soft Lighting," "Vibrant Colors," "White Background," "Sprite Sheet."

Ask for variations: "Give me 4 variations of the stone block."