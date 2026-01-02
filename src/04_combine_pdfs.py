#!/usr/bin/env python3
"""
Script to combine individual PDFs into one multi-page PDF
"""

from pypdf import PdfWriter, PdfReader
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
    pdf_dir = config['paths']['output_pdfs']
    output_file = config['paths']['combined_pdf']
    assignments = config['collage']['assignments']

    # Create PDF writer
    writer = PdfWriter()

    print(f"Combining {len(assignments)} PDFs into single file...")

    # Add each PDF in order from the config
    for assignment in assignments:
        collage_name = assignment['name']
        pdf_file = os.path.join(pdf_dir, f"{collage_name}.pdf")
        print(f"  Adding {pdf_file}")

        # Read the PDF and add its pages
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            writer.add_page(page)

    # Write out the merged PDF
    with open(output_file, "wb") as output:
        writer.write(output)

    print(f"\nSuccessfully created: {output_file}")
    print(f"Contains {len(assignments)} pages ({', '.join([a['name'] for a in assignments])})")

if __name__ == "__main__":
    main()
