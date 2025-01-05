import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps
import random

# Initialize the customTkinter window
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Guess the Character")
root.geometry("400x600")

# Global variables
guesses_left = 3
displayed_images = []

# Pixelation levels for different difficulties, including "Original" mode without pixelation
difficulty_levels = {
    "Original": {"pixel_size": None, "guesses": 5},
    "Easy": {"pixel_size": 15, "guesses": 5},
    "Medium": {"pixel_size": 30, "guesses": 3},
    "Hard": {"pixel_size": 50, "guesses": 2}
}

# Standardized image size
STANDARD_SIZE = (1300, 1000)

def prepare_image(image_path):
    """Resize each image to have a fixed height, center horizontally within a 300x300 canvas."""
    image = Image.open(image_path)
    target_height = STANDARD_SIZE[1]  # Fixed height (e.g., 300 pixels)
    aspect_ratio = image.width / image.height

    # Calculate new dimensions to match the fixed height while maintaining aspect ratio
    new_height = target_height
    new_width = int(new_height * aspect_ratio)

    # Resize image to the new width and fixed height
    image = image.resize((new_width, new_height), Image.LANCZOS)

    # Create a new canvas with a fixed size of 300x300 and a white background
    new_image = Image.new("RGB", STANDARD_SIZE, (255, 255, 255))
    
    # Paste the resized image onto the center of the canvas
    new_image.paste(image, ((STANDARD_SIZE[0] - new_width) // 2, 0))  # Center horizontally
    
    return new_image


def pixelate_image(image_path, pixel_size):
    """Load, standardize, and pixelate an image with a specified pixel size."""
    image = prepare_image(image_path)
    if pixel_size is None:  # If "Original" mode is selected, return the original image
        return image
    # Otherwise, pixelate the image
    small = image.resize((image.width // pixel_size, image.height // pixel_size), Image.NEAREST)
    pixelated_image = small.resize(image.size, Image.NEAREST)
    return pixelated_image

def display_image(image_path, pixel_size):
    """Display an image (pixelated or original) in the customTkinter window."""
    image_to_show = pixelate_image(image_path, pixel_size)
    tk_image = ImageTk.PhotoImage(image_to_show)
    image_label.configure(image=tk_image)
    image_label.image = tk_image

def show_original_image(image_path):
    """Display the original, unpixelated image for a brief moment."""
    original_image = prepare_image(image_path)  # Get the original image
    tk_image = ImageTk.PhotoImage(original_image)
    image_label.configure(image=tk_image)
    image_label.image = tk_image

def start_game():
    """Initialize a new game by selecting a character and setting guesses based on difficulty."""
    global answer, guesses_left, displayed_images
    difficulty = difficulty_var.get()
    guesses_left = difficulty_levels[difficulty]["guesses"]
    update_guess_label()
    feedback_label.configure(text="")  # Clear any previous feedback

    # Check if all images have been displayed
    if len(displayed_images) == len(characters):
        feedback_label.configure(text="All characters guessed! Starting new round.", text_color="blue")
        displayed_images = []

    # Select a new random character that hasn't been shown yet
    remaining_characters = {k: v for k, v in characters.items() if k not in displayed_images}
    answer, image_path = random.choice(list(remaining_characters.items()))
    displayed_images.append(answer)
    
    pixel_size = difficulty_levels[difficulty]["pixel_size"]
    display_image(image_path, pixel_size)
    guess_entry.delete(0, ctk.END)

def update_guess_label():
    """Update the label showing the number of guesses remaining."""
    guess_label.configure(text=f"Guesses Left: {guesses_left}")

def check_guess(event=None):
    """Check if the user's guess is correct."""
    global guesses_left
    guess = guess_entry.get().strip().lower()

    if guess == answer.lower():
        feedback_label.configure(text="Correct!", text_color="green")
        show_original_image(characters[answer])  # Show original image after correct guess
        root.after(2000, start_game)  # Wait 2 seconds before starting a new game
    else:
        guesses_left -= 1
        update_guess_label()
        feedback_label.configure(text="Wrong! Try again.", text_color="red")
        
        if guesses_left <= 0:
            feedback_label.configure(text=f"Out of guesses! The character was {answer}.", text_color="red")
            show_original_image(characters[answer])  # Show original image after incorrect guess
            root.after(2000, start_game)  # Wait 2 seconds before starting a new game

# Character images (you can add more)
characters = {
    "Luke": "images/luke_skywalker.png",
    "Kylo Ren": "images/kylo_ren.png",
    "R2D2": "images/r2d2.png",
    "Boba Fett" : "images/boba_fett.png",
    "Ahsoka" : "images/ahsoka_tano.png",
    "C3PO" : "images/c3po.png",
    "Rex" : "images/captain_rex.png",
    "Din Djarin" : "images/din_djarin.png",
    "Lando" : "images/lando_calrissian.png",
    "Leia" : "images/leia_organa.png",
    "Mace Windu": "images/mace_windu.png",
    "Obi-wan": "images/obiwan_kenobi.png",
    "Qui-gon": "images/quigon_jinn.png",
    "Rey": "images/rey.png",
    "Yoda" : "images/yoda.png",
    "Ackbar": "images/admiral_ackbar.png",
    "Anakin": "images/anakin_skywalker.png",
    "BB8" : "images/bb-8.png",
    "Bo-Katan": "images/bo_katan.png",
    "Chewbacca": "images/chewbacca.png",
    "Dooku": "images/count_dooku.png",
    "Maul": "images/darth_maul.png",
    "Grievous": "images/general_grievous.png",
    "Han Solo" : "images/han_solo.png",
    "Jabba": "images/jabba_the_hutt.png",
    "Padme": "images/padme_amidala.png",
    "Palpatine": "images/palpatine.png",
    "Qi'ra": "images/qira.png"
}

# Widgets and Layout
difficulty_var = ctk.StringVar(value="Medium")  # Default difficulty

# Difficulty Option Menu
difficulty_label = ctk.CTkLabel(root, text="Select Difficulty:")
difficulty_label.pack(pady=5)
difficulty_menu = ctk.CTkOptionMenu(root, variable=difficulty_var, values=list(difficulty_levels.keys()))
difficulty_menu.pack(pady=5)

# Image label for displaying the pixelated image
image_label = ctk.CTkLabel(root, text="")
image_label.pack(pady=20)

# Label for remaining guesses
guess_label = ctk.CTkLabel(root, text="Guesses Left:")
guess_label.pack(pady=5)

# Entry box for the player's guess
guess_entry = ctk.CTkEntry(root, font=("Arial", 14))
guess_entry.pack(pady=10)
guess_entry.bind("<Return>", check_guess)  # Bind the Enter key to submit

# Label for feedback
feedback_label = ctk.CTkLabel(root, text="", font=("Arial", 12))
feedback_label.pack(pady=5)

# Button to submit the guess
submit_button = ctk.CTkButton(root, text="Submit Guess", command=check_guess)
submit_button.pack(pady=5)

# Start button to begin the game
start_button = ctk.CTkButton(root, text="Start Game", command=start_game)
start_button.pack(pady=10)

# Start the game for the first time
start_game()

# Run the customTkinter main loop
root.mainloop()
