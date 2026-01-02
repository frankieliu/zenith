#!/usr/bin/env python3
"""
Script to create PDFs with collages and cutting lines on letter-sized pages
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, legal, A4
from reportlab.lib.units import inch
import os
import yaml

# Map of standard page size names to dimensions
PAGE_SIZES = {
    'letter': letter,
    'legal': legal,
    'a4': A4,
}

def load_config(config_path="config.yaml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_page_dimensions(page_size_config):
    """
    Get page dimensions from configuration.

    Args:
        page_size_config: Either a string name (e.g., 'letter') or [width, height] in inches

    Returns:
        Tuple of (width, height) in points (ReportLab units)
    """
    if isinstance(page_size_config, str):
        page_size_name = page_size_config.lower()
        if page_size_name in PAGE_SIZES:
            return PAGE_SIZES[page_size_name]
        else:
            raise ValueError(f"Unknown page size: {page_size_config}. Use 'letter', 'legal', 'a4', or specify [width, height] in inches")
    else:
        # Custom size as [width, height] in inches
        return (page_size_config[0] * inch, page_size_config[1] * inch)

def calculate_margins(page_width, page_height, collage_width, collage_height):
    """
    Calculate margins to center collage on page.

    Args:
        page_width: Page width in points
        page_height: Page height in points
        collage_width: Collage width in points
        collage_height: Collage height in points

    Returns:
        Tuple of (left_margin, right_margin, top_margin, bottom_margin) in points
    """
    # Calculate equal margins on left/right
    horizontal_margin_total = page_width - collage_width
    left_margin = horizontal_margin_total / 2
    right_margin = horizontal_margin_total / 2

    # Calculate equal margins on top/bottom
    vertical_margin_total = page_height - collage_height
    top_margin = vertical_margin_total / 2
    bottom_margin = vertical_margin_total / 2

    return left_margin, right_margin, top_margin, bottom_margin

def create_pdf_with_cutting_lines(collage_name, collage_image_path, output_filename,
                                  page_width, page_height, left_margin, bottom_margin,
                                  collage_width, collage_height, grid_rows, grid_cols,
                                  cutting_lines_enabled, line_color, line_width):
    """
    Create a PDF with the collage and cutting lines.

    Args:
        collage_name: Name of the collage (for logging)
        collage_image_path: Path to the collage image file
        output_filename: Output PDF filename
        page_width: PDF page width
        page_height: PDF page height
        left_margin: Left margin in inches
        bottom_margin: Bottom margin in inches
        collage_width: Collage width in inches
        collage_height: Collage height in inches
        grid_rows: Number of rows in grid
        grid_cols: Number of columns in grid
        cutting_lines_enabled: Whether to draw cutting lines
        line_color: RGB color tuple for cutting lines
        line_width: Line width in points
    """
    # Create canvas
    c = canvas.Canvas(output_filename, pagesize=(page_width, page_height))

    # Calculate position (bottom-left corner of image in PDF coordinates)
    x = left_margin
    y = bottom_margin

    # Draw the collage image
    c.drawImage(collage_image_path, x, y, width=collage_width, height=collage_height)

    if cutting_lines_enabled:
        # Calculate card dimensions
        card_width = collage_width / grid_cols
        card_height = collage_height / grid_rows

        # Set line style for cutting lines
        c.setStrokeColorRGB(*line_color)
        c.setLineWidth(line_width)

        # Draw vertical cutting lines
        for i in range(grid_cols + 1):
            line_x = left_margin + (i * card_width)
            c.line(line_x, 0, line_x, page_height)
            print(f"  Vertical line {i+1} at x={line_x/inch:.2f} inches")

        # Draw horizontal cutting lines
        for i in range(grid_rows + 1):
            line_y = bottom_margin + (i * card_height)
            c.line(0, line_y, page_width, line_y)
            print(f"  Horizontal line {i+1} at y={line_y/inch:.2f} inches")

    # Save the PDF
    c.save()
    print(f"Saved: {output_filename}\n")

def main():
    # Load configuration
    config = load_config()

    # Extract configuration values
    collages_dir = config['paths']['output_collages']
    output_dir = config['paths']['output_pdfs']

    # Get page size
    page_size_config = config['pdf'].get('page_size', 'letter')
    page_width, page_height = get_page_dimensions(page_size_config)

    # Collage dimensions
    collage_width_inches = config['collage']['width_inches']
    collage_height_inches = config['collage']['height_inches']
    collage_width = collage_width_inches * inch
    collage_height = collage_height_inches * inch

    # Calculate margins automatically to center collage
    left_margin, right_margin, top_margin, bottom_margin = calculate_margins(
        page_width, page_height, collage_width, collage_height
    )

    # Grid configuration
    grid_rows = config['collage']['grid_rows']
    grid_cols = config['collage']['grid_cols']

    # Cutting lines configuration
    cutting_lines = config['pdf']['cutting_lines']
    cutting_lines_enabled = cutting_lines['enabled']
    line_color = tuple(cutting_lines['color'])
    line_width = cutting_lines['width']

    # Card size
    card_width = collage_width / grid_cols
    card_height = collage_height / grid_rows

    # Collage assignments
    assignments = config['collage']['assignments']

    # Display configuration
    page_size_display = page_size_config if isinstance(page_size_config, str) else f"custom {page_size_config[0]}x{page_size_config[1]}"
    print(f"Creating PDFs on {page_size_display} pages ({page_width/inch:.2f}x{page_height/inch:.2f} inches)")
    print(f"Collage size: {collage_width_inches}x{collage_height_inches} inches")
    print(f"Calculated margins: L={left_margin/inch:.2f}\", R={right_margin/inch:.2f}\", T={top_margin/inch:.2f}\", B={bottom_margin/inch:.2f}\"")
    print(f"Grid: {grid_rows}x{grid_cols}, Card size: {card_width/inch:.2f}x{card_height/inch:.2f} inches\n")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Create PDFs for all collages defined in config
    for assignment in assignments:
        collage_name = assignment['name']
        print(f"Creating PDF for {collage_name}")

        collage_image_path = os.path.join(collages_dir, f"{collage_name}.png")
        output_file = os.path.join(output_dir, f"{collage_name}.pdf")

        create_pdf_with_cutting_lines(
            collage_name, collage_image_path, output_file,
            page_width, page_height, left_margin, bottom_margin,
            collage_width, collage_height, grid_rows, grid_cols,
            cutting_lines_enabled, line_color, line_width
        )

    print(f"Successfully created {len(assignments)} PDFs in {output_dir}/")

if __name__ == "__main__":
    main()
