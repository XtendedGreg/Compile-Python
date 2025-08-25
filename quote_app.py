# ------------------------------------------------------------------
# LIVE STREAM DEMO: "Quote of the Day" App with Gemini AI
# ------------------------------------------------------------------
#
# INSTRUCTIONS FOR YOUR LIVE STREAM:
#
# 1.  Prerequisites:
#     - Have Python installed.
#     - Have an icon file named `logo.ico` in the same folder as this script.
#     - Get a free Gemini API key from Google AI Studio.
#
# 2.  Terminal Commands to run during the stream:
#     -------------------------------------------------
#     # Step 1: Create and activate a virtual environment
#     python -m venv venv
#     venv\Scripts\activate
#
#     # Step 2: Install required packages
#     pip install pyinstaller requests
#
#     # Step 3: Run the final, complete build command
#     pyinstaller --onefile --windowed --icon="logo.ico" --add-data="logo.ico;." quote_app.py
#     -------------------------------------------------
#
# 3.  After the build, navigate to the `dist` folder to find and run
#     the final `quote_app.exe`.
#
# ------------------------------------------------------------------

# Filename: quote_app.py

import tkinter as tk
from tkinter import messagebox
import requests
import os
import sys
import json
import re

# --- IMPORTANT: Gemini API Configuration ---
# Get your free API key from Google AI Studio and paste it here.
API_KEY = "" # IMPORTANT: PASTE YOUR GEMINI API KEY HERE
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

# --- Helper Function for Assets ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Main Application Logic ---
def fetch_quote():
    """Fetches a random quote from the ZenQuotes API."""
    set_ui_state("loading")
    try:
        headers = {'User-Agent': 'MyQuoteApp/1.0'}
        response = requests.get("https://zenquotes.io/api/random", headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        quote_text = data[0].get('q', 'Quote not found.')
        author_text = data[0].get('a', 'Unknown Author')
        update_quote_display(quote_text, author_text)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Could not fetch quote. Please check your internet connection.\n\nError: {e}")
    except (KeyError, IndexError):
        messagebox.showerror("API Error", "The response from the quote API was invalid.")
    finally:
        set_ui_state("idle")

# --- GUI Management ---
def update_quote_display(quote, author):
    """Updates the main GUI labels with new text."""
    quote_label.config(text=f'"{quote}"')
    author_label.config(text=f'- {author}')

def set_ui_state(state):
    """Enables or disables buttons based on app state."""
    if state == "loading":
        status_label.config(text="Thinking...")
        for btn in all_buttons:
            btn.config(state=tk.DISABLED, cursor="")
    else: # idle
        status_label.config(text="")
        for btn in all_buttons:
            btn.config(state=tk.NORMAL, cursor="hand2")
    root.update_idletasks()


# --- GUI Setup ---
root = tk.Tk()
root.title("Quote of the Day")
root.geometry("600x450")
root.configure(bg="#2E3440")

try:
    icon_path = resource_path("logo.ico")
    root.iconbitmap(icon_path)
except tk.TclError:
    print("Icon file 'logo.ico' not found. Skipping.")

main_frame = tk.Frame(root, padx=20, pady=20, bg="#2E3440")
main_frame.pack(expand=True, fill=tk.BOTH)

quote_label = tk.Label(main_frame, text="Click the button below to fetch an inspirational quote!", font=("Inter", 14), wraplength=550, justify=tk.CENTER, fg="#D8DEE9", bg="#2E3440")
quote_label.pack(pady=(20, 10), expand=True)

author_label = tk.Label(main_frame, text="", font=("Inter", 12, "italic"), fg="#81A1C1", bg="#2E3440")
author_label.pack(pady=(0, 20))

# Button Frame
button_frame = tk.Frame(main_frame, bg="#2E3440")
button_frame.pack(pady=10)

fetch_button = tk.Button(button_frame, text="Get New Quote", command=fetch_quote, font=("Inter", 12, "bold"), bg="#5E81AC", fg="#ECEFF4", activebackground="#81A1C1", activeforeground="#ECEFF4", relief=tk.FLAT, padx=15, pady=10)
fetch_button.pack(side=tk.LEFT, padx=5)

all_buttons = [fetch_button]

# Status Label
status_label = tk.Label(main_frame, text="", font=("Inter", 10), fg="#A3BE8C", bg="#2E3440")
status_label.pack(pady=10)

root.mainloop()
