# ShellyTheSnail
## Hello!
Welcome to Alchemyhacks 2024! This is the public repository for the game, Shelly the Snail's GREAT Adventure!

If you don't know what we're talking about, check out our background here: [Devpost and Registration](https://alchemyhacks.devpost.com/)

## What is this?
For AlchemyHacks, we decided to take a unique approach to running a hackathon. We made a video game, and your job is to code up a tutorial for the video game. This repository is the code for our game!

## How to download and run the source code?
Download the code! To get the source code, you can download git and use git clone, github desktop, or just download the code as a .ZIP file. You'll need python installed: [Python](https://www.python.org/)

Then, after installing python, open command prompt and run:
```
C:> python -m pip install pygame
C:> python -m pip install numpy
```
If you've already installed these packages, but are running into errors still, you can update python and update the installed packages.

## What to do?
After downloading python and the game, then learn how to play the game! The goal is to beat the final boss, kung fu krane! There's several ways to make this fight eaiser, so explore as much as possible until you can beat it!

Then, plan out your tutorial. You have 10 minutes of tutorial time, and your tutorial is written in tutorial.tuto. There's a series of commands you can use, as described below, and you're trying to teach a complete newbie how to beat the game, from scratch!

Join our discord if you have any questions!

## Tutorial Specs
To get your tutorial, the game will open the file `tutorial/tutorial.tuto`, and parse the commands in it into a tutorial you can see on screen

### What is `tutorial.tuto`?
It's a plaintext file format that we've created! In it are all your graphics commands, for each frame of the tutorial. In its most basic form, a tutorial will look like this if you open it up in a text editor:
```
#HEADER
#FRAMES
#INITIAL
#LOBBY
#DUNGEON
#SWAMP
#DESERT
#MOUNTAINS
#ARCTIC
#DARKNESS
#VOID
#FINAL
```
Let's break this down some more
### The Header
Headers don't do anything graphics related, but that doesn't mean they aren't important! Headers will set what graphics commands you want to use, along with the wait between the last tutorial frame and returning to the game.

The cooldown is set with the header command `pausebeforereturn`, followed by a number representing the number of frames the game should run for

### Graphics Commands
If every graphics command possible was available from the start, then there wouldn't be much challenge to creating and running a tutorial, and you might as well just be coding a tutorial manually. This is why we decided to create a very specific set of graphics commands, and unlocking new ones costs some of your precious tutorial time. The way this will work is using packages, where you can purchase any of the 13 packages to unlock and upgrade the graphics commands you have available to you.

Purchasing a package of graphics commands is done with the `buy` header command, followed by the name of the package you wish to purchase

A header then might look like:
```
#HEADER
pausebeforereturn 120
buy advanced
buy control
```
Which sets a delay of 120 frames (2 seconds) before returning to the game after the displaying last tutorial frame, and unlocks the advanced and control packages for you to use

### The Package List and Graphics Commands
Commands are listed with their arguments after, and a brief description in brackets
All colours are specified as integers from 0-255, with 255 being brightest

Default (from the start)
 - drawrect left top right bottom R G B (Draw a rectangle, 4 per frame)
 - drawchar char X Y R G B (Draw character, up to 10 between clear commands)
 - clear ()
 - Layers: 1
 - Layer size: 640 x 400 (scaled to full screen)
 - Commands per frame: 3

CleaningPowers (20 seconds)
 - clear R G B (fill screen with colour)

Advanced (60 seconds)
 - switchlayer layer (switch between which layer is drawn. This can be a great way to draw in advance. Resets)
 - Layers: +1 (draw things without showing them, then switch to the layer you want to see)
 - Layer size: 2560 x 1600 (640 x 400 segments drawn on screen at once)

Elite (30 seconds)
 - Layers: +2 (draw more things)

Comprehensive (30 seconds)
 - Commands per frame: +6

Talkative (60 seconds)
 - drawchar text font_size X Y R G B (font size number from 0-3: 0=12, 1=18, 2=24, 3=36)
 - Characters between clears: +10

Shapes (45 seconds)
 - Shapes per frame: +4 (starts at 4)
 - drawellipse left top right bottom R G B (draw ellipse nested into rectangle bounds)
 - drawpolygon X1 Y1 X2 Y2 X3 Y3 X4 Y4 X5 Y5 X6 Y6 ... R G B (as many or as few vertices as you'd like, then the colour value)

Tiles (45 seconds)
 - Load all the tile textures
 - drawtile tile_texture_name X Y (draw a tile, take a look at the game's asset folder to see texture names)

Entities and Projectiles (60 seconds)
 - Load all the entity and projectile textures (not the bosses though, you'll have to get creative for those!)
 - drawentity entity_texture_name X Y (draw a tile, take a look at the game's asset folder to see texture names)

Items (45 seconds)
 - Load all the tile textures
 - drawtile tile_texture_name X Y (draw a tile, take a look at the game's asset folder to see texture names)

Regions (30 seconds)
 - clampregion left top right bottom (Only this region of the layer is drawn to the screen)

Display Control (45 seconds)
 - Layer shift size: +10
 - flipdisp acrossX acrossY (flip the layer across the X or Y)
 - rotatedisp rotation_change (<10 degrees per command)
 - Order is: flip, rotation, region clamping, scaling to screen

### The Biome Specifiers
Because 10 minutes is a ton of time to do everything all at once, we're letting you split your tutorial up into 10 different points in progression, mostly first entry to new biomes and boss arenas. Place your frames under each biome specifier, and they will run when the player reaches that point in progression, then the tutorial will cut back to the game. This lets you split up your 36,000 frames however you'd like across the 10 progression points, giving you full flexibility with your tutorial.
