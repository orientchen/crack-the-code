"""SEE Your Future Expo: educational, local-only password guessing demo."""
import itertools
import string
import time
import tkinter as tk
from tkinter import ttk

WORDS = ["password", "admin", "welcome", "letmein", "panther", "tiger", "school", "computer", "racine", "park", "hello", "secret"]
BATCH = 250
DELAY_MS = 25
BRUTE_CHARS = string.ascii_lowercase + string.digits


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
        self.brute = False
        self.length = 1
        self.mode = tk.StringVar(value="Brute force (a–z, 0–9; increasing length)")
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
        ttk.Button(frame, text="Try PANTHER2026", command=lambda: self.set_example("panther2026", 0)).pack(side="left", padx=3)
        frame2 = ttk.LabelFrame(outer, text="2  Choose a guessing strategy", padding=14)
        frame2.pack(fill="x", pady=15)
        self.combo = ttk.Combobox(frame2, textvariable=self.mode, state="readonly", values=[
            "Brute force (a–z, 0–9; increasing length)", "Dictionary + common year patterns"
        ], width=43)
        self.combo.pack(side="left", padx=(0, 12))
        ttk.Button(frame2, text="Start Attack", command=self.start).pack(side="left", padx=4)
        ttk.Button(frame2, text="Stop", command=self.stop).pack(side="left", padx=4)
        result = ttk.LabelFrame(outer, text="3  Watch the computer guess", padding=18)
        result.pack(fill="both", expand=True)
        tk.Label(result, text="CURRENT GUESS", font=("Arial", 11, "bold"), fg="#555").pack()
        tk.Label(result, textvariable=self.current, font=("Consolas", 34, "bold"), fg="#184f84").pack(pady=12)
        tk.Label(result, textvariable=self.stats, font=("Consolas", 13)).pack(pady=6)
        # Indeterminate: there is no meaningful finite percentage for an unbounded search.
        self.progress = ttk.Progressbar(result, mode="indeterminate")
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

    def dictionary_candidates(self):
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
        self.brute = self.mode.get().startswith("Brute")
        self.iterator = None if self.brute else iter(self.dictionary_candidates())
        self.length = 1
        self.attempts = 0
        self.started = time.perf_counter()
        self.running = True
        self.current.set("…")
        self.progress.start(12)
        self.status.set("Brute force: testing 1-character guesses…" if self.brute else "Trying dictionary and common patterns…")
        self.tick()

    def next_brute_guess(self):
        # Enumerate lengths lazily, without constructing an enormous list.
        if self.iterator is None:
            self.iterator = itertools.product(BRUTE_CHARS, repeat=self.length)
        try:
            return "".join(next(self.iterator))
        except StopIteration:
            self.length += 1
            self.iterator = itertools.product(BRUTE_CHARS, repeat=self.length)
            return "".join(next(self.iterator))

    def tick(self):
        self.job = None
        if not self.running:
            return
        found = False
        exhausted = False
        last_guess = None
        for _ in range(BATCH):
            try:
                guess = self.next_brute_guess() if self.brute else next(self.iterator)
            except StopIteration:
                exhausted = True
                break
            last_guess = guess
            self.attempts += 1
            if guess == self.target:
                found = True
                break
        elapsed = time.perf_counter() - self.started
        if last_guess is not None:
            self.current.set(last_guess)
        self.stats.set(f"Guesses: {self.attempts:,}     Elapsed: {elapsed:.2f} s")
        if found:
            self.running = False
            self.progress.stop()
            self.status.set("UNLOCKED! The computer discovered the password.")
        elif exhausted:
            self.running = False
            self.progress.stop()
            self.status.set("NOT FOUND. The dictionary and pattern list has been exhausted.")
        else:
            if self.brute:
                self.status.set(f"Brute force: testing {self.length}-character guesses. Longer passwords require many more combinations. Press Stop anytime.")
            self.job = self.root.after(DELAY_MS, self.tick)

    def stop(self, silent=False):
        self.running = False
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None
        if hasattr(self, "progress"):
            self.progress.stop()
        if not silent:
            self.status.set("Stopped. Try a different password or attack strategy.")

    def close(self):
        self.stop(silent=True)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    Demo(root)
    root.mainloop()
