# TetraShift - Readme

TetraShift is a Tetris game that uses a custom controller for user input. In addition to traditional keyboard controls, TetraShift utilizes gaze and blink detection for a more immersive and interactive gaming experience.

## Features

- Custom TetrisController class
- Gaze detection for left and right movement
- Blink detection for rotating the Tetris pieces
- Keyboard controls for traditional gameplay

## Dependencies

- Python 3
- Pygame
- OpenCV (cv2)
- Dlib
- Numpy

## Gamelogic

The Gamelogic class is responsible for handling the logic of the game, including checking for events, moving pieces, clearing rows, and setting new pieces. It initializes the game, handles sound and music, and checks the validity of moves. The game state, including the score and grid, is stored within instances of this class.

## Setup and Installation

1. Ensure you have Python 3 installed.
2. Install the required libraries by running:

```
pip install -r requirements.txt
```

3. Download the 'shape_predictor_68_face_landmarks.dat' file from [here](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) and place it in the same directory as the TetrisController.

## How to Play

1. Run the TetraShift game by running `main.py`:

```
python main.py
```

2. Use your gaze to move the Tetris pieces left and right.
3. Close your eyes for at least 3 seconds to rotate the Tetris pieces.
4. Alternatively, use the arrow keys on your keyboard for traditional controls.

## Troubleshooting

If you face any issues while running the game, consider the following common problems and solutions:

1. Make sure you have Python 3 installed and that you're using the correct version.
2. Ensure all the required libraries are installed. If you're facing issues with the installation, try to create a new virtual environment and install the requirements again.
3. If the gaze detection is not working, ensure that your webcam is functioning properly and is not being used by another application.

## Contributing

We welcome contributions from the open-source community. If you have ideas for improvements or bug fixes, please feel free to fork the repository and submit a pull request.

## Acknowledgments

We'd like to acknowledge the open-source community for providing the resources and libraries that made this project possible. Specifically, we would like to thank the creators of Pygame, OpenCV, and Dlib for their fantastic work.

## License

This project is licensed under the MIT License.

## Contact

If you have any questions or need further information, feel free to contact us.

## Thank You

Lastly, a huge thank you to everyone who uses and supports our project. We couldn't have done it without you. We appreciate any feedback you have and we're always looking to improve, so please don't hesitate to reach out!

Have fun playing TetraShift!
