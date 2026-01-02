#!/usr/bin/env python3
"""
Script to create collages of cards with configurable grid layout
"""

from PIL import Image
import os
import yaml

def load_config(config_path="config.yaml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def parse_card_list(card_spec):
    """
    Parse card specification that can include ranges.

    Args:
        card_spec: List that can contain integers and/or range strings like "10-18"

    Returns:
        List of integers

    Examples:
        [1, 2, 3] -> [1, 2, 3]
        ["1-5"] -> [1, 2, 3, 4, 5]
        [1, "2-5", 6, "7-9"] -> [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    result = []

    for item in card_spec:
        if isinstance(item, int):
            # Single card number
            result.append(item)
        elif isinstance(item, str):
            # Range specification like "10-18"
            if '-' in item:
                parts = item.split('-')
                if len(parts) == 2:
                    try:
                        start = int(parts[0])
                        end = int(parts[1])
                        # Inclusive range
                        result.extend(range(start, end + 1))
                    except ValueError:
                        raise ValueError(f"Invalid range format: {item}. Use 'start-end' like '10-18'")
                else:
                    raise ValueError(f"Invalid range format: {item}. Use 'start-end' like '10-18'")
            else:
                # Try to parse as integer string
                try:
                    result.append(int(item))
                except ValueError:
                    raise ValueError(f"Invalid card specification: {item}. Use integers or ranges like '10-18'")
        else:
            raise ValueError(f"Invalid card specification type: {type(item)}. Use integers or range strings")

    return result

def create_collage(card_numbers, output_filename, input_dir, collage_width_px, collage_height_px,
                   grid_rows, grid_cols, card_width, card_height, dpi):
    """
    Create a collage from the given card numbers.

    Args:
        card_numbers: List of card numbers to include
        output_filename: Output filename for the collage
        input_dir: Directory containing individual card images
        collage_width_px: Collage width in pixels
        collage_height_px: Collage height in pixels
        grid_rows: Number of rows in collage grid
        grid_cols: Number of columns in collage grid
        card_width: Width of each card slot in pixels
        card_height: Height of each card slot in pixels
        dpi: DPI for output image
    """
    # Validate that we have the right number of cards
    expected_cards = grid_rows * grid_cols
    if len(card_numbers) != expected_cards:
        raise ValueError(f"Expected {expected_cards} cards for {grid_rows}x{grid_cols} grid, got {len(card_numbers)}")

    # Create a new blank image
    collage = Image.new('RGB', (collage_width_px, collage_height_px), 'white')

    # Place each card in the grid
    for idx, card_num in enumerate(card_numbers):
        row = idx // grid_cols
        col = idx % grid_cols

        # Load the card image
        card_filename = os.path.join(input_dir, f"card_{card_num:02d}.png")
        card_img = Image.open(card_filename)

        # Calculate position
        x = col * card_width
        y = row * card_height

        # Paste the card into the collage
        collage.paste(card_img, (x, y))

        print(f"  Placed card_{card_num:02d} at position ({col}, {row})")

    # Save the collage with DPI metadata
    collage.save(output_filename, dpi=(dpi, dpi))
    print(f"Saved: {output_filename}\n")

def main():
    # Load configuration
    config = load_config()

    # Extract configuration values
    input_dir = config['paths']['output_individual_cards']
    output_dir = config['paths']['output_collages']

    dpi = config['card']['dpi']

    collage_width_inches = config['collage']['width_inches']
    collage_height_inches = config['collage']['height_inches']
    grid_rows = config['collage']['grid_rows']
    grid_cols = config['collage']['grid_cols']
    assignments = config['collage']['assignments']

    # Convert collage size to pixels
    collage_width_px = int(collage_width_inches * dpi)
    collage_height_px = int(collage_height_inches * dpi)

    # Calculate card slot size
    card_width = collage_width_px // grid_cols
    card_height = collage_height_px // grid_rows

    print(f"Creating collages at {collage_width_inches}x{collage_height_inches} inches ({collage_width_px}x{collage_height_px} pixels)")
    print(f"Grid layout: {grid_rows}x{grid_cols}")
    print(f"Each card slot: {card_width}x{card_height} pixels\n")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Create collages based on assignments
    for assignment in assignments:
        collage_name = assignment['name']
        card_spec = assignment['cards']

        # Parse card specification (handles ranges like "10-18")
        card_numbers = parse_card_list(card_spec)

        print(f"Creating {collage_name}: {len(card_numbers)} cards")
        output_file = os.path.join(output_dir, f"{collage_name}.png")

        create_collage(
            card_numbers, output_file, input_dir,
            collage_width_px, collage_height_px,
            grid_rows, grid_cols,
            card_width, card_height, dpi
        )

    print(f"Successfully created {len(assignments)} collages in {output_dir}/")

if __name__ == "__main__":
    main()
