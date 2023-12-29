def format_date(date): # formats dates
    return date.strftime('%m/%d/%y')

from datetime import datetime

def format_url(url): # filters urls down to domain name only
    return url.replace('http://','').replace('https://','').replace('www.','').split('/')[0].split('?')[0]

def format_plural(amount, word): # changes words to plural based on amount
    if amount != 1:
        return word + 's'
    
    return word
