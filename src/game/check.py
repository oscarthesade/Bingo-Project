# src/game/check.py

def count_lines(marked):
    """
    Count how many full rows are completely True.
    marked is a 2D list of booleans, e.g. 3x5.
    """
    count = 0
    for row in marked:
        if all(row):
            count += 1
    return count


def is_bingo(marked):
    """
    For a 3x5 card, bingo = all rows complete.
    """
    total_rows = len(marked)
    return count_lines(marked) == total_rows


def count_diagonals(marked):
    """
    Count full diagonals. Only works if board is square.
    For 3x5 this will normally return 0, but we keep it
    so we can change to 5x5 later or give partial points.
    """
    rows = len(marked)
    cols = len(marked[0])

    diags = 0

    # only count diagonals if it's square
    if rows == cols:
        # main diagonal
        if all(marked[i][i] for i in range(rows)):
            diags += 1
        # anti-diagonal
        if all(marked[i][cols - 1 - i] for i in range(rows)):
            diags += 1

    return diags
