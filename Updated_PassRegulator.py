import tkinter as tk
from tkinter import messagebox
import string
import random

# --- Secure Random Generator ---
# SystemRandom uses os.urandom() under the hood for cryptographically secure randomness
secure_rand = random.SystemRandom()

# --- UI Colors & Fonts ---
# These values define the look and feel of the app
BG_COLOR = "#1e1e2f"       # Main background
CARD_COLOR = "#2a2a40"     # Card background
TEXT_COLOR = "#ffffff"     # Text color
ACCENT_COLOR = "#4CAF50"   # Main accent (buttons)
BTN_HOVER = "#45a049"      # Button hover color

TITLE_FONT = ("Helvetica", 18, "bold")
SUBTITLE_FONT = ("Helvetica", 10)
LABEL_FONT = ("Helvetica", 11)
ENTRY_FONT = ("Courier", 11)
BTN_FONT = ("Helvetica", 10, "bold")

# =========================
#  PASSWORD GENERATION LOGIC
# =========================

def obfuscate_memory(memory_items):
    """
    Takes a list of memorable words and turns them into a secure password.
    - Applies letter-to-symbol/number substitutions
    - Randomly changes some letters to uppercase
    - Appends random digits & symbols
    - Shuffles the final result for unpredictability
    """
    substitutions = {
        "a": "@", "b": "8", "e": "3", "g": "9", "i": "!",
        "l": "1", "o": "0", "s": "$", "t": "7", "z": "2"
    }
    obfuscated_parts = []

    for item in memory_items:
        item = item.strip().lower()
        if not item:
            continue

        # Replace letters with leetspeak symbols
        for k, v in substitutions.items():
            item = item.replace(k, v)

        # Randomly uppercase some characters
        item = ''.join(
            c.upper() if secure_rand.random() > 0.5 else c
            for c in item
        )

        # Add random noise (numbers & symbol)
        noise = str(secure_rand.randint(10, 99)) + secure_rand.choice("!#$%&?*")
        obfuscated_parts.append(item + noise)

    # Merge parts and shuffle characters for added randomness
    password = ''.join(obfuscated_parts)
    password = ''.join(secure_rand.sample(password, len(password)))

    return password


def check_password_strength(password):
    """
    Checks password strength based on:
    - Length
    - Mix of upper/lowercase letters
    - Digits
    - Symbols
    Returns a tuple: (strength_label, display_color)
    """
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    # Score system for strength
    score = 0
    if length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    score += has_upper + has_lower + has_digit + has_symbol

    if score >= 7:
        return ("Very Strong", "#00BFFF")
    elif score >= 5:
        return ("Strong", "#4CAF50")
    elif score >= 3:
        return ("Medium", "#FFA500")
    else:
        return ("Weak", "#FF4C4C")


def generate_password():
    """
    Gets user input, processes it into a secure password,
    and updates the UI with the result and strength.
    """
    user_input = entry.get()
    if not user_input.strip():
        messagebox.showwarning("Missing Input", "Please enter some memorable items.")
        return

    memory_items = [item.strip() for item in user_input.split(",") if item.strip()]

    if not memory_items:
        messagebox.showwarning("Invalid Input", "Please enter valid words, not just commas or spaces.")
        return

    password = obfuscate_memory(memory_items)
    result_var.set(password)

    # Check and display password strength
    strength_label, color = check_password_strength(password)
    strength_var.set(f"Password Strength: {strength_label}")
    strength_display.config(fg=color)


def copy_to_clipboard():
    """
    Copies the generated password to the clipboard.
    """
    if not result_var.get():
        messagebox.showinfo("Nothing to Copy", "Please generate a password first.")
        return
    root.clipboard_clear()
    root.clipboard_append(result_var.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")


def clear_all():
    """
    Clears input, generated password, and strength display.
    """
    entry.delete(0, tk.END)
    result_var.set("")
    strength_var.set("")


def toggle_password_visibility():
    """
    Toggles password field between masked (*) and visible text.
    """
    if result_entry.cget('show') == "*":
        result_entry.config(show="")
    else:
        result_entry.config(show="*")


# =========================
#  GUI SETUP
# =========================

root = tk.Tk()
root.title("🔐 PassRegulator – Memory-Based Password Generator")
root.geometry("650x480")
root.configure(bg=BG_COLOR)

# Main container frame
main_frame = tk.Frame(root, bg=CARD_COLOR, bd=0, relief="flat")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Title & Subtitle
tk.Label(main_frame, text="PassRegulator", font=TITLE_FONT, bg=CARD_COLOR, fg=TEXT_COLOR).pack(pady=(15, 2))
tk.Label(main_frame, text="Generate secure passwords from your memories",
         font=SUBTITLE_FONT, bg=CARD_COLOR, fg="#aaaaaa").pack()

# Input field label & entry
tk.Label(main_frame, text="Enter memorable items (comma separated):",
         font=LABEL_FONT, bg=CARD_COLOR, fg=TEXT_COLOR).pack(pady=(20, 5))
entry = tk.Entry(main_frame, width=60, font=ENTRY_FONT, bd=2, relief="groove", bg="#fff", fg="#000")
entry.pack(ipady=4)

# Button container
btn_frame = tk.Frame(main_frame, bg=CARD_COLOR)
btn_frame.pack(pady=15)

# Helper to create styled buttons
def styled_button(parent, text, cmd, bg=ACCENT_COLOR, fg="white"):
    return tk.Button(parent, text=text, font=BTN_FONT, command=cmd,
                     bg=bg, fg=fg, activebackground=BTN_HOVER,
                     relief="flat", padx=10, pady=5, bd=0, cursor="hand2")

# Buttons: Generate / Copy / Clear
styled_button(btn_frame, "Generate Password", generate_password).grid(row=0, column=0, padx=5)
styled_button(btn_frame, "Copy", copy_to_clipboard, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)
styled_button(btn_frame, "Clear", clear_all, bg="#FF5722").grid(row=0, column=2, padx=5)

# Generated password display
tk.Label(main_frame, text="🔧 Generated Password:", font=LABEL_FONT, bg=CARD_COLOR, fg=TEXT_COLOR).pack()
result_var = tk.StringVar()
result_entry = tk.Entry(main_frame, textvariable=result_var, width=60, font=ENTRY_FONT, bd=2,
                        relief="sunken", state='readonly', show="*", bg="#f5f5f5")
result_entry.pack(ipady=4, pady=(0, 5))

# Show/Hide button
styled_button(main_frame, "Show/Hide", toggle_password_visibility, bg="#9C27B0").pack()

# Password strength display
strength_var = tk.StringVar()
strength_display = tk.Label(main_frame, textvariable=strength_var, font=("Helvetica", 12, "bold"), bg=CARD_COLOR)
strength_display.pack(pady=(10, 0))

# Start the GUI event loop
root.mainloop()

