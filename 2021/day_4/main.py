import fileinput
from typing import Iterator, List, Optional, Tuple


BOARD_HEIGHT = 5
BOARD_WIDTH  = 5

VERTICAL_MASK   = 0b00001_00001_00001_00001_00001
HORIZONTAL_MASK = 0b00000_00000_00000_00000_11111


FG_YELLOW = "\033[33m"
END = "\033[0m"


class Board:
    board: List[List[int]]
    marked: int

    def __init__(self, raw_rows: Iterator[str]) -> None:
        self.board = [
            [int(cell) for cell in row.split()]
            for row in raw_rows
        ]
        self.marked = 0

    def __str__(self) -> str:
        return "\n".join(
            " ".join(
                f"{FG_YELLOW if self.cell_is_marked(i, j) else ''}{cell:>2}{END}"
                for j, cell in enumerate(row)
            )
            for i, row in enumerate(self.board)
        )

    def cell_is_marked(self, row: int, col: int) -> bool:
        return (self.marked >> (col + row * BOARD_WIDTH)) & 1 == 1

    def mark_number(self, number: int) -> None:
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == number:
                    self.marked |= 1 << (j + i * BOARD_WIDTH)
                    # Assumng each number appears at most
                    # once per board.
                    break

    def has_bingo(self) -> bool:
        for i in range(BOARD_HEIGHT):
            mask = HORIZONTAL_MASK << (i * BOARD_WIDTH)
            if self.marked & mask == mask:
                return True

        for j in range(BOARD_WIDTH):
            mask = VERTICAL_MASK << j
            if self.marked & mask == mask:
                return True

        return False

    def sum_unmarked_cells(self) -> int:
        return sum(
            cell
            for i, row in enumerate(self.board)
            for j, cell in enumerate(row)
            if not self.cell_is_marked(i, j)
        )


class BoardSet:

    def __init__(self, raw) -> None:
        self.boards_in_play = []
        self.winning_boards = []
        for raw_board in zip(*(iter(raw),) * BOARD_HEIGHT):
            self.boards_in_play.append(Board(raw_board))

    def __str__(self) -> str:
        return "\n\n".join(str(board) for board in self.boards_in_play)
    
    def mark_number(self, number):
        boards_for_next_round = []
        for board in self.boards_in_play:
            board.mark_number(number)

            if board.has_bingo():
                self.winning_boards.append((board, number))
            else:
                boards_for_next_round.append(board)

        self.boards_in_play = boards_for_next_round


def play_bingo(boards: BoardSet, numbers: Iterator[int]) -> List[Tuple[Board, int]]:
    for i, number_called in enumerate(numbers, 1):
        boards.mark_number(number_called)

        if len(boards.boards_in_play) == 0:
            break

    return boards.winning_boards


def print_results(board: Board, number_called: int) -> None:
    sum_of_unmarked = board.sum_unmarked_cells()
    product = number_called * sum_of_unmarked
    print(board)
    print(f"{number_called=}, {sum_of_unmarked=}, {product=}")


if __name__ == "__main__":

    rows = [
        stripped_row
        for row in fileinput.input()
        if (stripped_row := row.strip()) != ""
    ]

    called_numbers = (
        int(n) 
        for n in rows.pop(0).split(",")
    )

    boards = BoardSet(rows)
    results = play_bingo(boards, called_numbers)

    print("Part 1")
    print_results(*results[0])

    print("\nPart 2")
    print_results(*results[-1])

