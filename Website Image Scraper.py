import subprocess
import sys
import requests
from bs4 import BeautifulSoup
import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import re
import time
from urllib.parse import urlparse, urljoin, unquote

# Function to install a package
def install_package(package_name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])

# Check and install BeautifulSoup4 if not installed
try:
    import bs4
except ImportError:
    print("BeautifulSoup4 is not installed. Installing now...")
    install_package('beautifulsoup4')

# Check and install requests if not installed
try:
    import requests
except ImportError:
    print("Requests is not installed. Installing now...")
    install_package('requests')

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def get_file_extension(url):
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    return os.path.splitext(path)[1]

def scrape_images(url, save_dir, progress, status_label):
    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Fetch the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')
    total_images = len(img_tags)
    
    if total_images == 0:
        messagebox.showinfo("No Images", "No images found on the provided URL.")
        return

    # Initialize progress bar
    progress['maximum'] = total_images

    start_time = time.time()

    # Download and save each image
    for i, img in enumerate(img_tags, start=1):
        img_url = img.get('src')
        if not img_url:
            continue
        img_url = urljoin(url, img_url)

        # Filter out invalid URLs
        if 'scorecardresearch.com' in img_url or 'spaceball.gif' in img_url:
            continue

        try:
            # Get the image response
            img_response = requests.get(img_url, stream=True)
            img_response.raise_for_status()

            file_extension = get_file_extension(img_url)
            img_name = os.path.join(save_dir, sanitize_filename(os.path.basename(img_url.split('?')[0])))

            # Ensure the filename has the correct extension
            if not img_name.lower().endswith(file_extension.lower()):
                img_name += file_extension

            # Save the image locally
            with open(img_name, 'wb') as file:
                shutil.copyfileobj(img_response.raw, file)

            print(f"Saved: {img_name}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to save {img_url}: {e}")

        # Update progress bar
        progress['value'] = i
        elapsed_time = time.time() - start_time
        estimated_total_time = (elapsed_time / i) * total_images
        remaining_time = estimated_total_time - elapsed_time
        status_label.config(text=f"Downloading images... {i}/{total_images} - ETA: {int(remaining_time)}s")
        root.update_idletasks()

    messagebox.showinfo("Done", f"All valid images have been saved to {save_dir}")

def browse_directory():
    directory = filedialog.askdirectory()
    entry_save_dir.delete(0, tk.END)
    entry_save_dir.insert(0, directory)

def start_scraping():
    url = entry_url.get()
    save_dir = entry_save_dir.get()
    if not url or not save_dir:
        messagebox.showwarning("Input Error", "Please provide both URL and directory.")
        return
    scrape_images(url, save_dir, progress_bar, status_label)

def reset_fields():
    entry_url.delete(0, tk.END)
    entry_save_dir.delete(0, tk.END)
    progress_bar['value'] = 0
    status_label.config(text="")

# Create the main window
root = tk.Tk()
root.title("Website Image Scraper")

# Configure grid weights for scalability
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)

# URL input
label_url = tk.Label(root, text="Website URL:")
label_url.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_url = tk.Entry(root, width=50)
entry_url.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="we")

# Directory input
label_save_dir = tk.Label(root, text="Save Directory:")
label_save_dir.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_save_dir = tk.Entry(root, width=50)
entry_save_dir.grid(row=1, column=1, padx=10, pady=10, sticky="we")
button_browse = tk.Button(root, text="Browse", command=browse_directory)
button_browse.grid(row=1, column=2, padx=10, pady=10, sticky="e")

# Start button
button_start = tk.Button(root, text="Start Scraping", command=start_scraping)
button_start.grid(row=2, column=1, padx=10, pady=10, sticky="e")

# Reset button
button_reset = tk.Button(root, text="Reset", command=reset_fields)
button_reset.grid(row=2, column=2, padx=10, pady=10, sticky="w")

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="we")

# Status label
status_label = tk.Label(root, text="")
status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="we")

# Run the GUI event loop
root.mainloop()