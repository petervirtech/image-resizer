#!/usr/bin/env python3
"""
Automatisch afbeeldingen optimalisatie script
Download originele bestanden, comprimeer en converteer naar WebP
"""

import os
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

# Basis URL van je website
BASE_URL = os.getenv("BASE_URL")

# Output folder voor geoptimaliseerde afbeeldingen
OUTPUT_FOLDER = "optimized_images"

import json

# Load images to optimize from JSON file
with open("images_to_optimize.json", "r", encoding="utf-8") as f:
    IMAGES_TO_OPTIMIZE = json.load(f)

def download_image(url):
    """Download afbeelding van URL"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        return None

def optimize_and_convert(image, target_width, target_height, quality=85):
    """
    Resize afbeelding naar target afmetingen en optimaliseer
    Behoudt aspect ratio indien nodig
    """
    # Resize met behoud van aspect ratio
    image.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Converteer naar RGB als het RGBA is (voor WebP compatibiliteit)
    if image.mode in ('RGBA', 'LA', 'P'):
        # Maak witte achtergrond
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')
    
    return image

def process_image(image_info):
    """Verwerk één afbeelding: download, resize, converteer en opslaan"""
    path = image_info['path']
    width = image_info['width']
    height = image_info['height']
    
    # Constructeer URL
    url = BASE_URL + path
    
    # Extract bestandsnaam en maak nieuwe naam
    original_filename = os.path.basename(path)
    name_without_ext = os.path.splitext(original_filename)[0]
    new_filename = f"{name_without_ext}.webp"
    
    # Maak subfolder structuur
    relative_dir = os.path.dirname(path).lstrip('/')
    output_dir = os.path.join(OUTPUT_FOLDER, relative_dir)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    output_path = os.path.join(output_dir, new_filename)
    
    print(f"\n📥 Verwerken: {original_filename}")
    print(f"   URL: {url}")
    print(f"   Target: {width}x{height}")
    
    # Download afbeelding
    image = download_image(url)
    if image is None:
        return False
    
    original_size = len(requests.get(url).content) / 1024  # KB
    print(f"   Originele grootte: {original_size:.1f} KB")
    
    # Optimaliseer en resize
    optimized_image = optimize_and_convert(image, width, height)
    
    # Opslaan als WebP
    optimized_image.save(
        output_path,
        'WEBP',
        quality=85,
        method=6  # Beste compressie methode
    )
    
    new_size = os.path.getsize(output_path) / 1024  # KB
    savings = ((original_size - new_size) / original_size) * 100
    
    print(f"   ✅ Opgeslagen: {output_path}")
    print(f"   Nieuwe grootte: {new_size:.1f} KB")
    print(f"   Besparing: {savings:.1f}%")
    
    return True

def main():
    """Hoofdfunctie"""
    print("=" * 80)
    print("AFBEELDINGEN OPTIMALISATIE SCRIPT")
    print("=" * 80)
    print(f"\nOutput folder: {OUTPUT_FOLDER}/")
    print(f"Aantal afbeeldingen: {len(IMAGES_TO_OPTIMIZE)}")
    print(f"Basis URL: {BASE_URL}")
    
    # Maak output folder
    Path(OUTPUT_FOLDER).mkdir(exist_ok=True)
    
    # Verwerk alle afbeeldingen
    successful = 0
    failed = 0
    
    for image_info in IMAGES_TO_OPTIMIZE:
        if process_image(image_info):
            successful += 1
        else:
            failed += 1
    
    # Samenvatting
    print("\n" + "=" * 80)
    print("SAMENVATTING")
    print("=" * 80)
    print(f"✅ Succesvol: {successful}")
    print(f"❌ Mislukt: {failed}")
    print(f"\nAlle geoptimaliseerde bestanden staan in: {OUTPUT_FOLDER}/")
    print("\nVervang de originele bestanden met de WebP versies en update je HTML/CSS")

if __name__ == "__main__":
    # Check of PIL/Pillow geïnstalleerd is
    try:
        from PIL import Image
        import requests
    except ImportError:
        print("⚠️  Vereiste libraries niet gevonden!")
        print("\nInstalleer met:")
        print("pip install Pillow requests")
        exit(1)
    
    main()
