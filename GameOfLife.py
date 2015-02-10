import random
import xxhash


class GameOfLife(object):
    def __init__(self, row, col, game_field=None):
        # Setup Game
        self.row = row
        self.col = col
        self.game_field = game_field
        self.field_hashes = set()
        if game_field is None:
            # Use List comprehension to generate a 2D List with random Data -> Lightning fast
            self.game_field = [[random.randint(0, 1) for _ in range(col)] for row in range(row)]

    def next_generation(self):
        # first step, count neighbours
        neighbours_map = [[0 for _ in range(self.col)] for _ in range(self.row)]
        for row in range(self.row):
            for col in range(self.col):
                neighbours_map[row][col] = self.count_neighbours(row, col)
        # second step, calculate new generation
        for row in range(self.row):
            for col in range(self.col):
                if self.is_cell_living(row, col):
                    if neighbours_map[row][col] < 2:
                        # cell dies: under population
                        self.game_field[row][col] = 0
                    if neighbours_map[row][col] == 2 or neighbours_map[row][col] == 3:
                        # cell keeps alive
                        self.game_field[row][col] = 1
                    if neighbours_map[row][col] > 3:
                        # cell dies: over population
                        self.game_field[row][col] = 0
                else:
                    if neighbours_map[row][col] == 3:
                        # cell is born
                        self.game_field[row][col] = 1
        if self.is_game_static():
            return None
        else:
            return self.game_field

    def is_cell_living(self, row, col):
        return self.game_field[row][col]

    def is_game_static(self):
        generation_hash = xxhash.xxh64(str(self.game_field)).hexdigest()
        if generation_hash in self.field_hashes:
            return True
        else:
            self.field_hashes.add(generation_hash)
            return False

    def life_finder(self):
        pass

    def count_neighbours(self, row, col):
        count = 0
        """
        The game field is a donut world. All edges are glued together, so the game field is theoretical
        infinite. let me explain the two concepts used here:

        1. The positive neighbour.
           I use a modulo operator to limit the list index. If we want the poitive nightbour of a cell
           on the outer bounds our index will be max_list_index + 1. This will Throw index out of
           bounds error. But the Modulo operator will set the index of the positive neighbour
           to 0 if the value is max_index + 1.

        2. The list index -1.
           Python has a nice feature. The list Index 0 is the first element. The list index -1 is
           the last element. So if we want to get the negative neighbour on index 0 we get automatically
           the last element of the list. Nothing to do here.
        """
        pos_neighbour_row = (row + 1) % self.row
        pos_neighbour_col = (col + 1) % self.col
        count += self.is_cell_living(row - 1, col)                  # top
        count += self.is_cell_living(row, pos_neighbour_col)        # right
        count += self.is_cell_living(row, col - 1)                  # left
        count += self.is_cell_living(pos_neighbour_row, col)        # down
        count += self.is_cell_living(row - 1, pos_neighbour_col)    # top right
        count += self.is_cell_living(row - 1, col - 1)              # top left
        count += self.is_cell_living(pos_neighbour_row, col - 1)    # down left
        count += self.is_cell_living(pos_neighbour_row, pos_neighbour_col)  # down right
        return count