"""
All File Reading functions go here
"""
import textract
import PyPDF2


def read_docx(docx_filename: str) -> dict:
    """
    :param docx_filename: The filename (and location) of the .docx document
    :return: Dictionary containing filename and ext content of the .docx file
    """
    text: bytes = textract.process(docx_filename)
    return {"filename": docx_filename, "content": text.decode('utf-8')}


def read_txt(txt_filename: str) -> dict:
    """

    :param txt_filename: The filename (and location) of the txt document
    :return: Dictionary containing filename and ext content of the .txt file
    """
    with open(txt_filename, 'r') as file:
        return {"filename": txt_filename, "content": file.read()}


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
    return {"filename": pdf_filename, "content": content}
