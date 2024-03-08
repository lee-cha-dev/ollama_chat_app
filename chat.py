import json
import subprocess
import tkinter as tk
from tkinter import messagebox
import requests
import customtkinter as ck
from customtkinter import CTk, CTkButton
from model_path import OLLAMA_EXE_PATH, LLAMA2_MODEL


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Llama Chat")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.configure(bg="#000000")
        self.window_width = 800
        self.window_height = 600
        self.geometry(f"{self.window_width}x{self.window_height}")
        self.minsize(width=self.window_width, height=self.window_height)

        self.font = ck.CTkFont(family="Roboto", size=13, weight="bold")

        # CONFIG THE ROWS & COLUMNS
        self.grid_rowconfigure(0, weight=9)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        start_command = f"{OLLAMA_EXE_PATH} run {LLAMA2_MODEL}"
        self.ollama_process = subprocess.Popen(start_command, shell=True)

        # Create a scrolled text widget for the chat history
        self.chat_history_frame = ck.CTkFrame(self)
        self.chat_history_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

        self.chat_history = ck.CTkTextbox(
            self.chat_history_frame, fg_color="#141414", text_color="silver", font=self.font
        )
        self.chat_history.pack(padx=10, pady=10, side="left", fill="both", expand=True)

        # Create a frame for the user input field and send button
        self.input_frame = ck.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        # Create the user input field
        self.user_input = ck.CTkTextbox(
            self.input_frame, fg_color="#141414", text_color="silver", font=self.font
        )
        self.user_input.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        self.user_input.bind("<Return>", self.send_message)
        self.user_input.bind("<Shift-Return>", self.insert_newline)

        # Create the send button
        self.send_button = CTkButton(
            self.input_frame, text="Send", fg_color="#141414",
            text_color="silver", font=self.font
        )
        self.send_button.pack(
            side="right", padx=(2, 10), pady=10, fill="y"
        )
        self.send_button.bind("<Enter>", self.on_enter)
        self.send_button.bind("<Leave>", self.on_leave)
        self.send_button.bind("<Button-1>", self.button_press)
        self.send_button.bind("<ButtonRelease-1>", self.on_enter)

        self.initialize_chat()

    def on_enter(self, e):
        self.send_button.configure(fg_color="silver")
        self.send_button.configure(text_color="#141414")

    def on_leave(self, e):
        self.send_button.configure(fg_color="#141414")
        self.send_button.configure(text_color="silver")

    def button_press(self, e):
        self.send_button.configure(text="Loading", fg_color="#ffffff")
        self.update()
        self.send_message()

    def button_release(self, e):
        self.send_button.configure(fg_color="#141414", text="Send")
        self.update()

    def insert_newline(self, event=None):
        self.user_input.insert(ck.INSERT, "\n")
        return "break"

    def get_model_response(self, message):
        api_url = "http://localhost:11434/api/generate"
        data = {
            "model": "llama2:13b",
            "prompt": message
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(api_url, json=data, headers=headers)
            response.raise_for_status()  # This will raise for HTTP errors

            # Split the response by newlines and parse each JSON object individually
            parts = response.text.strip().split('\n')
            full_response = ""
            for part in parts:
                json_part = json.loads(part)
                full_response += json_part.get("response", "")
                if json_part.get("done", False):
                    break  # Stop if the part indicates the response is complete

            return full_response
        except requests.RequestException as e:
            print(f"Error communicating with the model API: {e}")
            return "Error: Could not get a response from the model."
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return "Error: Invalid response format."

    def send_message(self, event=None):
        user_message = self.user_input.get("1.0", "end-1c")  # Get text from Text widget
        if not user_message.strip():
            self.send_button.configure(fg_color="#141414", text="Send")
            return "break"

        self.chat_history.configure(state="normal")
        self.chat_history.insert(tk.END, "You:\n" + user_message + "\n")
        self.chat_history.configure(state="disabled")
        self.chat_history.see(tk.END)

        model_response = self.get_model_response(user_message)
        self.chat_history.configure(state="normal")
        self.chat_history.insert(tk.END, "\nLlama:" + model_response + "\n\n")
        self.chat_history.configure(state="disabled")
        self.chat_history.see(tk.END)

        self.user_input.delete("1.0", "end-1c")

        self.send_button.configure(fg_color="#141414", text="Send")

        return "break"

    def initialize_chat(self):
        self.user_input.insert(
            tk.END,
            "A new chat has started (do not respond to this). "
            "Provide a general greeting to the user and ask "
            "them what they would like to talk about or need assistance with."
        )
        user_message = self.user_input.get("1.0", "end-1c")  # Get text from Text widget
        if not user_message.strip():
            return "break"

        if not user_message.strip():
            return "break"

        model_response = self.get_model_response(user_message)
        self.chat_history.configure(state="normal")
        self.chat_history.insert(tk.END, "Llama:" + model_response + "\n\n")
        self.chat_history.configure(state="disabled")
        self.chat_history.see(tk.END)

        self.user_input.delete("1.0", "end-1c")

    def on_exit(self):
        # Ask user for confirmation before exiting
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Terminate the Ollama subprocess before exiting
            self.ollama_process.terminate()
            self.destroy()
