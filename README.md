# Rock Paper Scissors — Gesture Controls

> **Work in progress:** the core game is implemented. Gesture recognition,
> error handling, and the user interface still need refinement.

Play rock paper scissors against a bot using your webcam. **MediaPipe** tracks
hand landmarks, simple rules classify your gestures, **OpenCV** handles the
camera, and **Pygame CE** renders the game. The bot chooses randomly using
`random.choice()`.

## Implemented Features

- Single-hand tracking, a mirrored camera preview, and hand landmark overlays.
- Recognition of rock, paper, scissors, and a gesture to start the next round.
- A game window with images for the player's and bot's moves.
- A five-second countdown that keeps the bot's move hidden until time runs out.
- Evaluation of standard valid moves and a running score.
- Color animations for wins, losses, and draws.
- Exit by closing the game window or pressing Escape in the camera window.

This overview is based on the source code. Full gameplay with a webcam has
not yet been verified.

## Installation and Setup

You need **64-bit Python 3.12**, a webcam, and a graphical desktop environment.
The code uses the legacy `mp.solutions.hands` API, so the dependencies pin
**MediaPipe 0.10.21**. Newer MediaPipe releases removed `mp.solutions`
([upstream issue](https://github.com/google-ai-edge/mediapipe/issues/6192)).
[Version 0.10.21 packages](https://pypi.org/project/mediapipe/0.10.21/)
include Python 3.12 support but do not cover Python 3.14.

### Windows (PowerShell)

Open a terminal in the project root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

You do not need to activate the environment or change the PowerShell execution
policy. If you already have an old `venv` directory, these commands create a
separate `.venv` environment with the correct Python version.

Dependency resolution has been verified with pip's `--dry-run` on Windows
with Python 3.12. This confirms package availability and compatible dependency
constraints; it does not verify installation or gameplay.

### Linux / macOS

With Python 3.12 installed, run these commands from the project root:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

These platforms have not yet been verified. Run the application from the project
root because it loads images using relative paths such as `Images/...`.

The project uses only `opencv-contrib-python`, which provides the `cv2` import
and is a MediaPipe dependency. Avoid installing another OpenCV variant in the
same environment: they share the same module. Headless variants also lack the
camera window support this application needs.

## How to Play

1. Start the application and allow camera access. A game window and camera
   preview will open.
2. Raise **only your index finger** to start a round.
3. Choose a gesture within five seconds and hold it until the countdown ends:
   - **Rock:** close all four fingers other than your thumb.
   - **Scissors:** raise your index and middle fingers and close the others.
   - **Paper:** raise all four fingers other than your thumb.
4. When the countdown ends, the bot's move is revealed, the score is updated,
   and the result animation plays.
5. Raise your index finger again to start the next round.

Your thumb does not determine the game gesture. Keep your hand in view with
fingers pointing upward and use good lighting. Scores are not saved after exit.

## Known Issues

- Losing sight of the hand does not reset the gesture, so the last detected
  move may be reused.
- Scissors detection does not strictly check that the ring and little fingers
  are closed.
- A continue gesture or an empty move at the end of the countdown has no clearly
  defined outcome; the previous round's result may remain active.
- An unknown gesture labeled `nic` currently awards a point to the bot.
- Animations use `time.sleep()`, temporarily pausing camera updates and event handling.
- An unavailable camera causes the application to exit without an explanatory message.
- Images use fixed paths and dimensions. The interface needs a layout review,
  especially the long score line.
- Automated tests and CI are missing.

If you see `AttributeError: module 'mediapipe' has no attribute 'solutions'`,
check that you are using Python from the new `.venv` environment and have
installed the dependencies from this `requirements.txt`.

## Roadmap

- [ ] Reset the gesture when hand tracking is lost and improve move classification.
- [ ] Separate round evaluation from detection and handle invalid input explicitly.
- [ ] Replace blocking animations with timing in the game loop.
- [ ] Add clear error messages for camera and image-loading failures.
- [ ] Split `main.py` into smaller components and add tests for game rules.
- [ ] Refine the interface and add a screenshot or short demo.
- [ ] Migrate to the supported MediaPipe Tasks API.
- [ ] Document the sources and licensing terms of images in `Images/`.

These are suggested next steps based on the code. This folder contains no Git
history or task tracking that could confirm which work is currently in progress.

## Project Structure

```text
RockPaperScrisors/
├── main.py           # Camera, gesture detection, game logic, and rendering
├── Images/           # Gesture and control images (Paper has no extension)
├── requirements.txt  # Direct dependencies with pinned versions
├── .gitignore        # Environments, caches, and local configuration
├── LICENSE           # MIT license for the project's original code
└── README.md
```

## Contributing

Bug fixes and small improvements are welcome. For gesture detection changes,
describe the gesture, conditions, and expected behavior. When reporting a bug,
include your Python version, operating system, and error message.

## License

The project's original code is available under the [MIT license](LICENSE).
Dependencies retain their own licenses. The sources and redistribution rights
of images in `Images/` have not yet been documented; the MIT license does not
grant rights to any third-party images.
