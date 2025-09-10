import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import json

# -------------------------
# Questions by Category
# -------------------------
quizzes = {
    "General Knowledge": [
        {"question": "What is the capital of France?",
         "options": ["Paris", "Rome", "Berlin", "Madrid"], "answer": "Paris"},
        {"question": "Who developed the theory of relativity?",
         "options": ["Newton", "Einstein", "Tesla", "Edison"], "answer": "Einstein"},
        {"question": "Which planet is known as the Red Planet?",
         "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"}
    ],
    "Math": [
        {"question": "2 + 2 equals?",
         "options": ["3", "4", "5", "22"], "answer": "4"},
        {"question": "Square root of 16?",
         "options": ["2", "4", "8", "16"], "answer": "4"},
        {"question": "5 * 6 equals?",
         "options": ["11", "30", "56", "20"], "answer": "30"}
    ],
    "Science": [
        {"question": "What gas do plants release during photosynthesis?",
         "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "answer": "Oxygen"},
        {"question": "H2O is the chemical formula for?",
         "options": ["Hydrogen", "Oxygen", "Water", "Salt"], "answer": "Water"},
        {"question": "What is the center of an atom called?",
         "options": ["Proton", "Nucleus", "Electron", "Neutron"], "answer": "Nucleus"}
    ]
}


# -------------------------
# Quiz App
# -------------------------
class QuizApp:
    def __init__(self, root, quiz):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("500x400")

        self.quiz = quiz
        random.shuffle(self.quiz)

        self.score = 0
        self.q_index = 0
        self.time_left = 10
        self.timer_id = None

        # Question Label
        self.question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=450, justify="left")
        self.question_label.pack(pady=20)

        # Option Buttons
        self.var = tk.StringVar()
        self.buttons = []
        for i in range(4):
            btn = tk.Radiobutton(root, text="", variable=self.var, value="", font=("Arial", 12), anchor="w")
            btn.pack(fill="x", padx=20, pady=5)
            self.buttons.append(btn)

        # Timer Label
        self.timer_label = tk.Label(root, text=f"Time left: {self.time_left}s", font=("Arial", 12), fg="red")
        self.timer_label.pack(pady=10)

        # Next Button
        self.next_button = tk.Button(root, text="Next", command=self.next_question, font=("Arial", 12))
        self.next_button.pack(pady=20)

        self.load_question()

    def load_question(self):
        """Load question and options"""
        if self.q_index < len(self.quiz):
            q = self.quiz[self.q_index]
            self.question_label.config(text=f"Q{self.q_index+1}: {q['question']}")
            self.var.set(None)
            for i, option in enumerate(q["options"]):
                self.buttons[i].config(text=option, value=option)

            # reset timer
            self.time_left = 10
            self.update_timer()
        else:
            self.show_result()

    def update_timer(self):
        """Update countdown every second"""
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            messagebox.showinfo("Time's up!", "You ran out of time for this question.")
            self.next_question(auto=True)

    def next_question(self, auto=False):
        """Check answer and go to next"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        if self.q_index >= len(self.quiz):
            self.show_result()
            return

        selected = self.var.get()
        correct_answer = self.quiz[self.q_index]["answer"]

        if not auto:  # user clicked Next
            if not selected:
                messagebox.showwarning("No answer", "Please select an option before continuing!")
                return
            if selected == correct_answer:
                self.score += 1
        # auto skip = no score

        self.q_index += 1

        if self.q_index < len(self.quiz):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        """Show final score and save it"""
        name = simpledialog.askstring("Quiz Finished", f"Your score: {self.score}/{len(self.quiz)}\nEnter your name:")

        if name:
            try:
                with open("scores.json", "r") as f:
                    scores = json.load(f)
            except FileNotFoundError:
                scores = {}

            scores[name] = self.score
            with open("scores.json", "w") as f:
                json.dump(scores, f, indent=4)

            # Show leaderboard
            leaderboard = "\n".join(
                [f"{player}: {sc}" for player, sc in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
            )
            messagebox.showinfo("Leaderboard", f"📊 Leaderboard:\n{leaderboard}")

        self.root.destroy()


# -------------------------
# Category Selection Window
# -------------------------
def start_quiz():
    category = category_var.get()
    if not category:
        messagebox.showwarning("Select Category", "Please select a quiz category to start.")
        return

    start_window.destroy()
    root = tk.Tk()
    QuizApp(root, quizzes[category])
    root.mainloop()


# -------------------------
# Start Menu
# -------------------------
start_window = tk.Tk()
start_window.title("Quiz Menu")
start_window.geometry("400x200")

tk.Label(start_window, text="Select Quiz Category", font=("Arial", 14)).pack(pady=20)

category_var = tk.StringVar()
category_dropdown = ttk.Combobox(start_window, textvariable=category_var, values=list(quizzes.keys()), state="readonly")
category_dropdown.pack(pady=10)

start_button = tk.Button(start_window, text="Start Quiz", command=start_quiz, font=("Arial", 12))
start_button.pack(pady=20)

start_window.mainloop()
