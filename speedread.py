import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import threading
import time
import re
from PyPDF2 import PdfReader
from tkinter import font as tkfont


class SpeedReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Speed Reader")

        # ====== STATE ======
        self.words = []
        self.current_index = 0
        self.running = False  # actively stepping through words
        self.text_color = "#FFFFFF"
        self.bg_color = "#111111"
        self.focus_color = "#FF4444"
        self.dark_mode = True

        # Feature toggles
        self.focus_on_var = tk.BooleanVar(value=True)       # focus letter highlight
        self.orp_on_var = tk.BooleanVar(value=True)         # align on ORP
        self.sentence_aware_var = tk.BooleanVar(value=True) # extra pause at punctuation

        # Font
        self.word_font = tkfont.Font(family="Helvetica", size=72, weight="bold")

        # ====== MAIN WORD DISPLAY (CENTER) ======
        self.canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(expand=True, fill="both")

        # ====== BOTTOM CONTROL PANEL ======
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # --- Top row: buttons ---
        controls = tk.Frame(bottom_frame)
        controls.pack(pady=3)

        self.load_button = tk.Button(controls, text="Load PDF", command=self.load_pdf, width=12)
        self.load_button.grid(row=0, column=0, padx=5)

        self.start_button = tk.Button(controls, text="Start", command=self.start_reading, width=12)
        self.start_button.grid(row=0, column=1, padx=5)

        self.pause_button = tk.Button(controls, text="Pause", command=self.pause_resume, width=12, state=tk.DISABLED)
        self.pause_button.grid(row=0, column=2, padx=5)

        # Theme buttons
        self.light_btn = tk.Button(controls, text="Light Mode", command=self.set_light_mode, width=12)
        self.light_btn.grid(row=0, column=3, padx=5)

        self.dark_btn = tk.Button(controls, text="Dark Mode", command=self.set_dark_mode, width=12)
        self.dark_btn.grid(row=0, column=4, padx=5)

        # Color buttons
        color_frame = tk.Frame(bottom_frame)
        color_frame.pack(pady=3)

        self.text_color_btn = tk.Button(color_frame, text="Text Color", command=self.choose_text_color, width=12)
        self.text_color_btn.pack(side=tk.LEFT, padx=5)

        self.focus_color_btn = tk.Button(color_frame, text="Focus Color", command=self.choose_focus_color, width=12)
        self.focus_color_btn.pack(side=tk.LEFT, padx=5)

        # --- WPM slider ---
        wpm_frame = tk.Frame(bottom_frame)
        wpm_frame.pack(pady=3)

        tk.Label(wpm_frame, text="Words per minute:").pack(side=tk.LEFT, padx=5)

        self.wpm_var = tk.IntVar(value=300)
        self.wpm_scale = tk.Scale(
            wpm_frame,
            from_=50, to=1200,
            orient=tk.HORIZONTAL,
            variable=self.wpm_var,
            length=300
        )
        self.wpm_scale.pack(side=tk.LEFT)

        # --- Start position slider ---
        startpos_frame = tk.Frame(bottom_frame)
        startpos_frame.pack(pady=3)

        tk.Label(startpos_frame, text="Start position (%):").pack(side=tk.LEFT, padx=5)

        self.start_pos_var = tk.IntVar(value=0)
        self.start_pos_scale = tk.Scale(
            startpos_frame,
            from_=0, to=100,
            orient=tk.HORIZONTAL,
            variable=self.start_pos_var,
            length=300
        )
        self.start_pos_scale.pack(side=tk.LEFT)

        # --- Feature toggles ---
        features_frame = tk.Frame(bottom_frame)
        features_frame.pack(pady=3)

        self.focus_check = tk.Checkbutton(
            features_frame,
            text="Focus Letter",
            variable=self.focus_on_var
        )
        self.focus_check.pack(side=tk.LEFT, padx=5)

        self.orp_check = tk.Checkbutton(
            features_frame,
            text="Align ORP",
            variable=self.orp_on_var
        )
        self.orp_check.pack(side=tk.LEFT, padx=5)

        self.sentence_check = tk.Checkbutton(
            features_frame,
            text="Sentence-aware timing",
            variable=self.sentence_aware_var
        )
        self.sentence_check.pack(side=tk.LEFT, padx=5)

        # --- Status bar ---
        self.status_var = tk.StringVar(value="No PDF loaded.")
        self.status_label = tk.Label(bottom_frame, textvariable=self.status_var, anchor="w")
        self.status_label.pack(fill=tk.X)

        # Apply initial theme
        self.apply_theme()

    # =================== THEME & COLORS ===================

    def apply_theme(self):
        bg = self.bg_color
        self.root.configure(bg=bg)
        self.canvas.configure(bg=bg)
        # Not changing all widgets' backgrounds to keep it simple/clean for now.

    def set_dark_mode(self):
        self.dark_mode = True
        self.bg_color = "#111111"
        if self.text_color == "#000000":
            self.text_color = "#FFFFFF"
        self.apply_theme()
        self.redraw_current_word()

    def set_light_mode(self):
        self.dark_mode = False
        self.bg_color = "#FFFFFF"
        if self.text_color == "#FFFFFF":
            self.text_color = "#000000"
        self.apply_theme()
        self.redraw_current_word()

    def choose_text_color(self):
        color = colorchooser.askcolor(title="Choose text color", initialcolor=self.text_color)[1]
        if color:
            self.text_color = color
            self.redraw_current_word()

    def choose_focus_color(self):
        color = colorchooser.askcolor(title="Choose focus color", initialcolor=self.focus_color)[1]
        if color:
            self.focus_color = color
            self.redraw_current_word()

    # =================== PDF LOADING ===================

    def load_pdf(self):
        filepath = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not filepath:
            return

        try:
            self.status_var.set("Loading PDF...")
            self.root.update_idletasks()

            reader = PdfReader(filepath)
            text_parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

            full_text = " ".join(text_parts)
            full_text = re.sub(r"\s+", " ", full_text)
            self.words = [w for w in full_text.split(" ") if w.strip()]

            if not self.words:
                messagebox.showerror("Error", "No extractable text found in PDF.")
                self.status_var.set("PDF load failed.")
                return

            self.current_index = 0
            self.status_var.set(f"Loaded {len(self.words)} words. Set options and press Start.")
            self.draw_word("Ready")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF:\n{e}")
            self.status_var.set("Error loading PDF.")

    # =================== CONTROL BUTTONS ===================

    def start_reading(self):
        if not self.words:
            messagebox.showwarning("No PDF", "Please load a PDF first.")
            return
        if self.running:
            return

        # Set starting position
        total = len(self.words)
        start_percent = self.start_pos_var.get()
        self.current_index = int(total * (start_percent / 100.0))
        if self.current_index >= total:
            self.current_index = total - 1

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL, text="Pause")
        self.status_var.set(f"Reading from {start_percent}% into document (word {self.current_index}/{total}).")

        t = threading.Thread(target=self.read_loop, daemon=True)
        t.start()

    def pause_resume(self):
        if not self.words:
            return
        if self.running:
            # Pause
            self.running = False
            self.pause_button.config(text="Resume")
            self.status_var.set("Paused.")
        else:
            # Resume
            if self.current_index >= len(self.words):
                self.status_var.set("At end of document. Press Start to restart.")
                return
            self.running = True
            self.pause_button.config(text="Pause")
            self.start_button.config(state=tk.DISABLED)

            t = threading.Thread(target=self.read_loop, daemon=True)
            t.start()

    # =================== READING LOOP ===================

    def read_loop(self):
        while self.running and self.current_index < len(self.words):
            word = self.words[self.current_index]

            # Update word on canvas
            self.root.after(0, self.draw_word, word)

            # Move to next word
            self.current_index += 1

            # Base delay from WPM
            wpm = max(self.wpm_var.get(), 1)
            delay = 60.0 / wpm

            # Sentence-aware timing (extra pause for punctuation)
            if self.sentence_aware_var.get():
                if word.endswith((".", "!", "?", "?!", "!!")):
                    delay *= 2.0
                elif word.endswith((",", ";", ":")):
                    delay *= 1.5

            time.sleep(delay)

        # When loop exits (either end or paused/stopped)
        if self.current_index >= len(self.words):
            self.status_var.set("Reached end of document.")
        # Only reset start button if fully stopped, not just paused
        if not self.running:
            self.root.after(0, self.start_button.config, {"state": tk.NORMAL})
            self.root.after(0, self.pause_button.config, {"state": tk.NORMAL})

        self.running = False

    # =================== WORD RENDERING ===================

    def compute_orp_index(self, word: str) -> int:
        # Simple heuristic: around 35% into the word, clamped
        if not word:
            return 0
        idx = int(len(word) * 0.35)
        if idx < 0:
            idx = 0
        if idx >= len(word):
            idx = len(word) - 1
        return idx

    def draw_word(self, word: str):
        """Draws the word with ORP alignment and focus highlighting."""
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 0 or h <= 0:
            w, h = 800, 400

        x_center = w / 2
        y_center = h / 2

        focus_on = self.focus_on_var.get()
        orp_on = self.orp_on_var.get()

        # If ORP/focus disabled, just draw centered text
        if not focus_on and not orp_on:
            self.canvas.create_text(
                x_center,
                y_center,
                text=word,
                font=self.word_font,
                fill=self.text_color
            )
            return

        # Determine ORP index
        orp_idx = self.compute_orp_index(word)
        pre = word[:orp_idx]
        focus_char = word[orp_idx] if word else ""
        post = word[orp_idx + 1:] if orp_idx + 1 <= len(word) else ""

        # Measure segments
        pre_w = self.word_font.measure(pre)
        focus_w = self.word_font.measure(focus_char)
        post_w = self.word_font.measure(post)

        if orp_on:
            # Keep the focus character centered at x_center
            pre_x = x_center - (focus_w / 2) - (pre_w / 2)
            focus_x = x_center
            post_x = x_center + (focus_w / 2) + (post_w / 2)
        else:
            # Center the whole word as a unit, ignore ORP alignment
            total_w = pre_w + focus_w + post_w
            left = x_center - total_w / 2

            pre_x = left + pre_w / 2
            focus_x = left + pre_w + focus_w / 2
            post_x = left + pre_w + focus_w + post_w / 2

        # Draw segments
        if pre:
            self.canvas.create_text(
                pre_x,
                y_center,
                text=pre,
                font=self.word_font,
                fill=self.text_color
            )

        if focus_char:
            self.canvas.create_text(
                focus_x,
                y_center,
                text=focus_char,
                font=self.word_font,
                fill=self.focus_color if focus_on else self.text_color
            )

        if post:
            self.canvas.create_text(
                post_x,
                y_center,
                text=post,
                font=self.word_font,
                fill=self.text_color
            )


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1400x600")
    app = SpeedReaderApp(root)
    root.mainloop()
