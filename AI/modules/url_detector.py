# URL detection module

import validators


def detect_url(url):


    suspicious=False


    reasons=[]


    if len(url)>40:


        suspicious=True

        reasons.append(

        "Very Long URL"

        )



    if '@' in url:


        suspicious=True

        reasons.append(

        "Contains @ Symbol"

        )



    if '-' in url:


        suspicious=True

        reasons.append(

        "Suspicious Domain"

        )



    if not validators.url(url):


        suspicious=True

        reasons.append(

        "Invalid URL"

        )



    return suspicious,reasons
