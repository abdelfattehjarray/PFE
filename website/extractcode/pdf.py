import pdfplumber
import re
import bidi.algorithm

def extract_text_per_line(pdf_path):

  with pdfplumber.open(pdf_path) as pdf:
    all_lines = []
    for page in pdf.pages:
      try:
        # Try with layout argument if available
        lines = page.extract_text(layout=True).splitlines()
      except (KeyError, AttributeError):
        lines = page.extract_text().splitlines()
      processed_lines = [process_text_line(line) for line in lines]
      all_lines.extend(processed_lines)
  return all_lines

def fix_arabic_text(text):

  arabic_pattern = r"[\u0600-\u06FF]+"
  matches = re.findall(arabic_pattern, text)

  for match in matches:
    reversed_word = match[::-1]
    text = text.replace(match, reversed_word)

  return text

def process_text_line(text):
  bidi_text = bidi.algorithm.get_display(text)
  return bidi_text

# Example usage
pdf_path = "C:/Users/jarra/Downloads/Documents/modele.pdf"
lines = extract_text_per_line(pdf_path)

def extract_remaining_text_from_list(lines, word):
   
    remaining_text = ""
    l=""
    empty=True
    for line in lines:  # Iterate through the list of lines
        
        if word in line:
            remaining_text = line.replace(word,'').strip()
            if remaining_text=="":
              empty=False
              
              continue
        if empty==False:
           l=line
           return l
           
    return remaining_text

#rtext=extract_remaining_text_from_list(lines,":العنوان")
