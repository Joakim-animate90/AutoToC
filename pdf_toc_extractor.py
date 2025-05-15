import os
import base64
import time
import fitz  # PyMuPDF
import functools
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def timing_decorator(func):
    """Decorator that measures and prints the execution time of any function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds")
        return result
    return wrapper


@timing_decorator
def setup_openai_client():
    """Initialize OpenAI client."""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY in .env file")
    
    return OpenAI(api_key=api_key)


@timing_decorator
def pdf_to_base64_images(pdf_path, max_pages=20):
    """
    Convert first several pages of a PDF to base64-encoded images.
    Limits to max_pages to focus on likely TOC pages and avoid memory issues.
    """
    pdf_document = fitz.open(pdf_path)
    base64_images = []
    
    # Process up to max_pages or fewer if the document is shorter
    pages_to_process = min(max_pages, pdf_document.page_count)
    
    print(f"Converting {pages_to_process} pages to images...")
    
    for page_num in range(pages_to_process):
        page = pdf_document.load_page(page_num)
        
        # Render page to image at higher resolution for better OCR
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        
        # Convert pixmap to bytes (PNG format)
        img_bytes = pix.tobytes("png")
        
        # Convert bytes to base64
        base64_image = base64.b64encode(img_bytes).decode('utf-8')
        base64_images.append(base64_image)
        
        print(f"Processed page {page_num + 1}/{pages_to_process}")
    
    pdf_document.close()
    return base64_images


@timing_decorator
def extract_table_of_contents(pdf_path, output_file="toc/table_of_contents.txt"):
    """
    Extract Table of Contents directly from a PDF file using OpenAI's Vision API.
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Setup OpenAI client
    client = setup_openai_client()
    
    # Convert PDF pages to base64-encoded images
    base64_images = pdf_to_base64_images(pdf_path)
    
    # Create content array for the API request 
    content = [
        {
            "type": "text",
            "text": "Extract the Table of Contents from this PDF document. The TOC follows this specific format:\n\n[Case Number] Juicio nº [Case ID] a instancia de [Plaintiff] contra [Defendant] .................. Página [Page Number]\n\nRequirements:\n1. Extract ONLY what is actually visible in the image\n2. Maintain exact case numbers, party names, and page numbers\n3. Preserve section headers like 'Juzgado de lo Social Número X de Santa Cruz de Tenerife'\n4. Keep dotted leader lines (..........) connecting entries to page numbers\n\nFormat using monospace to preserve the original layout. Include ONLY real content from the images."
        }
    ]
    
    # Add each page image to the request
    for i, base64_image in enumerate(base64_images):
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}",
                "detail": "high"
            }
        })
    
    # Send request to OpenAI
    print("Sending PDF pages to OpenAI for TOC extraction...")
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a specialized legal document analyzer tasked with extracting ONLY the actual Table of Contents from legal and judicial documents. Extract EXACTLY what is visible in the images without fabrication or inference. If you see a Table of Contents with case numbers, lawsuit details, and page numbers, extract it PRECISELY as it appears."
            },
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=20000
    )
    
    # Extract TOC from response
    toc = response.choices[0].message.content
    
    # Post-process the TOC to ensure proper formatting with monospace font
    formatted_toc = "```\n" + toc + "\n```"
    
    # Save the generated TOC to a file
    with open(output_file, 'w') as file:
        file.write(formatted_toc)
    
    print(f"Table of Contents saved to {output_file}")
    return toc


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_toc_extractor.py <path_to_pdf> [output_file]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
        extract_table_of_contents(pdf_path, output_file)
    else:
        extract_table_of_contents(pdf_path)
