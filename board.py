class Board:
    def __init__(self, rows=2, cols=2):
        if not isinstance(rows, int) or isinstance(rows, bool) or rows < 1:
            raise ValueError("rows must be a positive integer")
        if not isinstance(cols, int) or isinstance(cols, bool) or cols < 1:
            raise ValueError("cols must be a positive integer")
        self.rows = rows
        self.cols = cols
        self.horizontal = [[False] * cols for _ in range(rows + 1)]
        self.vertical = [[False] * (cols + 1) for _ in range(rows)]
        self.completed = set()

    def add_line(self, orientation, row, col):
        # Import locally to keep the board/rules dependency one-way at import time.
        from rules import valid_move

        if not valid_move(self, orientation, row, col):
            raise ValueError("move is invalid or the line is already drawn")
        before = len(self.completed)
        if orientation == "H":
            self.horizontal[row][col] = True
        elif orientation == "V":
            self.vertical[row][col] = True
        else:  # valid_move already rejects this; retained as a defensive guard.
            raise ValueError("orientation must be H or V")
        self._update_completed()
        return len(self.completed) - before

    def _update_completed(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (
                    self.horizontal[r][c]
                    and self.horizontal[r + 1][c]
                    and self.vertical[r][c]
                    and self.vertical[r][c + 1]
                ):
                    self.completed.add((r, c))

    def is_complete(self):
        total = self.rows * (self.cols + 1) + self.cols * (self.rows + 1)
        used = sum(map(sum, self.horizontal)) + sum(map(sum, self.vertical))
        return used == total

    def display(self, scores, current):
        print()
        print(f"Scores: P1={scores[0]}  P2={scores[1]} | Turn: P{current + 1}")

        for r in range(self.rows + 1):
            print(".".join("---" if self.horizontal[r][c] else "   " for c in range(self.cols)))
            if r < self.rows:
                middle = []
                for c in range(self.cols + 1):
                    wall = "|" if self.vertical[r][c] else " "
                    middle.append(wall)
                    if c < self.cols:
                        middle.append(" " + ("X" if (r, c) in self.completed else " ") + " ")
                print("".join(middle))
        print()
