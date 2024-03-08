import tkinter as tk
from tkinter import font as tkFont


class CustomButton(tk.Button):
    def __init__(self, master=None, **kw):
        self.default_background = kw.pop('background', '#141414')
        self.default_foreground = kw.pop('foreground', 'silver')
        self.hover_background = kw.pop('hover_background', 'silver')
        self.hover_foreground = kw.pop('hover_foreground', '#141414')

        # Use a modern font and larger size for the button text
        self.custom_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

        super().__init__(
            master, **kw,
            background=self.default_background, foreground=self.default_foreground,
            activebackground=self.hover_foreground, activeforeground=self.hover_background,
            cursor='hand2', relief='flat', font=self.custom_font
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.configure(background=self.hover_background, foreground=self.hover_foreground)

    def on_leave(self, e):
        self.configure(background=self.default_background, foreground=self.default_foreground)


class ModernButton(tk.Button):
    def __init__(self, master=None, padx=None, pady=None, **kw):
        # Define default and hover styles
        self.default_background = kw.pop('background', '#343a40')  # Dark gray
        self.default_foreground = kw.pop('foreground', '#f8f9fa')  # Light gray (almost white)
        self.hover_background = kw.pop('hover_background', '#495057')  # Slightly lighter gray
        self.hover_foreground = kw.pop('hover_foreground', '#ffffff')  # White
        self.padx = padx
        self.pady = pady

        # Use a modern font and larger size for the button text
        self.custom_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

        super().__init__(
            master, **kw,
            background=self.default_background, foreground=self.default_foreground,
            activebackground=self.hover_foreground, activeforeground=self.hover_background,
            cursor='hand2', relief='flat',
            font=self.custom_font,  # Apply the custom font to the button
            padx=self.padx, pady=self.pady  # Add some padding for a larger, more clickable area
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.configure(background=self.hover_background, foreground=self.hover_foreground)

    def on_leave(self, e):
        self.configure(background=self.default_background, foreground=self.default_foreground)
