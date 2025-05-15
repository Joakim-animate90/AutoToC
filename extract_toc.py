#!/usr/bin/env python3
"""
Simple command-line tool to extract a Table of Contents from any PDF file.
"""

import os
import sys
from pdf_toc_extractor import extract_table_of_contents

def main():
    # Display banner
    print("=" * 80)
    print(" PDF Table of Contents Extractor ".center(80, "="))
    print("=" * 80)
    
    # Get PDF path from command line or prompt user
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = input("Enter path to PDF file: ").strip()
    
    # Validate file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return
    
    # Get output path or use default
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        # Create default output path based on input filename
        basename = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = f"toc/{basename}_toc.txt"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Extracting Table of Contents from: {pdf_path}")
    print(f"Output will be saved to: {output_path}")
    
    try:
        # Extract TOC
        toc = extract_table_of_contents(pdf_path, output_path)
        
        # Display success message
        print("\nExtraction Complete!")
        print(f"Table of Contents saved to: {output_path}")
        
        # Show preview of TOC
        print("\nPreview of extracted Table of Contents:")
        print("-" * 80)
        # Show first few lines (up to 10) of the TOC
        lines = toc.split("\n")
        for line in lines[:min(10, len(lines))]:
            print(line)
        
        if len(lines) > 10:
            print("...")
            print(f"[{len(lines)-10} more lines not shown]")
        
        print("-" * 80)
        
    except Exception as e:
        print(f"Error extracting Table of Contents: {e}")

if __name__ == "__main__":
    main()
