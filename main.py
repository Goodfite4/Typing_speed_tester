import random
from tkinter import *
from time import time


class Panel(Tk):
    def __init__(self):
        super(Panel, self).__init__()
        self.title("Image Watermarker")
        self.minsize(700, 350)
        self.maxsize(700, 350)
        # Make Canvas fit all the empty space
        self.rowconfigure(index=1, weight=1)
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=1)

        self.word_list = []
        with open('words.txt') as words:
            all_words = list(words)
            for i in range(10):
                self.word_list.append((random.choice(all_words)).strip("\n") + " ")

        self.string_to_type = "".join(self.word_list)

        self.typed_string = ""
        self.incorrect_typed_string = ""
        self.stored_chars = ""

        self.untyped_string_left = Label(text=self.typed_string, fg="green", font=("Helvetica", 18), justify="right")
        self.untyped_string_left.grid(row=1, column=0)

        self.untyped_string_middle = Label(text=self.incorrect_typed_string, anchor="w", fg="red",
                                           font=("Helvetica", 18))
        self.untyped_string_middle.grid(row=1, column=1)

        self.untyped_string_right = Label(text=self.string_to_type, anchor="w", font=("Helvetica", 18), justify="left")
        self.untyped_string_right.grid(row=1, column=2)

        self.button = Button(text="Reset Test", command=self.restart_test)
        self.button.grid(row=0, column=0, columnspan=3, pady=50)

        self.start_time = None
        self.end_time = None

        self.bind("<KeyPress>", self.run_script)
        print(self.bind)

    def run_script(self, event):
        key = event.char
        if key and len(self.stored_chars) == 0:
            if self.start_time is None:
                self.start_time = time()

            if key == self.string_to_type[0]:
                self.string_to_type = self.string_to_type[1:]
                self.typed_string += key

            elif key == "\b":
                try:
                    self.string_to_type = self.stored_chars[-1] + self.string_to_type
                except IndexError:
                    pass
                if len(self.incorrect_typed_string) == 1:
                    self.incorrect_typed_string = ""
                else:
                    self.incorrect_typed_string = self.incorrect_typed_string[1:]
                self.stored_chars = self.stored_chars[0:-1]

            elif key != self.string_to_type[0] and self.string_to_type[0] != " ":
                self.stored_chars += self.string_to_type[0]
                self.string_to_type = self.string_to_type[1:]
                self.incorrect_typed_string += self.stored_chars

        elif key == "\b":
            try:
                self.string_to_type = self.stored_chars[-1] + self.string_to_type
            except IndexError:
                pass
            if len(self.incorrect_typed_string) == 1:
                self.incorrect_typed_string = ""
            else:
                self.incorrect_typed_string = self.incorrect_typed_string[1:]
            self.stored_chars = self.stored_chars[0:-1]

        if len(self.string_to_type) > 1:
            self.end_time = time()

        self.untyped_string_left.config(text=self.typed_string)
        self.untyped_string_middle.config(text=self.incorrect_typed_string)
        self.untyped_string_right.config(text=self.string_to_type)
        elapsed_time = round(self.end_time - self.start_time, 1)
        try:
            wpm = round(10/(elapsed_time/60), 1)
        except ZeroDivisionError:
            wpm = 0
        elapsed_time_tag = Label(text=f"elapsed_time: {elapsed_time} seconds | wpm: {wpm}", font=("Helvetica", 15))
        elapsed_time_tag.grid(row=2, column=0, columnspan=3)

    def restart_test(self):
        window.destroy()
        window.__init__()


window = Panel()

window.mainloop()
