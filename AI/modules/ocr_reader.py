# OCR reader module

import easyocr


reader=easyocr.Reader(['en'])



def extract_text(image_path):


    result=reader.readtext(image_path)


    text=""


    for r in result:


        text=text+r[1]+" "



    return text

