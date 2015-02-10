import Tkinter as tk
import GameOfLife


class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # GUI elements
        self.button = tk.Button(text="Start Random Game", command=self.btn_start_callback)
        self.button.pack(side=tk.BOTTOM)
        self.play_field = tk.Canvas(self.parent, width=400, height=400)
        self.play_field.pack()
        self.display_grid()
        self.game = GameOfLife.GameOfLife(10, 10)
        self.generations = 0

    def display_grid(self, data=[]):
        self.play_field.delete(tk.ALL)
        for row in range(len(data)):
            for col in range(len(data[0])):
                rect = (row * 10, col * 10, (row + 1) * 10, (col + 1) * 10)
                if data[row][col] == 0:
                    self.play_field.create_rectangle(rect, fill='grey')
                else:
                    self.play_field.create_rectangle(rect, fill='blue')

    def update_game(self):
        data = self.game.next_generation()
        if data is not None:
            self.display_grid(data)
            self.after(10, self.update_game)

    def btn_start_callback(self):
        self.display_grid(self.game.game_field)
        self.update_game()


def main():
    root = tk.Tk()
    root.na
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()