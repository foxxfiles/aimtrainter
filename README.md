# Aim Trainer

A customizable aim training program built with Pygame to help improve mouse precision and control.

## Features

- **Progressive Difficulty**: 100 increasingly challenging levels that adjust target size, recoil, and timing requirements
- **Custom Images**: Load your own image directory for visual rewards
- **Score Tracking**: Persistent high score leaderboard stored in JSON format
- **Customizable Settings**: Adjust initial target diameter through config file
- **Mouse Control**: Toggle mouse capture with F12 key


![Aimtrainer](https://github.com/foxxfiles/aimtrainter/blob/main/images/ui.png)

## How It Works

The aim trainer challenges you to keep your cursor within a target circle while holding down the left mouse button. As you progress through levels, the target circle becomes smaller, recoil gets stronger, and the required time on target increases.

### Game Mechanics

1. **Target Circle**: A red circular target appears in the center of the screen
2. **Recoil Simulation**: The cursor automatically drifts, simulating weapon recoil
3. **Visual Reward**: When on target with left-click pressed, your chosen image appears
4. **Level Progression**: Complete a level by staying on target for the required time
5. **Score System**: Earn points for completing levels, with higher levels worth more points

## Installation

### Prerequisites
- Python 3.x
- Pygame
- Tkinter (usually included with Python)

### Setup
1. Clone the repository:
```
git clone https://github.com/foxxfilesaim-trainer.git
cd aim-trainer
```

2. Install dependencies:
```
pip install pygame
```

3. Run the program:
```
python aimtrainer.py
```

## Configuration

The program uses two JSON files:

### config.json
Controls initial target diameter (default is 12 if not specified):
```json
{
  "diametro_inicial": 16
}
```

### score.json
Stores user high scores:
```json
{
  "username1": 1200,
  "username2": 950
}
```

## Controls

- **Left Mouse Button**: Hold to accumulate time on target
- **F12**: Toggle mouse capture/release
- **ESC**: Exit the program

## UI Elements

- **Top Left Button**: Change image directory
- **Top Right Button**: Skip current level
- **Right Side Panel**: Shows current score, high score, and leaderboard
- **Bottom Status Bar**: Displays current level and target time information

## Customization

### Image Directory
You can use your own images as visual rewards by selecting a directory containing supported image formats (.png, .jpg, .jpeg, .bmp, .gif).

### Target Size
Modify the initial target diameter in config.json to make the game easier or more challenging.


## Acknowledgments

- Created to help gamers improve mouse control and precision
- Inspired by FPS aim training applications

