#!/usr/bin/env python3
"""
Extract text from scanned PDF pages using macOS Vision framework.
Usage: python3 ocr_vision.py <input.pdf> <output_dir> [--dpi 150] [--lang en]
Output: Individual page text files + combined all_pages.txt with === p.XX === markers.
"""
import sys, os, argparse
import fitz  # pymupdf
import objc
from Foundation import NSURL
from Quartz import (
    CGImageSourceCreateWithURL,
    CGImageSourceCreateImageAtIndex,
    CGImageGetWidth,
    CGImageGetHeight,
)
import Vision

def pdf_to_images(pdf_path, output_dir, dpi=150):
    """Extract PDF pages as PNG images."""
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    paths = []
    for i, page in enumerate(doc):
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img_path = os.path.join(output_dir, f"page_{i+1:03d}.png")
        pix.save(img_path)
        paths.append(img_path)
        print(f"  Extracted page {i+1}/{len(doc)}")
    doc.close()
    return paths

def ocr_image(image_path, lang="en"):
    """OCR a single image using macOS Vision framework."""
    url = NSURL.fileURLWithPath_(image_path)
    source = CGImageSourceCreateWithURL(url, None)
    if not source:
        return f"[ERROR: Could not load {image_path}]"
    cgimage = CGImageSourceCreateImageAtIndex(source, 0, None)
    if not cgimage:
        return f"[ERROR: Could not create image from {image_path}]"

    request = Vision.VNRecognizeTextRequest.alloc().init()
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    request.setUsesLanguageCorrection_(True)
    lang_map = {"en": "en-US", "ja": "ja-JP", "zh": "zh-Hans"}
    request.setRecognitionLanguages_([lang_map.get(lang, lang)])

    handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(cgimage, None)
    success, error = handler.performRequests_error_([request], None)
    if not success:
        return f"[ERROR: OCR failed - {error}]"

    results = request.results()
    lines = []
    for obs in results:
        candidate = obs.topCandidates_(1)
        if candidate:
            lines.append(candidate[0].string())
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="OCR scanned PDF with macOS Vision")
    parser.add_argument("pdf", help="Input PDF file")
    parser.add_argument("output_dir", help="Output directory for text files")
    parser.add_argument("--dpi", type=int, default=150, help="DPI for image extraction (default: 150)")
    parser.add_argument("--lang", default="en", help="OCR language: en, ja, zh (default: en)")
    parser.add_argument("--start-page", type=int, default=1, help="Book page number of first PDF page")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    img_dir = os.path.join(args.output_dir, "images")

    print(f"[1/3] Extracting images from {args.pdf} at {args.dpi} DPI...")
    images = pdf_to_images(args.pdf, img_dir, args.dpi)
    print(f"  → {len(images)} pages extracted")

    print(f"[2/3] Running OCR ({args.lang})...")
    all_text = []
    for i, img_path in enumerate(images):
        page_num = args.start_page + i
        text = ocr_image(img_path, args.lang)
        # Save individual page
        page_file = os.path.join(args.output_dir, f"p{page_num:03d}.txt")
        with open(page_file, "w") as f:
            f.write(text)
        all_text.append(f"=== p.{page_num} ===\n{text}")
        print(f"  OCR page {page_num} ({i+1}/{len(images)})")

    print("[3/3] Writing combined output...")
    combined = os.path.join(args.output_dir, "all_pages.txt")
    with open(combined, "w") as f:
        f.write("\n\n".join(all_text))
    print(f"  → {combined}")
    print("Done!")

if __name__ == "__main__":
    main()
