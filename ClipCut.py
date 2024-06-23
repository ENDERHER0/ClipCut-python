import tkinter as tk
import os
from tkinter import messagebox, ttk

from moviepy.editor import *
from pytube import YouTube


def download_and_cut():
    url = url_entry.get()
    fileName = fileName_entry.get()
    parentDirector = ""
    videoMaxLength = float(videoMaxLength_var.get())

    try:
        if not os.path.exists(fileName):
            os.makedirs("YoutubeDownloads/" + fileName)

        yt = YouTube(url)
        mp4Stream = yt.streams.filter(file_extension="mp4", res="720p").first()
        print("Format: MP4")
        print("Resolution: 720p")
        latestDownload = mp4Stream.download(output_path="YoutubeDownloads")

        clip = VideoFileClip(latestDownload)
        audio = AudioFileClip(latestDownload)

        duration = float(clip.duration)
        print("Duration: " + str(duration))

        clipMaxDuration = videoMaxLength
        clipDuration = 0
        cut = 0
        extraCut = 0

        while duration >= clipMaxDuration:
            if videoMaxLength * 2 > duration > videoMaxLength:
                cut += 1
                extraCut = int(duration)
                break
            duration -= clipMaxDuration
            cut += 1

        print("Total Clips: " + str(cut))
        print("Extra Video: " + str(extraCut))

        # Create progress bar for both download and cut
        progress_bar["maximum"] = 100
        progress_bar["value"] = 0
        root.update()

        for i in range(cut):
            newClip = clip
            newAudio = audio

            print("Cutting Video")

            if i < cut - 1:
                newClip = newClip.subclip(clipDuration, clipMaxDuration)
                newAudio = newAudio.subclip(clipDuration, clipMaxDuration)
                newAudio.cutout(newClip.duration, newAudio.duration)
            else:
                newClip = newClip.subclip(clipDuration, clipDuration + extraCut)
                newAudio = newAudio.subclip(clipDuration, clipDuration + extraCut)
                newAudio.cutout(extraCut, newAudio.duration)

            newClip.write_videofile("YoutubeDownloads/" + fileName + "/Clip_" + str(i + 1) + ".mp4")
            print("Video: " + str(i + 1) + " Saved")
            clipDuration += videoMaxLength
            clipMaxDuration += videoMaxLength

            # Update progress bar
            progress_bar["value"] = (i + 1) * (100 / cut)
            root.update()

        messagebox.showinfo("Process Completed", "Videos downloaded and cut successfully.")
        progress_bar["value"] = 0

        # Reset input values after process completion
        reset_inputs()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        progress_bar["value"] = 0


def reset_inputs():
    url_entry.delete(0, tk.END)
    fileName_entry.delete(0, tk.END)
    videoMaxLength_var.set("60")  # Default value


# Create main window
root = tk.Tk()
root.title("ClipCut")

# Set window size, background color, and padding
root.geometry("600x300")  # Reduced height
root.configure(bg="black")
root.configure(padx=20, pady=20)

# Set font style
font_style = ("Arial", 12)

# Create and place elements using grid
title_label = tk.Label(root, text="ClipCut", font=("Arial", 20, "bold"), fg="white", bg="black")
title_label.grid(row=0, column=0, pady=(10, 20), columnspan=2, sticky="n")

url_label = tk.Label(root, text="YouTube URL:", font=font_style, fg="white", bg="black")
url_label.grid(row=1, column=0, pady=5, sticky="w")
url_entry = tk.Entry(root, font=font_style, width=40)  # Wider text box
url_entry.grid(row=1, column=1, pady=5, sticky="w")

fileName_label = tk.Label(root, text="File Name:", font=font_style, fg="white", bg="black")
fileName_label.grid(row=2, column=0, pady=5, sticky="w")
fileName_entry = tk.Entry(root, font=font_style, width=20)  # Shorter text box
fileName_entry.grid(row=2, column=1, pady=5, sticky="w")

videoMaxLength_label = tk.Label(root, text="Video Max Length (seconds):", font=font_style, fg="white", bg="black")
videoMaxLength_label.grid(row=3, column=0, pady=5, sticky="w")
videoMaxLength_var = tk.StringVar(value="60")  # Default value
videoMaxLength_entry = tk.Spinbox(root, from_=1, to=float('inf'), textvariable=videoMaxLength_var, font=font_style,
                                  width=10)  # No maximum limit
videoMaxLength_entry.grid(row=3, column=1, pady=5, sticky="w")

download_button = tk.Button(root, text="Download and Cut Video", command=download_and_cut, font=font_style)
download_button.grid(row=4, column=0, columnspan=2, pady=(20, 10), sticky="n")

# Create a single progress bar
progress_bar = ttk.Progressbar(root, length=500, mode="determinate")
progress_bar.grid(row=5, column=0, columnspan=2, pady=10, sticky="n")

# Start the GUI event loop
root.mainloop()
