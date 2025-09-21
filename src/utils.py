# src/utils.py
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import io, re, hashlib

def extract_text_from_pdf(path, ocr_threshold_chars=100):
    """
    1) Try pdfplumber for selectable text.
    2) If result is very short (likely scanned), fallback to OCR via pdf2image + pytesseract.
    """
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for p in pdf.pages:
                page_text = p.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PDF extraction error: {e}")
        text = ""

    # If no useful text, use OCR with better preprocessing
    if len(text.strip()) < ocr_threshold_chars:
        try:
            images = convert_from_path(path, dpi=200)  # Higher DPI for better OCR
            for img in images:
                # Enhanced preprocessing for better OCR
                gray = img.convert("L")
                # Resize if too small
                if gray.width < 1000:
                    gray = gray.resize((gray.width * 2, gray.height * 2), Image.Resampling.LANCZOS)
                # Use better OCR configuration
                ocr_text = pytesseract.image_to_string(gray, config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;:!?()[]{}"\' ')
                text += ocr_text + "\n"
        except Exception as e:
            print(f"OCR extraction error: {e}")
    
    return text

def extract_text_from_image_bytes(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    gray = img.convert("L")
    return pytesseract.image_to_string(gray)

def sanitize_text(text):
    """Remove repeated headers/footers (simple heuristics), excessive whitespace."""
    # Remove page numbers like "Page 1 of 5"
    text = re.sub(r"\bPage\s+\d+\b(?:\s+of\s+\d+)?", "", text, flags=re.IGNORECASE)
    # Remove multiple newlines
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()

def text_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

import re

def chunk_text_sentence_aware(text, max_chars=3000, overlap_chars=200):
    # split on sentence boundaries roughly
    sentences = re.split(r'(?<=[\.\?\!])\s+', text)
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) + 1 <= max_chars:
            current += ("" if current=="" else " ") + s
        else:
            if current:
                chunks.append(current)
            # start new chunk with overlap
            if overlap_chars > 0 and chunks:
                overlap = chunks[-1][-overlap_chars:]
                current = (overlap + " " + s).strip()
            else:
                current = s
    if current:
        chunks.append(current)
    return chunks
