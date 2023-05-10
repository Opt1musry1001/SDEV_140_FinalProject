# Python GUI program that allows the user to
# translate a message to or from Morse Code.
# Author: Ryan Moore
# Last updated: 5/9/23
# SDEV_140_FinalProject.py


# Import tkinter libraries.
import tkinter as tk
import tkinter.messagebox as messagebox

# Define a dictionary for translating.
morse_dict = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.', 'h': '....',
    'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 'p': '.--.',
    'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', ' ': '/'
}


# Function to get input and call translate functions.
def translate_text(input_box, output_box, translation_function):
    # Get the input text from the input box.
    input_text = input_box.get('1.0', tk.END).strip()  # input_text contains the text entered into the input box.

    # Clear the output box.
    output_box.delete('1.0', tk.END)

    # Translate the input text.
    try:
        # Split the input text into lines.
        lines = input_text.split('\n')  # lines contains the lines in the input text.

        # Translate each line and join them with newline characters.
        translated_lines = [translation_function(line.strip()) for line in lines]  # Holds translated lines of text.

        translated_text = '\n'.join(translated_lines)  # translated_text holds the translated lines joined together.

    except ValueError as e:
        # Display an error message if input is invalid.
        output_box.insert(tk.END, str(e))
        return

    # Display the translated text in the output box.
    output_box.insert(tk.END, translated_text)


# Function to translate regular text into Morse Code.
def text_to_morse(input_text):
    # Get the input text and convert to lowercase.
    text = input_text.lower()           # text holds the text passed to the function to translate.

    # Validate the input text.
    if not all(char.isalnum() or char.isspace() for char in text):
        messagebox.showerror('Error', 'Invalid characters. Only alphanumeric characters and spaces allowed.')
        return

    # Translate the text to Morse Code, character by character.
    morse_code = ''         # morse_code holds the complete string of translated Morse Code text.
    for char in text:
        if char == ' ':
            morse_code += ' '
        elif char == '\n':
            morse_code += '\n'
        else:
            morse_code += morse_dict[char] + ' '

    # Return translated string containing Morse Code.
    return morse_code


# Define the function to translate Morse Code to text.
def morse_to_text(input_text):
    # Get the input Morse code and convert to lowercase.
    morse_code = input_text.strip()     # morse_code holds the text passed to the function to translate.

    # Validate the input Morse code.
    if not all(char in '-. /\n' for char in morse_code):
        messagebox.showerror('Error', 'Invalid characters. Only dots, dashes, spaces, and newlines allowed.')
        return

    # Translate the Morse code to text, character by character.
    # Also evaluates each character to make sure it is a recognized Morse symbol.
    text = ''           # text holds the complete string of translated English text.
    morse_code_list = morse_code.split('\n')
    for code in morse_code_list:
        if code == '':
            text += '\n'
        else:
            code_list = code.split(' ')
            for c in code_list:
                if c == '':
                    text += ' '
                elif c not in morse_dict.values():
                    messagebox.showerror('Error', 'Invalid Morse code sequence: {}'.format(c) +
                                         "\nPlease separate characters with spaces.")
                    return
                else:
                    text += list(morse_dict.keys())[list(morse_dict.values()).index(c)]

    return text


# Create window for Morse Code key.
def create_key_window():
    # Create the window.
    key_window = tk.Toplevel(root)      # key_window is the variable for the Morse Code key window.
    key_window.configure(bg='#9ff279')
    key_window.title("Morse Code Key")

    # Load the Morse Code key image.
    morse_code_key = tk.PhotoImage(file="morse_code_key.png")       # Holds the image file for the Morse Code key.

    # Create the label to display the image.
    key_label = tk.Label(key_window, image=morse_code_key, text="Morse Code Key")   # Label for the image.
    key_label.image = morse_code_key
    key_label.pack()


# Create main window, called root.
root = tk.Tk()      # root is the variable for the main home page window.
root.title("Morse Code Translator")

# Set the window size and background color
root.geometry("400x300")
root.configure(bg='#9ff279')

# Create welcome label for main window.
welcome_label = tk.Label(root, text="Welcome to the Morse Code Translator!", bg='#9ff279')  # Main page greeting label.
welcome_label.pack(pady=10)

# Create button for translating into Morse Code.
to_morse_button = tk.Button(root, text="Translate to Morse Code", bg='#6fa8dc',
                            command=lambda: create_translation_window("Translate to Morse Code", text_to_morse))
to_morse_button.pack(pady=10)       # to_morse_button is a button that opens the appropriate translation window.

# Create button for translating into regular text.
from_morse_button = tk.Button(root, text="Translate from Morse Code", bg='#6fa8dc',
                              command=lambda: create_translation_window("Translate From Morse Code", morse_to_text))
from_morse_button.pack(pady=10)     # from_morse_button is a button that opens the appropriate translation window.

# Load the Telegraph image.
telegraph_image = tk.PhotoImage(file="Telegraph.png")   # Holds the telegraph image file.

# Resize the image to fit the window.
resized_telegraph_image = telegraph_image.subsample(2, 2)   # Holds the resized telegraph image file.

# Create the label to display the image.
telegraph_label = tk.Label(root, image=resized_telegraph_image, text="Morse Code Telegraph", )  # Label for the image.
telegraph_label.image = resized_telegraph_image
telegraph_label.pack()


# Create window for translation.
# Name of window and function of button depends on which button was pressed on the main window.
def create_translation_window(title, translation_function):
    # Create the window.
    translation_window = tk.Toplevel(root)      # translation_window is the variable for the translation window.
    translation_window.title(title)
    translation_window.configure(bg='#9ff279')

    # Create the input box.
    input_label = tk.Label(translation_window, text="Input:", bg='#9ff279')     # Label for the input box.
    input_label.pack()

    input_box = tk.Text(translation_window, height=5)   # Text box to hold input.
    input_box.pack()

    # Create the output box.
    output_label = tk.Label(translation_window, text="Output:", bg='#9ff279')   # Label for the output box.
    output_label.pack()

    output_box = tk.Text(translation_window, height=5)  # Text box to hold output.
    output_box.pack()

    # Create the translation button. Function corresponds with which button was pressed on the main window.
    translation_button = tk.Button(translation_window, text="Translate", bg='#6fa8dc',
                                   command=lambda: translate_text(input_box, output_box, translation_function))
    translation_button.pack(pady=10)    # Button to translate text in the appropriate manner.

    # Create the Morse Code key button.
    key_button = tk.Button(translation_window, text="Morse Code Key", command=create_key_window, bg='#6fa8dc')
    key_button.pack()   # Button to open the Morse Code Key window.


# Main function definition. Instantiates and pops up the window.
def main():
    root.mainloop()


# Call the main function.
if __name__ == "__main__":
    main()
