# Image Resizer and Optimizer

This project contains a Python script to automatically download, resize, and optimize images from a specified base URL. The optimized images are saved in WebP format in a designated output folder.

## Features

- Downloads images from a base URL.
- Resizes images to specified dimensions while maintaining aspect ratio.
- Converts images to WebP format for better compression.
- Saves optimized images in a structured output folder.

## Requirements

- Python 3.13 or higher
- Pillow
- requests

## Installation

This project uses [uv](https://github.com/indygreg/pyuv) to manage Python versions and virtual environments. Make sure you have `uv` installed and configured.

To install the required packages, first activate your environment with `uv`, then run:

```
uv pip install Pillow requests python-dotenv
```

## Configuration

- The `BASE_URL` for the images is stored in the `.env` file. This file is loaded automatically by the script using `python-dotenv`.
- A `.env.example` file is provided as a template. Copy this file to `.env` and update the `BASE_URL` value to your own base URL.
- The list of images to optimize is stored in `images_to_optimize.json`. You can edit this file to add or remove images and specify their target dimensions.

## Usage

Run the project by executing:

```
uv python main.py
```

This will run the `main.py` script, which calls the image optimization process.

## Notes

- The output folder can be changed in the script.
- Make sure to update your HTML/CSS to use the optimized WebP images.
