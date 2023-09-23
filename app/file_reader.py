"""
All File Reading functions go here
"""
import textract
import PyPDF2
from .openAI import generate_keywords_from_notes
from PIL import Image
import pytesseract
import cv2
from google.cloud import vision_v1

def ocr_with_tesseract(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def ocr_with_google_vision(image_path):
    client = vision_v1.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision_v1.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else ''

if __name__ == "__main__":
    image_path = 'path_to_your_image.png'
    
    # OCR with Tesseract
    tesseract_text = ocr_with_tesseract(image_path)
    print(f'Tesseract OCR Result:\n{tesseract_text}\n')
    
    # OCR with Google Cloud Vision API
    google_vision_text = ocr_with_google_vision(image_path)
    print(f'Google Cloud Vision OCR Result:\n{google_vision_text}\n')

def read_docx(docx_filename: str) -> dict:
    """
    :param docx_filename: The filename (and location) of the .docx document
    :return: Dictionary containing filename and ext content of the .docx file
    """
    text: str = textract.process(docx_filename).decode('utf-8')
    keywords = generate_keywords_from_notes(text)
    return {"filename": docx_filename, "content": text, "keywords": keywords}


def read_txt(txt_filename: str) -> dict:
    """

    :param txt_filename: The filename (and location) of the txt document
    :return: Dictionary containing filename and ext content of the .txt file
    """
    with open(txt_filename, 'r') as file:
        text = file.read()
        keywords = generate_keywords_from_notes(text)
        return {"filename": txt_filename, "content": text, "keywords": keywords}


def read_pdf(pdf_filename: str) -> dict:
    """

    :param pdf_filename: The filename (and location) of the pdf document
    :return: Dictionary containing filename and ext content of the .pdf file
    """
    with open(pdf_filename, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        content = ''
        for page in pdf.pages:
            content += page.extract_text()
    keywords = generate_keywords_from_notes(content)
    return {"filename": pdf_filename, "content": content, "keywords": keywords}
