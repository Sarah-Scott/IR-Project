import csv
import re
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
#from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


# Use WordNet's lemmatizer 
def lemmatize(tokens):
    myLemmatizer = WordNetLemmatizer()
    lemTokens = []
    for token, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemTokens.append(myLemmatizer.lemmatize(token,pos)) 
    return lemTokens


# Use regular expressions and NLTK's stop words
# Removes URLs, twitter handles, escaped characters, numbers, symbols, and white space
def cleanup(tokens):
    cleanTokens = []
    stopWords = stopwords.words('english')
    for token in tokens:
      noURLs = re.sub('http\S+', '', token)
      noHandles = re.sub('@\S+', '', noURLs)
      noEscapedChars = re.sub('\\\\.', '', noHandles)
      noNumsOrSymbols = re.sub('[^a-zA-Z]', '', noEscapedChars)
      word = noNumsOrSymbols.lower()
      if re.search('[a-zA-Z]', word):
          if word not in stopWords:
              cleanTokens.append(word)
    return cleanTokens



# Train sentiment analysis model on NLTK's "twitter_samples" corpus

positive_tweets = twitter_samples.tokenized('positive_tweets.json')
negative_tweets = twitter_samples.tokenized('negative_tweets.json')
neutral_tweets = twitter_samples.tokenized('tweets.20150430-223406.json')





print(cleanup(lemmatize(positive_tweets[0])))


file = open("tweets.csv", "r")
tweets = list(csv.reader(file, delimiter=' '))
file.close()

def clean_tweet(tweet):
    noURLs = re.sub('http\S+', ' ', str(tweet))
    noEscapedChars = re.sub('\\\\.', ' ', noURLs)
    onlyLetters = re.sub('[^a-zA-Z]', ' ', noEscapedChars)
    return onlyLetters.split()


tokens = []
for tweet in tweets:
    tokens.append(clean_tweet(tweet))

