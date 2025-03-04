# main.py
import pygame
from game import loading_screen, start_game
# Main function to handle game flow 
def main():
    loading_screen() 
    start_game()

# Start the game
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")

