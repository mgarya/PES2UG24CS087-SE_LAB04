# Scenario 23 - Dots and Boxes

## Overview

Dots and Boxes is a turn-based grid game. Players draw one line at a time between adjacent dots. Completing the fourth side of a box claims that box, earns a point, and gives the same player another turn.

The starter project is deliberately split into separate modules for game flow, board state, and rule validation. Read the existing implementation carefully before changing it.

## How to run

From this folder:

```text
python main.py
```

Enter moves in the form:

```text
H row column
```

or

```text
V row column
```

Rows and columns start at zero.

## Task 1 — Reproduce and investigate the bug

Run several games and deliberately create situations where a move completes one or more boxes.

Compare the score and turn behaviour before and after box completion. Identify the incorrect behaviour, trace it through the board and game-state logic, and fix it without replacing the modular structure.

Your before-change video should capture the broken behaviour clearly.

## Task 2 — Add a meaningful feature

Add a substantial gameplay feature that requires changes across more than one module.

The feature should make the game more complete rather than simply changing text or appearance. It should interact correctly with the existing board state and turn/score system.

## Task 3 — Validation and robustness

Strengthen input and game-state handling.

The program should safely handle malformed commands, invalid coordinates, repeated lines, and moves made after the board is already complete. Invalid input must not corrupt the board or score.

## Task 4 — Testing and quality

Create or expand automated tests covering the important game rules.

Include tests for at least:
- a valid horizontal move
- a valid vertical move
- an invalid/repeated move
- completion of a box
- the end-of-game condition

Document the changes you made and any design decisions that were important to the solution.

## Implementation notes

### Task 1 — Investigation and fix

The committed starter checkout was tested before making the final changes. Three
complete scripted 2-by-2 games produced scores of 2–2, 4–0, and 0–4, so the
box-scoring/turn behavior described in the task was not reproducible: box
completion correctly increased the current player's score and retained that
player's turn. Rather than inventing a broken behavior, the implementation
keeps the rule explicit in `DotsAndBoxes.play_move`: `Board.add_line` returns
the number of newly completed boxes; the game adds that count to the score and
only changes the turn when the count is zero. This also correctly handles a
single move that completes two adjacent boxes.

### Task 2 — Meaningful feature: computer opponent

The game now supports a human-vs-computer mode. The computer logic lives in
`rules.py`, while `game.py` integrates it with the existing turn and scoring
flow. Its heuristic:

1. takes an immediately available box when possible;
2. otherwise avoids moves that create an immediate box for the opponent; and
3. when every move creates a risk, minimizes the number of boxes opened.

This is intentionally a simple heuristic, not a perfect solver.

### Task 3 — Validation and robustness

- `valid_move` checks orientation, type, range, and whether the line is unused.
- `Board.add_line` validates again before mutating board state, so callers cannot
  accidentally corrupt the board with an invalid move.
- The CLI rejects malformed commands, non-numeric coordinates, out-of-range
  coordinates, repeated lines, and moves after the board is complete.
- Invalid input does not change scores, turns, or board state.

### Task 4 — Testing and quality

`test_game.py` uses Python's built-in `unittest` framework. The suite covers:

- valid horizontal and vertical moves;
- invalid and repeated moves;
- box completion and retained turns;
- a move that completes two boxes;
- completed-board rejection;
- direct board-level validation; and
- the computer's box-taking decision.

Board sizes can be selected when constructing `DotsAndBoxes`, for example
`DotsAndBoxes(rows=3, cols=4)`. The command-line game uses the default 2-by-2
board.

## Validation results

Run from the project folder:

```text
python -m unittest -v
```

All tests pass. The implementation uses only the Python standard library, so
no third-party installation is required.

A complete scripted human-vs-computer 2-by-2 game was also exercised; the
board reached the end-of-game state with all four boxes scored and the final
score/turn behavior remained consistent.

For the required 10-second videos, record the baseline behavior from the
original starter checkout before showing the completed implementation. The
starter checkout in this submission did not reproduce the stated scoring bug,
so the before-change video must not be fabricated.

## Constraints

- Keep the project modular.
- Do not replace the game with an unrelated implementation.
- Preserve the existing gameplay.
- Avoid putting all new logic into `main.py`.
- Keep third-party dependencies out unless there is a clear need for them.

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
