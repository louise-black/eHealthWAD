import urllib
from bs4 import BeautifulSoup
from textblob import TextBlob
from textstat.textstat import textstat

def process(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    blob = TextBlob(text)
    sent = blob.sentiment
    subj = 100 - int((sent.subjectivity)*100)                     #the less subjective, the better
    polar = 100 - int((sent.polarity)*100)                        #the less polar, the better
    readability = int(textstat.flesch_reading_ease(text))

    return subj, polar, readability
