def extract_text_from_pdf(reader):
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

