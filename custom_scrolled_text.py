import tkinter as tk
from tkinter import font as tkFont, ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import scrolledtext


class CustomScrolledText(ScrolledText):
    def __init__(self, master=None, **kw):
        self.scrollbar_background = '#000000'
        self.scrollbar_bar_background = '#141414'
        self.scrollbar_hover_background = 'silver'
        self.scrollbar_hover_bar_background = '#141414'
        # Set default width and height if not provided
        self.width = kw.pop('width', 70)
        self.height = kw.pop('height', 10)

        # Apply custom styling to the ScrolledText widget itself
        self.text_background = kw.pop('background', '#141414')
        self.text_foreground = kw.pop('foreground', 'silver')
        self.text_insert_background = kw.pop('insertbackground', 'silver')  # Color of the cursor
        self.custom_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

        super().__init__(
            master, **kw, font=self.custom_font,
            background=self.text_background,
            foreground=self.text_foreground,
            insertbackground=self.text_insert_background,
            height=self.height,
            width=self.width,
            wrap=tk.WORD
        )

        # Customize the scrollbar
        self.vbar = ttk.Scrollbar(self, orient='vertical')

        # Attach the scrollbar to the ScrolledText widget
        self.config(yscrollcommand=self.vbar.set)
        self.vbar['command'] = self.yview

        # Apply a custom style to the scrollbar
        style = ttk.Style()
        style.configure('Custom.TScrollbar', background=self.scrollbar_background)

        style.map('Custom.TScrollbar',
                  background=[('active', self.scrollbar_hover_background)])

        self.vbar.configure(style='Custom.TScrollbar')

        self.vbar.pack(side='right', fill='y')

        # Bind enter and leave events to the scrollbar
        self.vbar.bind("<Enter>", self.on_enter_scrollbar)
        self.vbar.bind("<Leave>", self.on_leave_scrollbar)

    def on_enter_scrollbar(self, e):
        # Change the colors to the hover colors
        self.vbar['background'] = self.scrollbar_hover_background
        self.vbar['troughcolor'] = self.scrollbar_hover_bar_background

    def on_leave_scrollbar(self, e):
        # Revert to the original colors
        self.vbar['background'] = self.scrollbar_background
        self.vbar['troughcolor'] = self.scrollbar_bar_background
