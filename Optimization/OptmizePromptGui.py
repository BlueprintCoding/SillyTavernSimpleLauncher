import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext
import tkinter.font as tkfont

# Create and activate a virtual environment
subprocess.call([sys.executable, "-m", "venv", "venv"])
venv_activate = "./venv/Scripts/activate"
subprocess.call(venv_activate, shell=True)

# Install required packages
subprocess.call([sys.executable, "-m", "pip", "install", "pyperclip"])
subprocess.call([sys.executable, "-m", "pip", "install", "nltk"])

import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import pyperclip

def stem_text():
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

def copy_text():
    text_to_copy = optimized_text.get("1.0", "end-1c")
    pyperclip.copy(text_to_copy)
    messagebox.showinfo("Text Copied", "The optimized text has been copied to the clipboard.")

def clear_text():
    text_entry.delete("1.0", "end")
    optimized_text.configure(state='normal')
    optimized_text.delete('1.0', 'end')
    optimized_text.configure(state='disabled')
    reduction_label.configure(text="Reduction Size: ")

# Create the main window
window = tk.Tk()
window.title("Text Stemming Tool")
window.configure(background='#343541')

# Create and position the text description label
description_label = tk.Label(window, text="Enter your text in the field below. The tool will perform stemming, remove stopwords and punctuation, and show the optimized text. This will help you optimize you prompts and characters to use less tokens. OpenAI and Poe will understand this truncated text like plain english.", bg='#343541', fg='white', wraplength=400, justify='center')
description_label.pack(pady=10)

# Create and position the text entry widget
text_label = tk.Label(window, text="Enter text:", bg='#343541', fg='white')
text_label.pack(pady=5)
text_entry = scrolledtext.ScrolledText(window, height=10, width=50, wrap=tk.WORD, bg='#23292e', fg='white')
text_entry.pack(padx=15)

# Create and position the stem button
stem_button = tk.Button(window, text="Stem Text", command=stem_text, bg='#1e88e5', fg='white')
stem_button.pack(pady=5)

# Create and position the clear button
clear_button = tk.Button(window, text="Clear Text", command=clear_text, bg='#757575', fg='white')
clear_button.pack(pady=5)

# Create and position the optimized text label
optimized_label = tk.Label(window, text="Optimized Text:", bg='#343541', fg='white')
optimized_label.pack(pady=10)

# Create and position the optimized text widget
optimized_text = scrolledtext.ScrolledText(window, height=10, width=50, wrap=tk.WORD, bg='#23292e', fg='white')
optimized_text.configure(state='disabled')
optimized_text.pack(padx=15)

# Create and position the copy button
copy_button = tk.Button(window, text="Copy to Clipboard", command=copy_text, bg='#4caf50', fg='white')
copy_button.pack(pady=5)

# Create and position the reduction size label
reduction_label = tk.Label(window, text="Reduction Size: ", bg='#343541', fg='white')
reduction_label.pack(pady=10)

# Configure font
font = tkfont.Font(family="Arial", size=10)
text_entry.configure(font=font)
optimized_text.configure(font=font)
reduction_label.configure(font=font)

# Start the GUI main loop
window.mainloop()

# Deactivate the virtual environment
subprocess.call("deactivate", shell=True)

