from newspaper import Article
from textblob import TextBlob
import paralleldots
from collections import Counter

# Parallel Dots API Config
paralleldots.set_api_key( "YOUR API KEY" )


url ='http://www.technovelgy.com/ct/Technology-Article.asp?ArtNum=20'
article = Article(url)
article.download()
article.parse()
text = article.text

desired_list=['rfid','payment','pos','frequency','identification','attack','security','debit','credit','contact']
keywords=[]
all_keywords=[]

blob = TextBlob(text)

# print(blob.noun_phrases)
for sentence in blob.sentences:
    # print(sentence)
    line =TextBlob(str(sentence))
    for tag in line.noun_phrases:
        all_keywords.append(str(tag))

# Delete strings from a list which do not contain certain words
keywords= [x for x in all_keywords if any(word in x for word in desired_list)]

#
#
# # Sort List Based on Occurances
# keywords.sort(key=Counter(keywords).get, reverse=True)

# Remove Repeatitions
keywords=list(set(keywords))

print(keywords)


