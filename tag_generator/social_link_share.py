from newspaper import Article
from textblob import TextBlob
import tweepy
import pymysql
import config as cfg
from datetime import datetime
import paralleldots
from collections import Counter
import bitly_api
import csv

# Open database connection
db = pymysql.connect(cfg.mysql['host'],cfg.mysql['user'],cfg.mysql['password'], cfg.mysql['db'])

# prepare a cursor object using cursor() method
cursor = db.cursor()


# TwitterAPI Configuration
auth = tweepy.OAuthHandler(cfg.twitter['consumer_key'],cfg.twitter['consumer_secret'])
auth.set_access_token(cfg.twitter['access_token'],cfg.twitter['access_token_secret'])
api = tweepy.API(auth)

def hashtag_generator(hashtags):
    nks = "#"
    for item in hashtags:
        kw = item
        kw = kw.replace(" ", "")
        nks = nks + kw + "#"
    nks = nks[:100]
    new_hashtags = nks.rsplit('#', 1)[0]

    return new_hashtags

def tweet_generator(raw_tweet):
    if len(raw_tweet) > 180:
        trim_tweet = raw_tweet[:180]
        tweet =  trim_tweet.rsplit(' ', 1)[0]
        return tweet
    else:
        return raw_tweet


def tweet_compose(text,hashtags):
    tweet=text+hashtags


    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO " + str(cfg.mysql['db']) + ".tbl_tweets(`tweet`,`hashtags`,`status`,`composed_date`,`posted_date`) \
           VALUES ('%s', '%s', '%s','%s','%s')" % \
          (str(tweet), str(hashtags), "Pending", str(datetime.now()),str(datetime.now()))

    print("Query::",sql)

    try:
        # Execute the SQL command
        cursor.execute(sql)
        trend_id = cursor.lastrowid
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        print("Task Failed.")
        print(sql)


def post_tweet():
    # status = api.update_status(tweet)
    print("Tweet::")
    print("--------")


def social_share(url):
    # url = 'https://www.tripwire.com/state-of-security/featured/what-rfid-skimming'
    article = Article(url)
    article.download()
    article.parse()
    text = article.text
    image_url= article.top_image

    desired_keyword_list = ['rfid', 'payment', 'pos', 'frequency', 'identification', 'attack', 'security', 'debit', 'credit',
                    'contact']

    all_keywords = []

    blob = TextBlob(text)

    # print(blob.noun_phrases)
    first_sentence_label=0
    for sentence in blob.sentences:
        # print(sentence)
        if first_sentence_label == 0:
            first_sentence = str(sentence)
            print("1st Sen::",first_sentence)
            first_sentence_label = 1
        line = TextBlob(str(sentence))
        for tag in line.noun_phrases:
            all_keywords.append(str(tag))

    # Delete strings from a list which do not contain certain words
    keywords = [x for x in all_keywords if any(word in x for word in desired_keyword_list)]
    tweet = tweet_generator(first_sentence)
    print("Keywords>>",keywords)
    print ("xxxxxxxxxxxxxxxxxxxxxxx-----------------xxxxxxxxxxxxxxxxxxxxxxxxx")
    tweet_compose(tweet,hashtag_generator(keywords))


    #
    #
    # # Sort List Based on Occurances
    # keywords.sort(key=Counter(keywords).get, reverse=True)

    # Remove Repeatitions
    keywords = list(set(keywords))

    # print(keywords)
    # print(image_url)
    # print(keywords)
    # print("----------------------")



bitly = bitly_api.Connection(cfg.bitly['API_USER'],cfg.bitly['API_KEY'])

#Generated links.csv file
with open('links.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['LongUrl','TinyUrl'])

# Reading sheet.csv file
with open('sheet.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        response = bitly.shorten(uri = row)

        tiny_url=str(response['url'])
        for u in row:
            social_share(u)
        with open('links.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow([str(row),str(response['url'])])








