from tkinter import *
from tkinter import messagebox
from math import floor
import simpleaudio as sa

DARK_RED = "#F47C7C"
LIGHT_RED = "#FAD4D4"
FONT = ("Courier", 50, "bold")


class Pomodoro:
    def __init__(self, root):

        # setting up the main window
        self.root = root
        self.root.title("Pomodoro")
        self.root.config(bg=LIGHT_RED, pady=20)

        # time info
        self.timer = None
        self.isPaused = False
        self.count = 0
        self.reps = 0
        self.focus_stages = 0
        self.focus_secs = 25 * 60
        self.short_break_secs = 5 * 60
        self.long_break_secs = 20 * 60

        # graphic assets
        self.one_sprout = PhotoImage(file="sprout.png")
        self.two_vegetative = PhotoImage(file="vegetative.png")
        self.three_flowering = PhotoImage(file="flowering.png")
        self.four_fruit_formation = PhotoImage(file="fruit-formation.png")
        self.five_mature_fruiting = PhotoImage(file="mature_fruiting.png")
        self.bloody_mary = PhotoImage(file="bloody-mary.png")
        self.ketchup = PhotoImage(file="ketchup.png")
        self.grey_tomato = PhotoImage(file="tomato-grayscale.png")
        self.red_tomato = PhotoImage(file="tomato.png")
        self.pause_img = PhotoImage(file="pause.png")
        self.play_img = PhotoImage(file="play.png")
        self.unpause_img = PhotoImage(file="pause_grey.png")
        self.unplay_img = PhotoImage(file="play_grey.png")
        self.restart_img = PhotoImage(file="restart.png")

        self.ding_sound = sa.WaveObject.from_wave_file("ding.wav")

        # UI SET-UP
        self.canvas = Canvas(width=500, height=200, bg=LIGHT_RED, highlightthickness=0)
        self.bg_image = self.canvas.create_image(250, 100, image=self.one_sprout)
        self.canvas.grid(column=0, columnspan=5, row=1)

        self.phase_label = Label(text="POMODORO", font=FONT, bg=LIGHT_RED, fg=DARK_RED)
        self.phase_label.grid(column=0, columnspan=5, row=0)

        self.counter_label = Label(text="00:00", font=FONT, bg=LIGHT_RED, fg=DARK_RED)
        self.counter_label.config(pady=40)
        self.counter_label.grid(column=0, columnspan=5, row=2)

        # finished / unfinished focus sessions counters
        self.phase_1 = Label(image=self.grey_tomato, bg=LIGHT_RED)
        self.phase_1.grid(column=0, row=3)
        self.phase_2 = Label(image=self.grey_tomato, bg=LIGHT_RED)
        self.phase_2.grid(column=1, row=3)
        self.phase_3 = Label(image=self.grey_tomato, bg=LIGHT_RED)
        self.phase_3.grid(column=2, row=3)
        self.phase_4 = Label(image=self.grey_tomato, bg=LIGHT_RED)
        self.phase_4.grid(column=3, row=3)
        self.phase_5 = Label(image=self.grey_tomato, bg=LIGHT_RED)
        self.phase_5.grid(column=4, row=3)

        # empty spaces so the UI isn't as crowded
        self.separator = Label(bg=LIGHT_RED)
        self.separator.grid(column=1, row=4)
        self.separator_2 = Label(bg=LIGHT_RED)
        self.separator_2.grid(column=1, row=5)

        # start, pause, and restart buttons
        self.start_button = Button(image=self.play_img, width=30, height=30, command=self.start_timer)
        self.start_button.grid(column=1, row=6)

        self.pause_button = Button(image=self.unpause_img, width=30, height=30)
        self.pause_button.grid(column=2, row=6)

        self.restart_button = Button(image=self.restart_img, width=30, height=30, command=self.reset_timer)
        self.restart_button.grid(column=3, row=6)

    # starting the timer
    def start_timer(self):
        self.start_button.config(image=self.unplay_img, command="")
        self.pause_button.config(image=self.pause_img, command=self.pause_timer)
        self.reps += 1
        self.ding_sound.play()
        self.color_tomato()

        if self.reps == 10:     # pomodoro session finished
            self.canvas.itemconfig(self.bg_image, image=self.ketchup)
            self.phase_label.config(text="FINISHED")

        elif self.reps == 8:    # long break
            self.canvas.itemconfig(self.bg_image, image=self.bloody_mary)
            self.phase_label.config(text="BREAK")
            self.countdown(self.long_break_secs)

        elif self.reps % 2 == 0:  # short break
            self.canvas.itemconfig(self.bg_image, image=self.bloody_mary)
            self.phase_label.config(text="BREAK")
            self.countdown(self.short_break_secs)
        else:
            self.canvas.itemconfig(self.bg_image, image=self.one_sprout)
            self.phase_label.config(text="FOCUS")
            self.countdown(self.focus_secs)

    # changes the color of counter tomatoes
    def color_tomato(self):
        if self.reps == 2:
            self.phase_1.config(image=self.red_tomato)
        elif self.reps == 4:
            self.phase_2.config(image=self.red_tomato)
        elif self.reps == 6:
            self.phase_3.config(image=self.red_tomato)
        elif self.reps == 8:
            self.phase_4.config(image=self.red_tomato)
        elif self.reps == 10:
            self.phase_5.config(image=self.red_tomato)

    # the countdown mechanism
    def countdown(self, count):
        if not self.isPaused:
            self.count = count
            minutes = floor(count / 60)
            seconds = count % 60
            self.counter_label.config(text=f"{minutes:02d}:{seconds:02d}")

            if count > 0:
                # changing the phases of growth every five minutes in work mode:
                if self.reps % 2 != 0:
                    if count == 20 * 60:
                        self.canvas.itemconfig(self.bg_image, image=self.two_vegetative)
                    if count == 15 * 60:
                        self.canvas.itemconfig(self.bg_image, image=self.three_flowering)
                    if count == 10 * 60:
                        self.canvas.itemconfig(self.bg_image, image=self.four_fruit_formation)
                    if count == 5 * 60:
                        self.canvas.itemconfig(self.bg_image, image=self.five_mature_fruiting)

                self.timer = self.root.after(1000, self.countdown, count-1)
            else:
                self.start_timer()

    # pausing and unpausing the timer
    def pause_timer(self):
        self.isPaused = True
        self.start_button.config(image=self.play_img, command=self.unpause_timer)
        self.pause_button.config(image=self.unpause_img, command="")

    def unpause_timer(self):
        self.isPaused = False
        self.start_button.config(image=self.unplay_img, command="")
        self.pause_button.config(image=self.pause_img, command=self.pause_timer)
        self.countdown(self.count)

    # resetting the timer and UI
    def reset_timer(self):

        self.pause_timer()
        should_reset = messagebox.askokcancel(title="Reset timer?",
                                              message="Are you sure you want to reset? All your progress will be lost.")

        if should_reset:
            self.count = 0
            self.reps = 0
            self.root.after_cancel(self.timer)
            self.isPaused = False
            self.start_button.config(image=self.play_img, command=self.start_timer)
            self.pause_button.config(image=self.unpause_img, command=self.pause_timer)
            self.phase_label.config(text="FOCUS")
            self.canvas.itemconfig(self.bg_image, image=self.one_sprout)
            self.counter_label.config(text="00:00")
            self.phase_1.config(image=self.grey_tomato)
            self.phase_2.config(image=self.grey_tomato)
            self.phase_3.config(image=self.grey_tomato)
            self.phase_4.config(image=self.grey_tomato)
            self.phase_5.config(image=self.grey_tomato)

        else:
            self.unpause_timer()

    def main(self):
        self.root.mainloop()


if __name__ == '__main__':
    my_pomo = Pomodoro(Tk())
    my_pomo.main()
