import sys
import re
import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def parse_cv(text):
    sections = {}
    # Define regex patterns for common CV sections
    section_patterns = {
        "Contact": r"^(Contact Information|Contact)$",
        "Summary": r"^(Professional Summary|Summary)$",
        "Experience": r"^(Work Experience|Professional Experience|Employment History|Experience)$",
        "Education": r"^(Education|Academic Background)$",
        "Skills": r"^(Skills|Technical Skills|Areas of Expertise)$",
        "Certifications": r"^(Certifications|Licenses)$",
    }
    
    current_section = "Header"
    sections[current_section] = []
    
    lines = text.splitlines()
    
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        section_found = False
        for section, pattern in section_patterns.items():
            if re.match(pattern, stripped_line, re.IGNORECASE):
                current_section = section
                sections.setdefault(current_section, [])
                section_found = True
                break
        if not section_found:
            sections[current_section].append(stripped_line)
    
    for key in sections:
        sections[key] = "\n".join(sections[key]).strip()
    
    return sections

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 checker.py <cv_file.pdf>")
        sys.exit(1)
    
    cv_filename = sys.argv[1]
    try:
        # Use the PDF extraction function instead of reading as text.
        cv_text = extract_text_from_pdf(cv_filename)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    
    parsed_cv = parse_cv(cv_text)
    
    # Display the parsed CV sections
    for section, content in parsed_cv.items():
        print(f"--- {section} ---")
        print(content)
        print()

if __name__ == "__main__":
    main()
