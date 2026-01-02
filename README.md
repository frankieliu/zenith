# Zenith Card Processor

A configurable Python pipeline for processing card sprite sheets into printable PDFs with cutting lines.

## Features

- **Flexible sprite sheet layouts**: Supports any m×n grid configuration
- **Customizable collages**: Create multiple collages with configurable card assignments
- **Automatic centering**: PDFs automatically center collages with calculated margins
- **Multiple page sizes**: Supports letter, legal, A4, or custom page dimensions
- **Print-ready output**: Includes optional cutting lines for easy card separation

## Requirements

- Python 3.9 or higher
- pip or uv for package management

## Installation

### Using uv (recommended)

```bash
uv sync
```

### Using pip

```bash
pip install -e .
```

## Project Structure

```
zenith/
├── config.yaml              # Configuration file (customize this!)
├── pyproject.toml          # Project dependencies
├── img/                    # Input directory
│   └── cards.png           # Your card sprite sheet
├── src/                    # Python scripts
│   ├── 01_split_cards.py      # Step 1: Split sprite sheet into individual cards
│   ├── 02_create_collages.py  # Step 2: Create collages from cards
│   ├── 03_create_pdfs.py      # Step 3: Create PDFs with cutting lines
│   └── 04_combine_pdfs.py     # Step 4: Combine all PDFs into one file
└── output/                 # Generated output
    ├── individual_cards/   # Individual card images
    ├── collages/          # Collage images
    └── pdfs/              # PDF files
```

## Quick Start

### 1. Prepare Your Sprite Sheet

Place your card sprite sheet image at `img/cards.png` (or update the path in `config.yaml`).

### 2. Configure the Pipeline

Edit `config.yaml` to match your sprite sheet layout:

```yaml
sprite_sheet:
  rows: 9           # Number of rows in your sprite sheet
  cols: 12          # Number of columns in your sprite sheet
  total_cards: 108  # Total cards (must equal rows × cols)

card:
  width_inches: 2.5   # Target card width for printing
  height_inches: 3.5  # Target card height for printing
  dpi: 300           # Print resolution

collage:
  grid_rows: 3        # Rows per collage page
  grid_cols: 3        # Columns per collage page
  width_inches: 7.5   # Collage width
  height_inches: 10.5 # Collage height
  assignments:        # Define which cards go in each collage
    - name: "collage_1"
      cards: ["1-9"]  # Cards 1-9 using range notation
    - name: "collage_2"
      cards: ["10-18"]  # Cards 10-18
```

### 3. Run the Pipeline

Run each script in order:

```bash
# Step 1: Split sprite sheet into individual cards
uv run src/01_split_cards.py

# Step 2: Create collages from cards
uv run src/02_create_collages.py

# Step 3: Create PDFs with cutting lines
uv run src/03_create_pdfs.py

# Step 4: Combine all PDFs into one file
uv run src/04_combine_pdfs.py
```

Or run all steps at once:

```bash
uv run src/01_split_cards.py && \
uv run src/02_create_collages.py && \
uv run src/03_create_pdfs.py && \
uv run src/04_combine_pdfs.py
```

## Configuration Guide

### Sprite Sheet Configuration

The sprite sheet is your input image containing all cards in a grid layout.

```yaml
sprite_sheet:
  rows: 9          # Number of card rows in the sprite sheet
  cols: 12         # Number of card columns in the sprite sheet
  total_cards: 108 # Total cards (validation: must equal rows × cols)
```

**Example layouts:**
- 1 row × 28 columns = 28 cards (single horizontal strip)
- 4 rows × 7 columns = 28 cards (2D grid)
- 9 rows × 12 columns = 108 cards (larger grid)

### Card Dimensions

Define the target size for printed cards:

```yaml
card:
  width_inches: 2.5   # Standard poker card width
  height_inches: 3.5  # Standard poker card height
  dpi: 300           # 300 DPI for high-quality printing
```

### Collage Configuration

Collages group multiple cards onto a single page:

```yaml
collage:
  grid_rows: 3        # 3 rows of cards per collage
  grid_cols: 3        # 3 columns of cards per collage
  width_inches: 7.5   # Collage width (3 × 2.5")
  height_inches: 10.5 # Collage height (3 × 3.5")
```

**Card assignments** specify which cards appear in each collage:

```yaml
assignments:
  - name: "collage_1"
    cards: ["1-9"]  # Range notation: expands to [1,2,3,4,5,6,7,8,9]
  - name: "collage_2"
    cards: ["10-18"]  # Cards 10-18 (9 cards)
  - name: "collage_3"
    cards: [1, "2-5", 6, "7-9"]  # Mix integers and ranges
```

**Range notation**: Use `"start-end"` (inclusive) for contiguous card sequences:
- `"1-9"` expands to `[1, 2, 3, 4, 5, 6, 7, 8, 9]`
- `"10-18"` expands to `[10, 11, 12, 13, 14, 15, 16, 17, 18]`
- You can mix individual numbers and ranges: `[1, "2-5", 6]` → `[1, 2, 3, 4, 5, 6]`

Each collage must have exactly `grid_rows × grid_cols` cards.

### PDF Configuration

Configure the output PDF pages:

```yaml
pdf:
  page_size: "letter"  # Options: "letter", "legal", "a4", or [width, height]
  cutting_lines:
    enabled: true      # Draw cutting lines between cards
    color: [0, 0, 0]  # RGB values (0-1), [0,0,0] = black
    width: 0.5        # Line width in points
```

**Page sizes:**
- `letter`: 8.5" × 11" (US standard)
- `legal`: 8.5" × 14" (US legal)
- `a4`: 8.27" × 11.69" (ISO standard)
- Custom: `[8.5, 11]` (width, height in inches)

**Margins are automatically calculated** to center the collage on the page.

## Output Files

After running the pipeline, you'll find:

### Individual Cards
`output/individual_cards/card_01.png` through `card_108.png`
- Each card as a separate PNG file
- Sized to your configured dimensions (e.g., 750×1050 pixels at 300 DPI)

### Collages
`output/collages/collage_1.png`, `collage_2.png`, etc.
- Grid arrangements of cards (e.g., 3×3 = 9 cards per page)
- Sized to your configured collage dimensions (e.g., 2250×3150 pixels)

### PDFs
`output/pdfs/collage_1.pdf`, `collage_2.pdf`, etc.
- Individual PDF files for each collage
- Includes cutting lines (if enabled)
- Centered on letter-sized pages with auto-calculated margins

### Combined PDF
`output/pdfs/all_collages.pdf`
- All collages merged into a single multi-page PDF
- Ready to send to a printer

## Advanced Usage

### Custom Page Sizes

Use a custom page size for specialty printing:

```yaml
pdf:
  page_size: [11, 17]  # 11" × 17" tabloid size
```

### Disable Cutting Lines

For a cleaner look without cutting guides:

```yaml
pdf:
  cutting_lines:
    enabled: false
```

### Different Card Sizes

For business cards (3.5" × 2"):

```yaml
card:
  width_inches: 3.5
  height_inches: 2.0
  dpi: 300

collage:
  grid_rows: 3
  grid_cols: 2
  width_inches: 7.0
  height_inches: 6.0
```

## Troubleshooting

### Error: "Grid dimensions don't match total_cards"

Make sure `rows × cols = total_cards` in your sprite sheet configuration:

```yaml
sprite_sheet:
  rows: 9
  cols: 12
  total_cards: 108  # Must be 9 × 12 = 108
```

### Error: "Expected N cards for MxN grid, got K"

Each collage assignment must have exactly `grid_rows × grid_cols` cards:

```yaml
collage:
  grid_rows: 3
  grid_cols: 3  # 3 × 3 = 9 cards required
  assignments:
    - name: "collage_1"
      cards: [1, 2, 3, 4, 5, 6, 7, 8, 9]  # Must have exactly 9 cards
```

### Cards are blurry

Increase the DPI setting:

```yaml
card:
  dpi: 600  # Higher DPI = better quality but larger files
```

### Collage doesn't fit on page

Ensure your collage dimensions fit within the page size with some margin:

```yaml
pdf:
  page_size: "letter"  # 8.5" × 11"

collage:
  width_inches: 7.5   # Leaves 0.5" left + 0.5" right margins
  height_inches: 10.5 # Leaves 0.25" top + 0.25" bottom margins
```

## Example Workflow

Here's a complete example for 108 cards in a 9×12 sprite sheet:

1. **Place sprite sheet**: `img/cards.png` (9 rows × 12 columns)

2. **Configure** (`config.yaml`):
   ```yaml
   sprite_sheet:
     rows: 9
     cols: 12
     total_cards: 108
   ```

3. **Run pipeline**:
   ```bash
   uv run src/01_split_cards.py      # Creates 108 individual cards
   uv run src/02_create_collages.py  # Creates 12 collages (9 cards each)
   uv run src/03_create_pdfs.py      # Creates 12 PDFs with cutting lines
   uv run src/04_combine_pdfs.py     # Creates 1 combined PDF (12 pages)
   ```

4. **Print**: Send `output/pdfs/all_collages.pdf` to your printer

5. **Cut**: Use the cutting lines to separate cards

## License

MIT License - feel free to use and modify for your projects.

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.
