from board import Board
from rules import valid_move, computer_move

class DotsAndBoxes:
    def __init__(self, rows=2, cols=2, vs_computer=False):
        self.board = Board(rows, cols)
        self.current = 0
        self.scores = [0, 0]
        self.vs_computer = vs_computer

    def play_move(self, orientation, row, col):
        """Apply a legal move, returning boxes claimed or None if invalid."""
        if self.board.is_complete() or not valid_move(self.board, orientation, row, col):
            return None

        boxes = self.board.add_line(orientation, row, col)
        if boxes:
            self.scores[self.current] += boxes
        else:
            self.current = 1 - self.current
        return boxes

    def _read_opponent_choice(self):
        while True:
            try:
                choice = input("Play against the computer? (y/n): ").strip().lower()
            except EOFError:
                return
            if choice in {"y", "yes"}:
                self.vs_computer = True
                return
            if choice in {"n", "no"}:
                self.vs_computer = False
                return
            print("Enter y or n.")

    def run(self):
        print("Dots and Boxes")
        self._read_opponent_choice()
        print("Enter moves as H row col or V row col.")
        print("Rows and columns start at 0.")
        print("Example: H 0 1")

        while not self.board.is_complete():
            self.board.display(self.scores, self.current)
            if self.vs_computer and self.current == 1:
                move = computer_move(self.board)
                if move is None:
                    break
                orientation, row, col = move
                print(f"Computer plays: {orientation} {row} {col}")
                self.play_move(*move)
                continue

            try:
                raw = input(f"Player {self.current + 1}, move: ").strip().upper()
            except EOFError:
                print("Input ended. Game stopped.")
                return
            parts = raw.split()

            if len(parts) != 3:
                print("Invalid format.")
                continue

            orientation, row, col = parts
            if not row.isdigit() or not col.isdigit():
                print("Row and column must be nonnegative integers.")
                continue

            row, col = int(row), int(col)
            boxes = self.play_move(orientation, row, col)
            if boxes is None:
                print("Invalid or already-used move.")
                continue
            if boxes:
                print(f"Player {self.current + 1} completed {boxes} box(es) and plays again.")

        self.board.display(self.scores, self.current)
        print("Game over!")
        if self.scores[0] == self.scores[1]:
            print("The game is a draw.")
        else:
            winner = 1 if self.scores[0] > self.scores[1] else 2
            print(f"Player {winner} wins!")
