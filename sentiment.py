import csv
import re
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
#from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from random import shuffle
from nltk import classify
from nltk import NaiveBayesClassifier


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


# Use regular expressions to remove
# URLs, twitter handles, escaped characters, numbers, symbols, and white space
# Use NLTK's stop words
def cleanup(tokens):
    cleanTokens = []
    stopWords = stopwords.words('english')
    for token in tokens:
      noURLs = re.sub('http\S+', '', token)
      noHandles = re.sub('@\S+', '', noURLs)
      noEscapedChars = re.sub('\\\\.', '', noHandles)
      noNumsOrSymbols = re.sub('[^a-zA-Z]', '', noEscapedChars)
      word = noNumsOrSymbols.lower()
      if re.search('[a-z]', word):
          if word not in stopWords:
              cleanTokens.append(word)
    return cleanTokens


def makeTokensList(tweets):
    tokensList = []
    for tokens in tweets:
        tokensList.append(cleanup(lemmatize(tokens)))
    return tokensList

def genTokenDict(tokens_list):
  for tokens in tokens_list:
      yield dict([token, True] for token in tokens)

# Train sentiment analysis model on NLTK's "twitter_samples" corpus

def getDataset():
  pos_tweets = twitter_samples.tokenized('positive_tweets.json')
  neg_tweets = twitter_samples.tokenized('negative_tweets.json')

  pos_tokens_list = makeTokensList(pos_tweets)
  neg_tokens_list = makeTokensList(neg_tweets)

  pos_tokens_dict = genTokenDict(pos_tokens_list)
  neg_tokens_dict = genTokenDict(neg_tokens_list)

  pos_dataset = [(tok_dict, "Pos") for tok_dict in pos_tokens_dict]
  neg_dataset = [(tok_dict, "Neg") for tok_dict in neg_tokens_dict]

  dataset = pos_dataset + neg_dataset
  shuffle(dataset)
  return dataset


def trainClassifier(train_data):
  myClassifier = NaiveBayesClassifier.train(train_data)
  print("Training Accuracy:", classify.accuracy(myClassifier, train_data))
  return myClassifier



   
dataset = getDataset()
train_data = dataset[:7000]
test_data = dataset[7000:]
myClassifier = trainClassifier(train_data)
print("Testing Accuracy:", classify.accuracy(myClassifier, test_data))



def analyzeTweets(tweetFilename,sentimentFilename):
   
   file = open(tweetFilename, "r")
   bey_tweets = list(csv.reader(file, delimiter=' '))
   file.close()

   bey_tokens = []
   bey_dates = []
   for t in bey_tweets:
      bey_tokens.append(t[0].split())
      bey_dates.append(t[1])

   bey_tokens_list = makeTokensList(bey_tokens)
   bey_tokens_dict = genTokenDict(bey_tokens_list)
   output_list = [] #format: [[tweet,date,sentiment],...]
   numPos = 0
   numNeg = 0 

   count = 0
   for tok_dict in bey_tokens_dict:
      temp = []
      sentiment = myClassifier.classify(tok_dict)
      temp.append(bey_tokens[count])
      temp.append(bey_dates[count])
      temp.append(sentiment)
    
      if (sentiment == 'Pos'):
        numPos += 1
      else:
        numNeg += 1
    
   output_list.append(temp)
   count += 1

   print("Number of positive tweets:", str(numPos))
   print("Number of negative tweets", str(numNeg))

   with open(sentimentFilename, "w", newline="") as csvfile:
      writer = csv.writer(csvfile, delimiter=' ')
      for x in output_list:
        writer.writerow(x)

