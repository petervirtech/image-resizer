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


```
uv pip install Pillow requests
```

## Usage

Run the `optimize_images.py` script:

```
uv python optimize_images.py
```

The script will download and optimize the images listed in the script and save them in the `optimized_images` folder.

## Notes

- The base URL and image paths are configured in the script.
- The output folder can be changed in the script.
- Make sure to update your HTML/CSS to use the optimized WebP images.
