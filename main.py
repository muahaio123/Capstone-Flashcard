import pandas
import tkinter
import random

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")

try:
    data_csv = pandas.read_csv("data/words_to_learn.csv")  # resume the old not learnt words
except FileNotFoundError:  # if the user is using for the first time, create new file
    data_csv = pandas.read_csv("data/french_words.csv")  # take from the original list
except pandas.errors.EmptyDataError:  # if the user already learnt all the words, refresh the list
    data_csv = pandas.read_csv("data/french_words.csv")  # take from the original list

to_learn = data_csv.to_dict(orient="records")
current_word = None
card_flipped = None


# --------------------------- MOVE TO NEXT CARD ----------------------- #
def next_card():
    global current_word, card_flipped
    current_word = random.choice(to_learn)

    card_canvas.itemconfig(card_title, text="French", fill="black")
    card_canvas.itemconfig(card_word, text=current_word["French"], fill="black")
    card_canvas.itemconfig(card_img, image=card_front_img)  # change the card back to the front side

    card_flipped = window.after(ms=3000, func=flip_card)  # after 3s, flip the card


# --------------------------- FLIP CARD ----------------------- #
def flip_card():
    global current_word

    card_canvas.itemconfig(card_title, text="English", fill="white")
    card_canvas.itemconfig(card_word, text=current_word["English"], fill="white")
    card_canvas.itemconfig(card_img, image=card_back_img)  # change the card back to the front side


# --------------------------- RIGHT BUTTON ----------------------- #
def right_click():
    global card_flipped, to_learn, current_word
    window.after_cancel(card_flipped)  # cancel the old timer so that it will not stack
    next_card()

    to_learn.remove(current_word)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)


# --------------------------- WRONG BUTTON ----------------------- #
def wrong_click():
    global card_flipped
    window.after_cancel(card_flipped)  # cancel the old timer before moving to next card
    next_card()


# --------------------------- UI ----------------------- #
window = tkinter.Tk()
window.title("Flashcard Capstone - FRENCH")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

# image for the front card
card_front_img = tkinter.PhotoImage(file="images/card_front.png")
card_back_img = tkinter.PhotoImage(file="images/card_back.png")

# creating card canvas
card_canvas = tkinter.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_canvas.grid(row=0, column=0, columnspan=2)

# creating img, title and word on top of canvas
card_img = card_canvas.create_image(400, 263, image=card_front_img)
card_title = card_canvas.create_text(400, 150, font=LANGUAGE_FONT)
card_word = card_canvas.create_text(400, 263, font=WORD_FONT)

# right button should be on the right side
right_button_img = tkinter.PhotoImage(file="images/right.png")
right_button = tkinter.Button(image=right_button_img, highlightthickness=0, command=right_click)
right_button.grid(row=1, column=1)

# wrong button should be on the left side
wrong_button_img = tkinter.PhotoImage(file="images/wrong.png")
wrong_button = tkinter.Button(image=wrong_button_img, highlightthickness=0, command=wrong_click)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()
