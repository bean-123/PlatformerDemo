# 🧗 Python-Platformer
A vertical-scrolling 2D platformer built with Pygame, focused on climbing as high as possible while surviving hazards and managing limited health. Platforms are partly handcrafted and partly procedurally generated, so no two climbs feel exactly the same.

The higher you go, the world changes—colors shift, stars appear, and the game quietly turns into a survival test against gravity, timing, and fire.

## 🎮 Gameplay Overview
- Goal: Climb upward indefinitely and beat your best height

- Health system: 5 hearts (10 half-hits total)

- Hazards: Animated fire traps that deal damage on contact

- Progression: Platforms generate dynamically as you climb

- Atmosphere: Dynamic sky gradient + parallax star field at high altitude

Your best height is tracked across runs, so every fall is just research for the next attempt.

## 🕹️ Controls
```
Key	Action
A	Move left
D	Move right
SPACE	Jump (double jump supported)
Close Window	Quit game
```

## ✨ Features
- Smooth character animation with directional sprite flipping

- Double-jump mechanics with gravity-based fall acceleration

- Pixel-perfect collision using masks

- Dynamic background that evolves with height

- Procedural platform generation with risk-reward fire placement

- Persistent best height tracking across deaths

- Visual heart-based health UI (full / half / empty hearts)

## 🚀 How to Run
1. Make sure Python 3.9+ is installed

2. Install dependencies:
```
python -m pip install pygame
```
3. Run the game:
```
python main.py
```

## 🛠️ Customization Ideas
- All sprites are loaded dynamically, so swapping characters or terrain is as simple as replacing assets in Player.SPRITES

- Adjust gravity, jump strength, or animation speed for different game feel

- Add enemies, collectibles, or checkpoints

- Introduce biomes tied to height ranges (space debris, clouds, ruins…)

- This codebase is intentionally modular—meant to be played with, broken, and rebuilt.

## 📚 Built With
- Python

- Pygame

- Procedural generation logic

## 🙏 Credits & Acknowledgements

This project was originally inspired by tutorials from **Tech With Tim** on YouTube.

The core foundation and concepts come from his platformer series, and the project was later extended and heavily modified by me, including:

- Vertical infinite climbing gameplay

- Procedural platform generation

- Health and damage system with visual hearts

- Dynamic background transitions and star field

- Height tracking and persistent best score

This project evolved beyond the original tutorial into a personal learning and experimentation project.
