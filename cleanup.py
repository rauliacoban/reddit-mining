import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('stopwords')
import datetime
import re

infile = "sorted.csv"
outfile = "temp.csv"

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    lemmatizer = WordNetLemmatizer()

    # Tokenize words
    words = word_tokenize(text)

    # Remove stopwords and lemmatize words
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.isalnum() and word.lower() not in stop_words]

    words_split = []
    for word in words:
        words_split.extend(re.split('(\d+)',word))

    return ' '.join(words_split)

def postsFromCSV(filename):
    posts = pd.read_csv(filename)
    return posts

def postsToCSV(posts, filename):
    posts.to_csv(filename, index=False)

def isEnglish(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def separateNumbersAlphabets(str):
    numbers = re.findall(r'[0-9]+', str)
    alphabets = re.findall(r'[a-zA-Z]+', str)
    print(*numbers)
    print(*alphabets)

if __name__ == "__main__":
    
    posts = postsFromCSV(infile)
    print(type(posts))

    start = datetime.datetime.now()

    lemmed = []

    for idx in posts.index:
        if idx % 50000 == 0:
            print(idx / 1000)
        text = posts['title'][idx]
        text = preprocess(text)
        if isEnglish(text):
            lemmed.append(text)
        else:
            lemmed.append('DELETEME')

    stop = datetime.datetime.now()
    print("Took", stop - start, "seconds")

    posts["title"] = lemmed
    
    posts.drop(posts.loc[posts['title'] == 'DELETEME'].index, inplace=True)
    posts.drop(posts.loc[posts['title'] == ''].index, inplace=True)

    print(posts)
    postsToCSV(posts, outfile)
    
    #word = "covid19"

    #print(re.split('(\d+)',word))
