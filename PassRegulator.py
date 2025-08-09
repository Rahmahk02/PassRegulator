import random
import tkinter as tk
from tkinter import messagebox
import string

def obfuscate_memory(memory_items):
    """Turn a list of memory items into a secure, obfuscated password."""
    obfuscated = ""
    for item in memory_items:
        item = item.strip()
        if not item:
            continue

        item = item.lower()
        item = (item.replace("a", "@")
                    .replace("e", "3")
                    .replace("i", "!")
                    .replace("o", "0")
                    .replace("s", "$"))
        item = item.capitalize()
        noise = str(random.randint(10, 99)) + random.choice(["!", "#", "$", "%", "&", "?"])
        obfuscated += item + noise

    return obfuscated

def check_password_strength(password):
    """Check the strength of the password and return a (label, color) tuple."""
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    score = 0
    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    score += has_upper + has_lower + has_digit + has_symbol

    if score >= 5:
        return ("Strong", "green")
    elif score >= 3:
        return ("Medium", "orange")
    else:
        return ("Weak", "red")

def generate_password():
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

    # Check strength and update label
    strength_label, color = check_password_strength(password)
    strength_var.set(f"Password Strength: {strength_label}")
    strength_display.config(fg=color)

# --- GUI Setup ---
root = tk.Tk()
root.title("🔐 PassRegulator – Memory-Based Password Generator")
root.geometry("580x360")  # slightly taller to fit strength label
root.configure(bg="#f2f2f2")

title_font = ("Helvetica", 16, "bold")
label_font = ("Helvetica", 11)
entry_font = ("Courier", 11)

tk.Label(root, text="PassRegulator", font=title_font, bg="#f2f2f2", fg="#333").pack(pady=(15, 5))
tk.Label(root, text="Generate secure passwords from your memories", font=("Helvetica", 10), bg="#f2f2f2").pack()

tk.Label(root, text="Enter memorable items (e.g., name, memorable date, favorite word):", font=label_font, bg="#f2f2f2").pack(pady=(20, 5))
entry = tk.Entry(root, width=60, font=entry_font, bd=2, relief="groove")
entry.pack(ipady=4)

tk.Button(root, text="Generate Password", font=("Helvetica", 10, "bold"),
          bg="#4CAF50", fg="white", activebackground="#45a049",
          padx=10, pady=5, command=generate_password).pack(pady=15)

tk.Label(root, text="🔧 Generated Password:", font=label_font, bg="#f2f2f2").pack()
result_var = tk.StringVar()
tk.Entry(root, textvariable=result_var, width=60, font=entry_font, bd=2, relief="sunken", state='readonly').pack(ipady=4)

strength_var = tk.StringVar()
strength_display = tk.Label(root, textvariable=strength_var, font=("Helvetica", 12, "bold"), bg="#f2f2f2")
strength_display.pack(pady=(10,0))

root.mainloop()
