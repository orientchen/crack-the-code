# Crack the Code — Cybersecurity Outreach Demos

Two interactive Python demonstrations developed for the **UW–Parkside Computer Science** outreach table at the **SEE Your Future Expo** at Racine Park High School:

- **Cipher Puzzle:** Touchscreen-friendly Caesar cipher wheel and simulated vault.
- **Password Guessing Demo:** Simulated local password attacks with a live guess counter and progress display.

Both activities run locally, without network access or third-party packages, and require no prior programming experience.

## Demo 1 — Cipher Puzzle

## What students do

1. Read the encrypted message: **SDQWKHU**.
2. Touch and drag the **inner alphabet ring** to rotate it. A mouse works too.
3. Watch the decoded message update as the wheel moves.
4. Select **UNLOCK VAULT** when the decoded word makes sense.
5. Select **RESET** for the next participant.

**Presenter note:** The secret word is `PANTHER`, a reference to Racine Park High School. The correct Caesar shift is 3. Avoid revealing this until the student has tried the puzzle.

## Demo 2 — Password Guessing

Students enter a **made-up demo password** (never a real password), select a guessing strategy, and watch the computer test candidates. Presets include `cat`, `panther`, and `panther2026`.

- **Brute force (a–z, 1–4 letters):** Systematically checks short lowercase combinations. It cannot find `panther` because that password exceeds the four-letter limit.
- **Dictionary + common year patterns:** Tries a small built-in list of words and predictable variations. It may find `panther` or `panther2026` but can miss other passwords, including `cat`.
- **Start Attack / Stop:** Launch or interrupt the local demonstration.

The GUI reports guesses and elapsed time. Results are limited by the demonstration's search space and maximum number of guesses; **NOT FOUND does not mean a password is secure**. The displayed speed is a property of this teaching program, not a realistic estimate of an online or offline attack against a production authentication system.

Run:

```bash
python password_cracker_demo.py
```

## Requirements

- Python 3 with Tkinter support (Tkinter is typically bundled with standard Python installers for Windows)
- Windows touchscreen or a computer with a mouse
- No internet connection or third-party Python packages required

## Run the cipher puzzle

From a terminal in the repository folder:

```bash
python cipher_puzzle.py
```

On systems where Python 3 is invoked as `python3`:

```bash
python3 cipher_puzzle.py
```

## Cipher puzzle controls

| Control | Action |
| --- | --- |
| Drag inner ring | Rotate the cipher wheel |
| Left / right arrow buttons | Rotate by one letter |
| Keyboard left / right arrows | Rotate by one letter |
| UNLOCK VAULT | Check whether the secret word is decoded |
| RESET | Return to the starting puzzle |

The application uses a two-column layout to fit the wheel and puzzle controls on a typical laptop display. It also adjusts the wheel size when the window is resized.

## Teaching points

- A **Caesar cipher** replaces each letter with another letter a fixed distance away in the alphabet.
- Rotating the wheel explores the 26 possible shifts.
- This historical cipher is **not secure for modern communication**; its small key space makes it easy to break.
- **Encryption and password authentication are different concepts.** The cipher wheel illustrates a historical cipher; the second program illustrates candidate password guessing.
- The password demo does **not** attempt to access accounts, websites, or external services.
- Password length, unpredictability, and resistance to common guessing patterns all matter.

## Project files

```text
crack-the-code/
├── README.md
├── cipher_puzzle.py
├── password_cracker_demo.py
└── .gitignore
```

## Publish to GitHub

Create a new, empty repository on GitHub named `crack-the-code`, then from this folder run:

```bash
git init
git add .
git commit -m "Add cipher puzzle and password guessing outreach demos"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/crack-the-code.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Alternatively, upload these files using GitHub's web interface.

## License

No license has been selected yet. Add a `LICENSE` file if you plan to distribute or invite reuse of this project.
