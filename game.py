from board import Board


class Minesweeper:
    DIFFICULTIES = {
        "1": ("Easy", 5, 5, 3),
        "2": ("Medium", 6, 6, 6),
        "3": ("Hard", 8, 8, 12),
    }

    def __init__(self):
        self.board = None

    def choose_difficulty(self):
        print("Select difficulty:")
        print("1. Easy   (5x5, 3 mines)")
        print("2. Medium (6x6, 6 mines)")
        print("3. Hard   (8x8, 12 mines)")

        while True:
            choice = input("Difficulty (1-3): ").strip()

            if choice == "q":
                return False

            if choice in self.DIFFICULTIES:
                name, rows, cols, mines = self.DIFFICULTIES[choice]
                self.board = Board(rows, cols, mines)
                print(f"{name} mode selected.")
                return True

            print("Invalid choice. Enter 1, 2, or 3.")
    

    def display(self, reveal_mines=False):
        b = self.board
        print("\n   " + " ".join(str(c + 1) for c in range(b.cols)))
        for r in range(b.rows):
            cells = []
            for c in range(b.cols):
                pos = (r, c)
                if reveal_mines and pos in b.mines:
                    ch = "*"
                elif pos in b.flags:
                    ch = "F"
                elif pos not in b.revealed:
                    ch = "#"
                elif pos in b.mines:
                    ch = "*"
                else:
                    ch = str(b.adjacent_mines(r, c))
                cells.append(ch)
            print(f"{r + 1:2} " + " ".join(cells))

    def run(self):
        print("Minesweeper")

        if not self.choose_difficulty():
            return

        print("Commands: r row col | f row col | q")

        while True:
            self.display()
            raw = input("> ").strip().lower()
            if raw == "q":
                return
            parts = raw.split()
            if len(parts) != 3 or parts[0] not in {"r", "f"}:
                print("Use r row col or f row col.")
                continue
            try:
                r, c = int(parts[1]) - 1, int(parts[2]) - 1
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not self.board.in_bounds(r, c):
                print("Outside the board.")
                continue

            if parts[0] == "f":
                self.board.toggle_flag((r, c))
                continue

            before_revealed = len(self.board.revealed)

            if self.board.reveal((r, c)):
                self.display(reveal_mines=True)
                print("BOOM! You hit a mine.")
                return

            revealed_count = len(self.board.revealed) - before_revealed
            print(f"Revealed {revealed_count} cell{'s' if revealed_count != 1 else ''}.")

            if self.board.won():
                self.display()
                print("You cleared the board!")
                return
