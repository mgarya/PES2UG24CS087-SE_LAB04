import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from game import DotsAndBoxes
from rules import computer_move


class DotsAndBoxesTests(unittest.TestCase):
    def test_valid_horizontal_move(self):
        game = DotsAndBoxes(rows=1, cols=1)

        self.assertEqual(game.play_move("H", 0, 0), 0)
        self.assertTrue(game.board.horizontal[0][0])
        self.assertEqual(game.current, 1)

    def test_valid_vertical_move(self):
        game = DotsAndBoxes(rows=1, cols=1)

        self.assertEqual(game.play_move("V", 0, 1), 0)
        self.assertTrue(game.board.vertical[0][1])

    def test_invalid_and_repeated_moves_do_not_change_game(self):
        game = DotsAndBoxes(rows=1, cols=1)

        self.assertIsNone(game.play_move("X", 0, 0))
        self.assertIsNone(game.play_move("H", 2, 0))
        self.assertEqual(game.play_move("H", 0, 0), 0)
        scores = game.scores[:]
        current = game.current
        self.assertIsNone(game.play_move("H", 0, 0))
        self.assertEqual(game.scores, scores)
        self.assertEqual(game.current, current)

    def test_completing_box_scores_and_keeps_turn(self):
        game = DotsAndBoxes(rows=1, cols=1)
        for move in (("H", 0, 0), ("H", 1, 0), ("V", 0, 0)):
            game.play_move(*move)

        self.assertEqual(game.play_move("V", 0, 1), 1)
        self.assertEqual(game.scores, [0, 1])
        self.assertEqual(game.current, 1)
        self.assertIn((0, 0), game.board.completed)

    def test_completed_board_rejects_moves(self):
        game = DotsAndBoxes(rows=1, cols=1)
        for move in (("H", 0, 0), ("H", 1, 0), ("V", 0, 0), ("V", 0, 1)):
            game.play_move(*move)

        self.assertTrue(game.board.is_complete())
        self.assertIsNone(game.play_move("H", 0, 0))
        self.assertEqual(game.scores, [0, 1])


    def test_one_move_can_complete_two_boxes(self):
        game = DotsAndBoxes(rows=1, cols=2)

        # Fill every side except the shared vertical edge between the boxes.
        for move in (
            ("H", 0, 0), ("H", 0, 1),
            ("H", 1, 0), ("H", 1, 1),
            ("V", 0, 0), ("V", 0, 2),
        ):
            game.play_move(*move)

        boxes = game.play_move("V", 0, 1)
        self.assertEqual(boxes, 2)
        self.assertEqual(game.scores, [2, 0])
        self.assertEqual(game.current, 0)
        self.assertEqual(game.board.completed, {(0, 0), (0, 1)})

    def test_board_add_line_rejects_invalid_moves_without_mutation(self):
        game = DotsAndBoxes(rows=1, cols=1)

        with self.assertRaises(ValueError):
            game.board.add_line("H", 5, 0)
        self.assertFalse(game.board.horizontal[0][0])

        game.board.add_line("H", 0, 0)
        with self.assertRaises(ValueError):
            game.board.add_line("H", 0, 0)
        self.assertTrue(game.board.horizontal[0][0])

    def test_computer_takes_an_available_box(self):
        game = DotsAndBoxes(rows=1, cols=1)
        for move in (("H", 0, 0), ("H", 1, 0), ("V", 0, 0)):
            game.play_move(*move)

        self.assertEqual(computer_move(game.board), ("V", 0, 1))

    def test_cli_ignores_malformed_out_of_range_and_repeated_input(self):
        game = DotsAndBoxes(rows=1, cols=1)
        responses = iter((
            "n", "bad command", "H nope 0", "H 5 0", "H 0 0", "H 0 0",
            "H 1 0", "V 0 0", "V 0 1",
        ))
        output = StringIO()
        with patch("builtins.input", side_effect=lambda _prompt="": next(responses)):
            with redirect_stdout(output):
                game.run()

        self.assertTrue(game.board.is_complete())
        self.assertEqual(game.scores, [0, 1])
        self.assertIn("Invalid format.", output.getvalue())
        self.assertIn("Row and column must be nonnegative integers.", output.getvalue())
        self.assertEqual(output.getvalue().count("Invalid or already-used move."), 2)


if __name__ == "__main__":
    unittest.main()
