# Bingo Project

A **console-based 3×5 Bingo game** built entirely in Python.
Players can fill their own cards, draw random numbers, and earn points for completing lines or diagonals.
Developed as part of the **Project Session 2** assignment.

## Features

✅ 3×5 Bingo Card — generated randomly or filled manually by the player
✅ Duplicate Validation — prevents repeated numbers when entering custom cards
✅ Automatic Marking — drawn numbers are automatically crossed off
✅ Scoring System
- +10 pts per completed line
- +5 pts per completed diagonal (bonus only)
- +50 pts for full bingo (all 3 lines)
✅ Real-Time Updates — card and score refresh after each draw
✅ Modular Structure — separated into src/game and src/ui folders for clarity

## File Structure
Bingo-Project/
├── main.py
├── src/
│   ├── game/
│   │   ├── card.py        # Card generation & marking logic
│   │   ├── draw.py        # Random number drawing
│   │   ├── check.py       # Line, diagonal & bingo detection
│   │   └── score.py       # Scoring and bonuses
│   └── ui/
│       └── terminal.py    # Terminal input/output
└── tests/                 # (Optional) unit tests

## How to Run

1️⃣ Clone the repository
git clone https://github.com/oscarthesade/Bingo-Project.git
cd Bingo-Project

2️⃣ Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # (Mac/Linux)

3️⃣ Run the game
python3 main.py

4️⃣ Play!
- Choose to create your own card or get a random one
- Press Enter each round to draw a new number
- Watch your card fill and your score increase

## Scoring Example
Event                    Points
-----------------------   -------
Completing a line         +10
Completing a diagonal     +5
Full bingo (3 lines)      +50

## Contributors
Clement Standaert
Oscar @oscarthesade
(Add the rest of your team here)

## Future Improvements
- Multiplayer support
- Saving game history to CSV
- Colorized terminal interface (rich / colorama)
- Automated tests with pytest

“Luck is when preparation meets opportunity — so prepare your card 😉”
