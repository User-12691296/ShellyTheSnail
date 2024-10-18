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
  
