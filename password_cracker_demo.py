"""SEE Your Future Expo: educational, local-only password guessing demo."""
import itertools
import string
import time
import tkinter as tk
from tkinter import ttk

WORDS = ["password", "admin", "welcome", "letmein", "panther", "tiger", "school", "computer", "racine", "park", "hello", "secret"]
MAX_GUESSES = 250_000
BATCH = 250

class Demo:
    def __init__(self, root):
        self.root = root
        root.title("Crack the Code | UW–Parkside Computer Science")
        root.geometry("850x640")
        root.minsize(680, 560)
        self.target = ""
        self.iterator = None
        self.running = False
        self.attempts = 0
        self.started = 0.0
        self.job = None
        self.mode = tk.StringVar(value="Brute force (a–z, 1–4 letters)")
        self.password = tk.StringVar(value="cat")
        self.current = tk.StringVar(value="—")
        self.status = tk.StringVar(value="Choose a demo password and start the attack.")
        self.stats = tk.StringVar(value="Guesses: 0     Elapsed: 0.00 s")
        self.build()
        root.protocol("WM_DELETE_WINDOW", self.close)

    def build(self):
        outer = ttk.Frame(self.root, padding=24)
        outer.pack(fill="both", expand=True)
        tk.Label(outer, text="CAN YOU CRACK THE PASSWORD?", font=("Arial", 23, "bold"), fg="#173a60").pack(anchor="w")
        tk.Label(outer, text="UW–Parkside Computer Science  •  SEE Your Future Expo", font=("Arial", 12)).pack(anchor="w", pady=(2, 20))
        frame = ttk.LabelFrame(outer, text="1  Create a DEMO password (never enter a real password)", padding=14)
        frame.pack(fill="x")
        ttk.Entry(frame, textvariable=self.password, font=("Consolas", 17), width=23).pack(side="left", padx=(0, 12))
        ttk.Button(frame, text="Try CAT", command=lambda: self.set_example("cat", 0)).pack(side="left", padx=3)
        ttk.Button(frame, text="Try PANTHER", command=lambda: self.set_example("panther", 1)).pack(side="left", padx=3)
        ttk.Button(frame, text="Try PANTHER2026", command=lambda: self.set_example("panther2026", 1)).pack(side="left", padx=3)
        frame2 = ttk.LabelFrame(outer, text="2  Choose a guessing strategy", padding=14)
        frame2.pack(fill="x", pady=15)
        self.combo = ttk.Combobox(frame2, textvariable=self.mode, state="readonly", values=["Brute force (a–z, 1–4 letters)", "Dictionary + common year patterns"], width=43)
        self.combo.pack(side="left", padx=(0, 12))
        ttk.Button(frame2, text="Start Attack", command=self.start).pack(side="left", padx=4)
        ttk.Button(frame2, text="Stop", command=self.stop).pack(side="left", padx=4)
        result = ttk.LabelFrame(outer, text="3  Watch the computer guess", padding=18)
        result.pack(fill="both", expand=True)
        tk.Label(result, text="CURRENT GUESS", font=("Arial", 11, "bold"), fg="#555").pack()
        tk.Label(result, textvariable=self.current, font=("Consolas", 34, "bold"), fg="#184f84").pack(pady=12)
        tk.Label(result, textvariable=self.stats, font=("Consolas", 13)).pack(pady=6)
        self.progress = ttk.Progressbar(result, mode="determinate", maximum=MAX_GUESSES)
        self.progress.pack(fill="x", pady=10)
        tk.Label(result, textvariable=self.status, font=("Arial", 13, "bold"), wraplength=650, justify="center").pack(pady=8)
        tk.Label(outer, text="Educational simulation: guesses a local secret only. Real services use rate limits, secure password hashing, and other protections.", wraplength=760, justify="left", fg="#555").pack(anchor="w", pady=(14, 0))

    def set_example(self, value, mode):
        self.stop(silent=True)
        self.password.set(value)
        self.mode.set(self.combo["values"][mode])
        self.status.set("Example selected. Click Start Attack.")
        self.current.set("—")
        self.stats.set("Guesses: 0     Elapsed: 0.00 s")
        self.progress["value"] = 0

    def candidates(self):
        if self.mode.get().startswith("Brute"):
            for length in range(1, 5):
                for chars in itertools.product(string.ascii_lowercase, repeat=length):
                    yield "".join(chars)
        else:
            seen = set()
            for word in WORDS:
                for candidate in (word, word.capitalize(), word.upper(), word + "123", word + "2026", word.upper() + "2026", word + "!"):
                    if candidate not in seen:
                        seen.add(candidate)
                        yield candidate

    def start(self):
        self.stop(silent=True)
        self.target = self.password.get()
        if not self.target or len(self.target) > 32:
            self.status.set("Enter a demo password between 1 and 32 characters.")
            return
        self.iterator = iter(self.candidates())
        self.attempts = 0
        self.started = time.perf_counter()
        self.running = True
        self.current.set("…")
        self.progress["value"] = 0
        self.status.set("Trying guesses against the local demo password…")
        self.tick()

    def tick(self):
        if not self.running:
            return
        found = False
        exhausted = False
        for _ in range(BATCH):
            if self.attempts >= MAX_GUESSES:
                exhausted = True
                break
            try:
                guess = next(self.iterator)
            except StopIteration:
                exhausted = True
                break
            self.attempts += 1
            if guess == self.target:
                found = True
                break
        elapsed = time.perf_counter() - self.started
        if self.attempts:
            self.current.set(guess)
        self.stats.set(f"Guesses: {self.attempts:,}     Elapsed: {elapsed:.2f} s")
        self.progress["value"] = self.attempts
        if found:
            self.running = False
            self.status.set("UNLOCKED! The computer discovered the password.")
        elif exhausted:
            self.running = False
            self.status.set("NOT FOUND. This strategy did not discover the password within its search limit.")
        else:
            self.job = self.root.after(25, self.tick)

    def stop(self, silent=False):
        self.running = False
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None
        if not silent:
            self.status.set("Stopped. Try a different password or attack strategy.")

    def close(self):
        self.stop(silent=True)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    Demo(root)
    root.mainloop()
