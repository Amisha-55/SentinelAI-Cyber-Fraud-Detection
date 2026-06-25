# Scam detection module
from transformers import pipeline


classifier = pipeline(

    "text-classification",

    model="mrm8488/bert-tiny-finetuned-sms-spam-detection"

)



def detect_scam(text):


    result=classifier(text)


    label=result[0]["label"]

    score=result[0]["score"]


    return label,score
