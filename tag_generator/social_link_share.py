from newspaper import Article
from textblob import TextBlob
import paralleldots
from collections import Counter
import bitly_api
import csv

API_USER = "o_3kr02js6o"
API_KEY = "R_4218fa246fd84fdd818aadeb2d28728e"

def social_share(url):
    # url = 'https://www.tripwire.com/state-of-security/featured/what-rfid-skimming'
    article = Article(url)
    article.download()
    article.parse()
    text = article.text

    desired_list = ['rfid', 'payment', 'pos', 'frequency', 'identification', 'attack', 'security', 'debit', 'credit',
                    'contact']
    keywords = []
    all_keywords = []

    blob = TextBlob(text)

    # print(blob.noun_phrases)
    for sentence in blob.sentences:
        # print(sentence)
        line = TextBlob(str(sentence))
        for tag in line.noun_phrases:
            all_keywords.append(str(tag))

    # Delete strings from a list which do not contain certain words
    keywords = [x for x in all_keywords if any(word in x for word in desired_list)]

    #
    #
    # # Sort List Based on Occurances
    # keywords.sort(key=Counter(keywords).get, reverse=True)

    # Remove Repeatitions
    keywords = list(set(keywords))

    print(keywords)

b = bitly_api.Connection(API_USER, API_KEY)

#Generated links.csv file
with open('links.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['LongUrl','TinyUrl'])

# Reading sheet.csv file
with open('sheet.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        response = b.shorten(uri = row)

        tiny_url=str(response['url'])
        for u in row:
            social_share(u)
        with open('links.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow([str(row),str(response['url'])])






