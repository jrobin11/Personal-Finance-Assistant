import tkinter as tk
from tkinter import ttk

# Color and Font Styles
BG_COLOR = "#1f2833"
BUTTON_COLOR = "#66fcf1"
BUTTON_HOVER_COLOR = "#45a29e"
TEXT_COLOR = "#0b0c10"
ENTRY_BG = "#ffffff"
FONT = ("Arial", 12)
HEADER_FONT = ("Arial", 14, "bold")

# Style Configuration Function
def configure_styles():
    style = ttk.Style()

    style.theme_use("default")

    style.configure("Header.TLabel", 
                    background=BG_COLOR, 
                    foreground="#66fcf1",  # Change to desired text color
                    font=HEADER_FONT)
    style.configure("TButton", font=FONT, padding=6, background=BUTTON_COLOR, foreground=TEXT_COLOR)
    style.map("TButton", background=[("active", BUTTON_HOVER_COLOR)])

    style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=FONT)
    style.configure("Header.TLabel", font=HEADER_FONT)

    style.configure("TEntry", padding=5, fieldbackground=ENTRY_BG, foreground=TEXT_COLOR, font=FONT)
    style.configure("TFrame", background=BG_COLOR)