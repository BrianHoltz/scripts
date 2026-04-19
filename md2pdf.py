#!/usr/bin/env python3
"""
Convert markdown files to PDF using fpdf2.

Handles basic markdown formatting:
- H1, H2, H3 headings (bold, various sizes)
- Bullet lists with indentation
- Paragraph text with indentation support
- Unicode character normalization for font compatibility

Usage:
    md2pdf.py <input.md> <output.pdf>
    md2pdf.py Minutes.md Minutes.pdf
"""

import sys
import unicodedata
from pathlib import Path
from fpdf import FPDF


def clean_text(text):
    """Remove or replace problematic unicode characters.
    
    Normalizes NFKD (decompose characters) then encodes to ASCII,
    ignoring characters outside ASCII range. This converts smart quotes,
    dashes, etc. to ASCII equivalents for font compatibility.
    """
    nfkd = unicodedata.normalize('NFKD', text)
    return nfkd.encode('ascii', 'ignore').decode('ascii')


def markdown_to_pdf(input_file, output_file):
    """Convert a markdown file to PDF.
    
    Args:
        input_file: Path to markdown file
        output_file: Path to output PDF file
    """
    with open(input_file, 'r') as f:
        content = f.read()

    # Create PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    # Process lines
    lines = content.split('\n')
    for idx, line in enumerate(lines):
        try:
            # Reset x position at start of processing each line
            pdf.set_x(10)
            
            if line.strip() == '':
                pdf.ln(2)
            elif line.startswith('# '):
                text = clean_text(line[2:].strip())
                pdf.set_font("Helvetica", 'B', size=16)
                pdf.multi_cell(0, 8, text)
                pdf.set_font("Helvetica", size=10)
                pdf.ln(1)
            elif line.startswith('## '):
                text = clean_text(line[3:].strip())
                pdf.set_font("Helvetica", 'B', size=13)
                pdf.multi_cell(0, 7, text)
                pdf.set_font("Helvetica", size=10)
                pdf.ln(0.5)
            elif line.startswith('### '):
                text = clean_text(line[4:].strip())
                pdf.set_font("Helvetica", 'B', size=11)
                pdf.multi_cell(0, 6, text)
                pdf.set_font("Helvetica", size=10)
            elif line.startswith('- '):
                # Handle bullet points with proper indentation
                bullet_text = clean_text(line.lstrip('- ').strip())
                # Get indentation level
                indent_count = (len(line) - len(line.lstrip())) // 2
                left_margin = 10 + (indent_count * 4)
                pdf.set_x(left_margin)
                pdf.multi_cell(0, 4, '* ' + bullet_text)
            else:
                if line.strip():
                    # Handle regular paragraph text and indented lines
                    text = clean_text(line.strip())
                    indent_count = (len(line) - len(line.lstrip())) // 2
                    if indent_count > 0:
                        left_margin = 10 + (indent_count * 4)
                        pdf.set_x(left_margin)
                        pdf.multi_cell(0, 4, text)
                    else:
                        pdf.multi_cell(0, 4, text)
            
            # Add page break if we're running out of space
            if pdf.will_page_break(4):
                pdf.add_page()
                
        except Exception as e:
            print(f"Error on line {idx}: {repr(line[:80])}", file=sys.stderr)
            print(f"Error: {e}", file=sys.stderr)
            raise

    pdf.output(output_file)
    print(f"PDF created: {output_file}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.md> <output.pdf>", file=sys.stderr)
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        markdown_to_pdf(str(input_file), str(output_file))
    except Exception as e:
        print(f"Failed to convert: {e}", file=sys.stderr)
        sys.exit(1)
