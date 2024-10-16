import io
import re
import PyPDF2
from html2text import HTML2Text

def parse_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        file_content = uploaded_file.read()
        if file_extension in ['md', 'txt']:
            return file_content.decode('utf-8')
        elif file_extension == 'pdf':
            return pdf_to_markdown(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    else:
        return None

def pdf_to_markdown(pdf_content):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
    markdown_content = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        text = clean_text(text)
        html_content = text_to_html(text)
        markdown_content += html_to_markdown(html_content)
    return markdown_content.strip()

def clean_text(text):
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove page numbers
    text = re.sub(r'\n\d+\n', '\n', text)
    # Normalize line breaks
    text = text.replace('\r', '\n')
    return text.strip()

def text_to_html(text):
    # Convert potential main headers
    text = re.sub(r'^([A-ZА-ЯІЇЄ\s]{10,})$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    # Convert potential subheaders
    text = re.sub(r'^([A-ZА-ЯІЇЄ][a-zа-яіїє]+ [A-ZА-ЯІЇЄ][a-zа-яіїє]+.*:)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    # Convert potential paragraphs
    text = re.sub(r'(.+\n){2,}', r'<p>\g<0></p>', text)
    # Convert potential list items
    text = re.sub(r'^\s*[-•]\s*(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    # Wrap list items in <ul> tags
    text = re.sub(r'(<li>.+</li>\n)+', r'<ul>\g<0></ul>', text)
    # Convert potential quotes
    text = re.sub(r'"([^"]+)"', r'<blockquote>\1</blockquote>', text)
    # Convert potential bold text
    text = re.sub(r'\b([A-ZА-ЯІЇЄ]{2,})\b', r'<strong>\1</strong>', text)
    return f'<div>{text}</div>'

def html_to_markdown(html):
    h = HTML2Text()
    h.body_width = 100
    h.ignore_links = False
    h.ignore_images = True
    h.ignore_emphasis = False
    h.ignore_tables = False
    h.ul_item_mark = '-'
    h.emphasis_mark = '*'
    h.strong_mark = '##'
    h.single_line_break = False
    h.wrap_links = False
    h.wrap_list_items = False
    return h.handle(html)