def valid_move(board, orientation, row, col):
    if not isinstance(orientation, str) or orientation not in {"H", "V"}:
        return False
    if any(not isinstance(value, int) or isinstance(value, bool) for value in (row, col)):
        return False

    if orientation == "H":
        return (
            0 <= row <= board.rows
            and 0 <= col < board.cols
            and not board.horizontal[row][col]
        )

    return (
        0 <= row < board.rows
        and 0 <= col <= board.cols
        and not board.vertical[row][col]
    )


def completed_boxes(board, before):
    return len(board.completed - before)


def legal_moves(board):
    """Return every available move as (orientation, row, column)."""
    moves = []
    for row in range(board.rows + 1):
        for col in range(board.cols):
            if valid_move(board, "H", row, col):
                moves.append(("H", row, col))
    for row in range(board.rows):
        for col in range(board.cols + 1):
            if valid_move(board, "V", row, col):
                moves.append(("V", row, col))
    return moves


def _adjacent_boxes(board, orientation, row, col):
    if orientation == "H":
        return [(r, col) for r in (row - 1, row) if 0 <= r < board.rows]
    return [(row, c) for c in (col - 1, col) if 0 <= c < board.cols]


def _box_side_count(board, box_row, box_col):
    return sum((
        board.horizontal[box_row][box_col],
        board.horizontal[box_row + 1][box_col],
        board.vertical[box_row][box_col],
        board.vertical[box_row][box_col + 1],
    ))


def computer_move(board):
    """Choose a legal move: claim boxes, avoid opening them, then proceed."""
    moves = legal_moves(board)
    if not moves:
        return None

    # Taking a third side completes a box immediately and is always preferred.
    for move in moves:
        orientation, row, col = move
        if any(_box_side_count(board, r, c) == 3
               for r, c in _adjacent_boxes(board, orientation, row, col)):
            return move

    # Otherwise avoid creating a three-sided box that the opponent can take.
    for move in moves:
        orientation, row, col = move
        if all(_box_side_count(board, r, c) < 2
               for r, c in _adjacent_boxes(board, orientation, row, col)):
            return move

    # Every remaining move gives up at least one box; minimize the number opened.
    return min(
        moves,
        key=lambda move: sum(
            _box_side_count(board, r, c) == 2
            for r, c in _adjacent_boxes(board, *move)
        ),
    )
