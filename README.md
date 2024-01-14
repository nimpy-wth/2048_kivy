# 2048 Game
## Description

This application is a classic implementation of the 2048 game using the Kivy framework. Dive straight into the game grid, where the goal is to reach the 2048 tile by merging tiles with the same number.

## Features
- Swipe or Arrow Key Controls : Use either swipe gestures on a touch screen or the arrow keys on your keyboard to move tiles in different directions.
    - Number Merging : Combine tiles with the same number by sliding them together.
    - Dynamic Number and Color Updates : Tiles change colors and font sizes based on their values, creating a visual progression as you merge them.
    - Game Over Condition : The game ends when the board is filled, and no more moves are possible.
    - Winning Condition : Achieve victory by creating the elusive 2048 tile!
    - Restart Button : Easily start a new game without closing the application.
    - Exit Button : Conveniently close the game when you're ready to stop playing.

## Instructions
   ### Playing the Game:
- Launch the Game : Run the main.py file to start the game.
    - Move Tiles :
        - Use the arrow keys (up, down, left, right) on your keyboard.
        - Or, swipe in the desired direction on a touch screen.
    - Merge Tiles : Swipe or move tiles to combine those with the same number.
    - Aim for 2048 : Keep merging tiles to create higher-value tiles and ultimately reach the 2048 tile to win.
   
   ### Game Over:
    - The game ends when the board is filled, and no more moves are possible.
    - A "Game Over" popup appears with options to restart or exit.

   #### Restart Option:
    - Restart the game at any time using the "Restart" button.

   ### Exit Button:
    - Close the game window or use the "Exit" button to end the game.

   ### Confirmation Popups:
    - Prevent accidental restarts or exits with confirmation popups.

## Installation
  ### Dependencies
  - Python : Ensure you have Python installed on your system.
  - Kivy : Install Kivy using pip:
  
```Copy code
pip install kivy
```
  ### Running the Application

  - Download Files : Clone the repository or download the source code files (main.py, game.kv, board.png, cell.png, game_over.mp3).
  - Navigate to Directory : Open a terminal or command prompt and navigate to the directory containing the downloaded files.
  - Run the Game : Execute the following command to start the game:

  ```Copy code
python main.py
```