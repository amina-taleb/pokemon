# In this file, we have imported the differents images in order to create a gif
import pygame
import os

#load GIF frames
def load_gif_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)): # Ensure order
        if filename.endswith(".png"): # GIF frames should be PNGs
            # Load GIF as frames (assuming a single frame per gif in the folder)
            frame = pygame.image.load(os.path.join(folder_path, filename))
            frames.append(frame)
    return frames
