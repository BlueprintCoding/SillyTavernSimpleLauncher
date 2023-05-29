import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext
import tkinter.font as tkfont
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import pyperclip
import logging

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')


# Get the absolute path of the current directory
current_directory = os.path.abspath(os.path.dirname(sys.argv[0]))

# Create the "Logs" directory if it doesn't exist
logs_directory = os.path.join(current_directory, '..', 'Logs')
os.makedirs(logs_directory, exist_ok=True)

# Configure logging
log_file_path = os.path.join(logs_directory, 'OptimizeGuiError.log')
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def stem_text():
    try:
        input_text = text_entry.get("1.0", "end-1c")
        if not input_text:
            messagebox.showwarning("Warning", "Please enter some text.")
            return

        ps = PorterStemmer()
        stop_words = set(stopwords.words('english'))

        tokens = word_tokenize(input_text)
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words and word not in string.punctuation]
        stemmed_text = " ".join([ps.stem(word) for word in filtered_tokens])

        optimized_text.configure(state='normal')
        optimized_text.delete('1.0', 'end')
        optimized_text.insert('1.0', stemmed_text)
        optimized_text.configure(state='disabled')

        original_length = len(input_text)
        reduced_length = len(stemmed_text)
        reduction_size = (original_length - reduced_length) / original_length * 100

        reduction_label.configure(text="Reduction Size: {:.2f}%".format(reduction_size))
    except Exception as e:
        logging.error(f"Error in stem_text function: {e}")

def summarize_text(max_tokens=4096):
    try:
        input_text = text_entry.get("1.0", "end-1c")
        if not input_text:
            messagebox.showwarning("Warning", "Please enter some text.")
            return
        summary = summarizer.summarize(input_text)
        if len(summary) > max_tokens:
            summary = summary[:max_tokens]
        return summary

    except Exception as e:
        logging.error(f"Error in summarize_text function: {e}")


def copy_text():
    try:
        text_to_copy = optimized_text.get("1.0", "end-1c")
        pyperclip.copy(text_to_copy)
        messagebox.showinfo("Text Copied", "The optimized text has been copied to the clipboard.")
    except Exception as e:
        logging.error(f"Error in copy_text function: {e}")

def clear_text():
    try:
        text_entry.delete("1.0", "end")
        optimized_text.configure(state='normal')
        optimized_text.delete('1.0', 'end')
        optimized_text.configure(state='disabled')
        reduction_label.configure(text="Reduction Size: ")
    except Exception as e:
        logging.error(f"Error in clear_text function: {e}")

def center_window(window):
    try:
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        window.geometry(f"+{x}+{y}")
    except Exception as e:
        logging.error(f"Error in center_window function: {e}")

def close_window(event):
    try:
        window.destroy()
    except Exception as e:
        logging.error(f"Error in close_window function: {e}")

# Create the main window
window = tk.Tk()
window.title("Text Stemming Tool")
window.configure(background='#343541')


# Show the message box with the package list
messagebox.showinfo("Installed Packages", package_string)

# Create and position the text description label
description_label = tk.Label(window, text="Enter your text in the field below. The tool will perform stemming, remove stopwords and punctuation, and show the optimized text. This will help you optimize you prompts and characters to use less tokens. OpenAI and Poe will understand this truncated text like plain english.", bg='#343541', fg='white', wraplength=400, justify='center')
description_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create and position the text entry widget
text_label = tk.Label(window, text="Enter text:", bg='#343541', fg='white')
text_label.grid(row=1, column=0, pady=5)
text_entry = scrolledtext.ScrolledText(window, height=10, width=50, wrap=tk.WORD, bg='#23292e', fg='white')
text_entry.grid(row=1, column=1, padx=15)

# Create and position the stem button
stem_button = tk.Button(window, text="Stem Text", command=stem_text, bg='#1e88e5', fg='white')
stem_button.grid(row=2, column=0, pady=5)

# Create and position the summarize button
summarize_button = tk.Button(window, text="Summarize Text", command=summarize_text, bg='#FF9800', fg='white')
summarize_button.grid(row=2, column=1, pady=5)

# Create and position the clear button
clear_button = tk.Button(window, text="Clear Text", command=clear_text, bg='#757575', fg='white')
clear_button.grid(row=2, column=2, pady=5)

# Create and position the optimized text label
optimized_label = tk.Label(window, text="Optimized Text:", bg='#343541', fg='white')
optimized_label.grid(row=3, column=0, pady=10)

# Create and position the optimized text widget
optimized_text = scrolledtext.ScrolledText(window, height=10, width=50, wrap=tk.WORD, bg='#23292e', fg='white')
optimized_text.configure(state='disabled')
optimized_text.grid(row=3, column=1, padx=15)

# Create and position the copy button
copy_button = tk.Button(window, text="Copy to Clipboard", command=copy_text, bg='#4caf50', fg='white')
copy_button.grid(row=4, column=0, columnspan=2, pady=5)

# Create and position the reduction size label
reduction_label = tk.Label(window, text="Reduction Size: ", bg='#343541', fg='white')
reduction_label.grid(row=5, column=0, columnspan=2, pady=10)

# Configure font
font = tkfont.Font(family="Arial", size=10)
text_entry.configure(font=font)
optimized_text.configure(font=font)
reduction_label.configure(font=font)

# Bind the Ctrl+W event to the close_window function
window.bind("<Control-w>", close_window)

# Start the GUI main loop
center_window(window)
window.mainloop()
