import tkinter as tk
import requests
import random
import html

API_URL = "https://opentdb.com/api.php?amount=10&category=28&difficulty=medium&type=multiple"

class TriviaGame:
    def __init__(self, root):
        self.root = root
        self.questions = []
        self.current_question = None
        self.question_label = None
        self.answers_buttons = []
        self.score_label = None
        self.score = 0

        self.get_questions()

        self.question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=400)
        self.question_label.pack(pady=20)

        for _ in range(4):
            answer_button = tk.Button(root, text="", font=("Arial", 12), wraplength=400)
            answer_button.pack(pady=5)
            answer_button.config(command=lambda button=answer_button: self.check_answer(button))
            self.answers_buttons.append(answer_button)

        self.score_label = tk.Label(root, text="Score: {}".format(self.score), font=("Arial", 12))
        self.score_label.pack(pady=10)

        self.next_question()

    def get_questions(self):
        response = requests.get(API_URL)
        data = response.json()
        self.questions = data["results"]

    def next_question(self):
        if len(self.questions) == 0:
            self.question_label.config(text="Trivia Game Over! Final Score: {}".format(self.score))
            for button in self.answers_buttons:
                button.config(state="disabled")
        else:
            self.current_question = self.questions.pop(0)
            self.question_label.config(text=html.unescape(self.current_question["question"]))

            answers = self.current_question["incorrect_answers"] + [self.current_question["correct_answer"]]
            random.shuffle(answers)

            for i in range(4):
                self.answers_buttons[i].config(text=html.unescape(answers[i]), state="normal")

    def check_answer(self, button):
        selected_answer = button.cget("text")
        correct_answer = html.unescape(self.current_question["correct_answer"])

        if selected_answer == correct_answer:
            self.score += 1

        for b in self.answers_buttons:
            b.config(state="disabled")
            if b.cget("text") == correct_answer:
                b.config(bg="green")

        self.score_label.config(text="Score: {}".format(self.score))
        self.root.after(2000, self.next_question)  # Wait for 2 seconds before displaying the next question

# Create the main window
root = tk.Tk()
root.title("Trivia Game")
root.geometry("500x300")

# Create an instance of the TriviaGame class
game = TriviaGame(root)

# Start the main event loop
root.mainloop()
