from pytesseract import pytesseract
from pytesseract import Output
from PIL import Image
import pandas as pd
import enum

class OS(enum.Enum):
    Mac = 0
    Windows = 1
#C:\Users\aryan\OneDrive\Skrivebord\UsefulPrograms\ImageToText\Tesseract-OCR\tesseract.exe
#Tesseract-OCR\tesseract.exe
class ImageReader:
    def __init__(self, os: OS):
        self.config = "--psm 6"
        self.lang = None
        self.img_path = "TEST.png"
        if os == OS.Windows:
            tesseract_path = r"Tesseract-OCR\tesseract.exe"
            pytesseract.tesseract_cmd = tesseract_path 

    def extract_text(self) -> str:
          img = Image.open(self.img_path)
          d = pytesseract.image_to_data(img, lang=self.lang, config=self.config, output_type=Output.DICT)
          print(d)
          df = pd.DataFrame(d)

          df1 = df[(df.conf!='-1')&(df.text!=' ')&(df.text!='')]
          # sort blocks vertically
          sorted_blocks = df1.groupby('block_num').first().sort_values('top').index.tolist()
          for block in sorted_blocks:
              curr = df1[df1['block_num']==block]
              sel = curr[curr.text.str.len()>3]
              char_w = (sel.width/sel.text.str.len()).mean()
              prev_par, prev_line, prev_left = 0, 0, 0
              text = ''
              for ix, ln in curr.iterrows():
                  # add new line when necessary
                  if prev_par != ln['par_num']:
                      text += '\n'
                      prev_par = ln['par_num']
                      prev_line = ln['line_num']
                      prev_left = 0
                  elif prev_line != ln['line_num']:
                      text += '\n'
                      prev_line = ln['line_num']
                      prev_left = 0

                  added = 0  # num of spaces that should be added
                  if ln['left']/char_w > prev_left + 1:
                      added = int((ln['left'])/char_w) - prev_left
                      text += ' ' * added 
                  text += ln['text'] + ' '
                  prev_left += len(ln['text']) + added + 1
              text += '\n'
              return text