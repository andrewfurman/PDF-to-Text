from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

def is_header_or_footer(element, page_height, header_height=50, footer_height=50):
    """Determine if an element is likely a header or footer based on its position."""
    if not isinstance(element, LTTextContainer):
        return False
    
    y0, y1 = element.bbox[1], element.bbox[3]
    if y1 > page_height - header_height or y0 < footer_height:
        return True
    
    return False

def extract_text_from_pdf(pdf_path: str, txt_path_1: str, txt_path_2: str):
    all_text = []

    page_layouts = list(extract_pages(pdf_path))
    total_pages = len(page_layouts)
    midpoint = total_pages // 2

    first_half_text = []
    second_half_text = []

    for i, page_layout in enumerate(page_layouts):
        page_height = page_layout.bbox[3]
        texts = [
            element.get_text()
            for element in page_layout
            if isinstance(element, LTTextContainer)
            and not is_header_or_footer(element, page_height)
        ]

        if i < midpoint:
            first_half_text.extend(texts)
        else:
            second_half_text.extend(texts)

    # Write the filtered text to the specified text files
    with open(txt_path_1, 'w', encoding='utf-8') as txt_file_1:
        txt_file_1.write('\n'.join(first_half_text))

    with open(txt_path_2, 'w', encoding='utf-8') as txt_file_2:
        txt_file_2.write('\n'.join(second_half_text))

if __name__ == "__main__":
    pdf_path = 'facetsapi.pdf'
    txt_path_1 = 'facetsapi_first_half.txt'
    txt_path_2 = 'facetsapi_second_half.txt'
    extract_text_from_pdf(pdf_path, txt_path_1, txt_path_2)