"""Compact touchscreen Caesar cipher game. Standard-library Tkinter only."""
import math
import string
import tkinter as tk

ALPHABET = string.ascii_uppercase
SECRET = 'PANTHER'
CIPHER = 'SDQWKHU'
BG, PANEL, GOLD, MINT = '#101b2c', '#1c2c43', '#ffdc85', '#79e4c0'

class CipherPuzzle:
    def __init__(self, root):
        self.root = root
        self.shift = 0
        self.last_angle = None
        self.drag_accum = 0.0
        root.title('Crack the Code | UW–Parkside Computer Science')
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        width = min(1050, max(720, sw - 90))
        height = min(690, max(520, sh - 105))
        root.geometry(f'{width}x{height}+25+25')
        root.minsize(720, 520)
        root.configure(bg=BG)
        self.build()
        root.bind('<Left>', lambda e: self.rotate(-1))
        root.bind('<Right>', lambda e: self.rotate(1))
        root.bind('<Configure>', self.on_resize)

    def label(self, parent, text, size=13, color='white', bold=False, **kw):
        return tk.Label(parent, text=text, font=('Segoe UI', size, 'bold' if bold else 'normal'),
                        bg=parent.cget('bg'), fg=color, **kw)

    def button(self, parent, text, command, width=8):
        return tk.Button(parent, text=text, command=command, width=width,
                         font=('Segoe UI', 12, 'bold'), bg='#eaf1fc', fg='#13243b',
                         activebackground='#c9e8f7', relief='flat', pady=10, cursor='hand2')

    def build(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill='x', pady=(8, 4))
        self.label(header, 'CRACK THE CODE', 25, '#7ed9ff', True).pack()
        self.label(header, 'UW–Parkside Computer Science  •  SEE Your Future Expo', 10).pack()

        main = tk.Frame(self.root, bg=BG)
        main.pack(fill='both', expand=True, padx=16, pady=(3, 10))
        main.grid_columnconfigure(0, weight=3)
        main.grid_columnconfigure(1, weight=2)
        main.grid_rowconfigure(0, weight=1)

        left = tk.Frame(main, bg=PANEL)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 8))
        self.label(left, 'DRAG THE INNER RING', 13, '#b5cfff', True).pack(pady=(10, 2))
        self.canvas = tk.Canvas(left, bg=PANEL, highlightthickness=0, cursor='hand2')
        self.canvas.pack(fill='both', expand=True, padx=6, pady=3)
        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.canvas.bind('<Configure>', lambda e: self.refresh())
        controls = tk.Frame(left, bg=PANEL)
        controls.pack(pady=(2, 10))
        self.button(controls, '◀', lambda: self.rotate(-1), 5).pack(side='left', padx=8)
        self.button(controls, '▶', lambda: self.rotate(1), 5).pack(side='left', padx=8)

        right = tk.Frame(main, bg=BG)
        right.grid(row=0, column=1, sticky='nsew', padx=(8, 0))
        self.label(right, 'MISSION', 12, GOLD, True).pack(pady=(15, 2))
        self.label(right, 'Decode the secret word\nto unlock the vault.', 14, 'white', True,
                   justify='center').pack()
        self.label(right, 'ENCRYPTED MESSAGE', 11, '#a7b9d0', True).pack(pady=(20, 2))
        self.label(right, CIPHER, 29, 'white', True).pack()
        self.label(right, 'YOUR DECODED MESSAGE', 11, '#a7b9d0', True).pack(pady=(25, 2))
        self.decoded = self.label(right, '', 29, MINT, True)
        self.decoded.pack()
        self.feedback = self.label(right, 'Hint: Every letter has the same shift.', 11, GOLD,
                                   wraplength=330, justify='center')
        self.feedback.pack(pady=(18, 12))
        self.button(right, 'UNLOCK VAULT', self.unlock, 18).pack(pady=5)
        self.button(right, 'RESET', self.reset, 12).pack(pady=5)
        self.refresh()

    def on_resize(self, event):
        if event.widget == self.root:
            self.root.after_idle(self.refresh)

    def geometry(self):
        w, h = max(1, self.canvas.winfo_width()), max(1, self.canvas.winfo_height())
        cx, cy = w / 2, h / 2
        r = max(70, min(w, h) / 2 - 14)
        return cx, cy, r

    def angle(self, x, y):
        cx, cy, _ = self.geometry()
        return (math.degrees(math.atan2(x - cx, cy - y)) + 360) % 360

    def on_press(self, event):
        cx, cy, r = self.geometry()
        distance = math.hypot(event.x - cx, event.y - cy)
        if .47 * r <= distance <= .83 * r:
            self.last_angle = self.angle(event.x, event.y)
            self.drag_accum = 0.0

    def on_drag(self, event):
        if self.last_angle is None:
            return
        angle = self.angle(event.x, event.y)
        delta = (angle - self.last_angle + 180) % 360 - 180
        self.last_angle = angle
        self.drag_accum += delta
        steps = math.trunc(self.drag_accum / (360 / 26))
        if steps:
            self.drag_accum -= steps * (360 / 26)
            self.rotate(steps)

    def on_release(self, event):
        self.last_angle = None
        self.drag_accum = 0.0

    def rotate(self, steps):
        self.shift = (self.shift + steps) % 26
        self.feedback.config(text='Hint: Every letter has the same shift.', fg=GOLD)
        self.refresh()

    def refresh(self):
        if not hasattr(self, 'canvas'):
            return
        c = self.canvas
        c.delete('all')
        cx, cy, r = self.geometry()
        c.create_oval(cx-r, cy-r, cx+r, cy+r, fill='#25334a', outline=GOLD, width=3)
        c.create_oval(cx-.78*r, cy-.78*r, cx+.78*r, cy+.78*r,
                     fill='#183b45', outline=MINT, width=3)
        c.create_oval(cx-.43*r, cy-.43*r, cx+.43*r, cy+.43*r,
                     fill=PANEL, outline='#4e7e85', width=2)
        font_size = max(9, min(14, int(r / 14)))
        for i, letter in enumerate(ALPHABET):
            theta = 2 * math.pi * i / 26
            x, y = cx + .89*r*math.sin(theta), cy - .89*r*math.cos(theta)
            c.create_text(x, y, text=letter, fill=GOLD, font=('Segoe UI', font_size, 'bold'))
            x2, y2 = cx + .66*r*math.sin(theta), cy - .66*r*math.cos(theta)
            c.create_text(x2, y2, text=ALPHABET[(i-self.shift)%26], fill=MINT,
                          font=('Segoe UI', font_size, 'bold'))
        c.create_text(cx, cy-14, text='DRAG', fill='#b5cfff', font=('Segoe UI', 15, 'bold'))
        c.create_text(cx, cy+12, text=f'SHIFT {self.shift}', fill='white', font=('Segoe UI', 12, 'bold'))
        self.decoded.config(text=''.join(ALPHABET[(ALPHABET.index(ch)-self.shift)%26] for ch in CIPHER))

    def unlock(self):
        if self.shift == 3:
            self.feedback.config(text='VAULT UNLOCKED! You cracked the cipher!', fg=MINT)
        else:
            self.feedback.config(text='Still locked. Rotate the wheel and try again!', fg='#ff9c9c')

    def reset(self):
        self.shift = 0
        self.last_angle = None
        self.drag_accum = 0.0
        self.feedback.config(text='Hint: Every letter has the same shift.', fg=GOLD)
        self.refresh()

if __name__ == '__main__':
    root = tk.Tk()
    CipherPuzzle(root)
    root.mainloop()
