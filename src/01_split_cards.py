#!/usr/bin/env python3
"""
Script to split sprite sheet into individual cards with configurable grid layout
"""

from PIL import Image
import os
import yaml

def load_config(config_path="config.yaml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    # Load configuration
    config = load_config()

    # Extract configuration values
    input_file = config['paths']['input_sprite']
    output_dir = config['paths']['output_individual_cards']

    sprite_rows = config['sprite_sheet']['rows']
    sprite_cols = config['sprite_sheet']['cols']
    total_cards = config['sprite_sheet']['total_cards']

    target_width_inches = config['card']['width_inches']
    target_height_inches = config['card']['height_inches']
    dpi = config['card']['dpi']

    # Validate configuration
    if sprite_rows * sprite_cols != total_cards:
        raise ValueError(f"Grid dimensions ({sprite_rows}x{sprite_cols}={sprite_rows*sprite_cols}) don't match total_cards ({total_cards})")

    # Convert target size to pixels
    target_width_px = int(target_width_inches * dpi)
    target_height_px = int(target_height_inches * dpi)

    # Load the sprite sheet
    img = Image.open(input_file)
    img_width, img_height = img.size

    print(f"Original sprite sheet size: {img_width}x{img_height} pixels")
    print(f"Grid layout: {sprite_rows} rows × {sprite_cols} columns = {total_cards} cards")

    # Calculate individual card size from the source image
    card_width = img_width // sprite_cols
    card_height = img_height // sprite_rows

    print(f"Source card size: {card_width}x{card_height} pixels")
    print(f"Target card size: {target_width_px}x{target_height_px} pixels ({target_width_inches}x{target_height_inches} inches at {dpi} DPI)")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Split and save each card
    card_num = 1
    for row in range(sprite_rows):
        for col in range(sprite_cols):
            # Calculate crop box for this card
            left = col * card_width
            top = row * card_height
            right = left + card_width
            bottom = top + card_height

            # Crop the card
            card = img.crop((left, top, right, bottom))

            # Scale to target size
            card_resized = card.resize((target_width_px, target_height_px), Image.Resampling.LANCZOS)

            # Save with DPI metadata for proper printing
            output_filename = os.path.join(output_dir, f"card_{card_num:02d}.png")
            card_resized.save(output_filename, dpi=(dpi, dpi))

            print(f"Saved: {output_filename} (row {row}, col {col})")
            card_num += 1

    print(f"\nSuccessfully split {total_cards} cards into {output_dir}/")

if __name__ == "__main__":
    main()
