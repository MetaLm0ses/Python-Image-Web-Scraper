# Python Image Scraper

This Python application scrapes images from a specified website and saves them to a local directory. The application features a graphical user interface (GUI) built with `tkinter`, allowing users to input a website URL, choose a save directory, and start the scraping process with a progress bar and estimated time remaining.

## Features

- Scrapes images from any specified website
- Saves images to a user-defined local directory
- GUI built with `tkinter`
- Progress bar with estimated time remaining
- Reset button to clear inputs and progress

## Prerequisites

- Python 3.x

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/Python-Image-Web-Scraper.git
    cd Python-Image-Web-Scraper
    ```

2. Install the required libraries:

    ```sh
    pip install requests beautifulsoup4
    ```

## Usage

1. Run the application:

    ```sh
    python Website\ Image\ Scraper.py
    ```

2. Enter the website URL from which you want to scrape images.

3. Choose the directory where you want to save the images.

4. Click the "Start Scraping" button to begin the scraping process. The progress bar will show the progress, and the estimated time remaining will be displayed.

5. To clear the inputs and reset the progress, click the "Reset" button.

## Code Overview

- `install_package(package_name)`: Installs a Python package if not already installed.
- `sanitize_filename(filename)`: Sanitizes the filename by removing invalid characters.
- `get_file_extension(url)`: Extracts the file extension from a URL.
- `scrape_images(url, save_dir, progress, status_label)`: Main function to scrape images from the specified URL and save them to the local directory.
- `browse_directory()`: Opens a file dialog to select the save directory.
- `start_scraping()`: Starts the scraping process by calling `scrape_images`.
- `reset_fields()`: Resets the input fields, progress bar, and status label.

## Example

```sh
python Website\ Image\ Scraper.py
