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
C:> python -m pip instal numpy
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

Default (from the start)
 - drawrect left top right bottom R G B (Draw a rectangle, 4 per frame)
 - drawchar text X Y R G B (Draw character, up to 10 between clear commands)
 - clear ()
 - Layers: 1
 - Commands per frame: 3
CleaningPowers (20 seconds)
 - Fill screen with specified colour
Advanced (60 seconds)
 - + 1 layer
 - Switch layers anytime
 - Layers are now 4x the size of the screen, and can be shifted as needed, up to 10 pixels per frame
Elite (60 seconds)
 - + 2 layers
Comprehensive (30 seconds)
 - + 6 commands per frame
Talkative (60 seconds)
 - Up to 10 characters on screen at once
 - 4 font sizes with drawchar: 12, 18, 24, 36
Shapes (45 seconds)
 - (max 4 per frame)
 - Draw polygon 
 - Draw ellipse
 - Draw box
Tiles (45 seconds)
 - One tile per frame
Entities and Projectiles (60 seconds)
 - One entity per frame
Items (45 seconds)
 - One item per frame
Regions (30 seconds)
 - Clamp region of layer drawn
Display Control (45 seconds)
 - Layer shifts += 10
 - Flip, rotate layers on screen
