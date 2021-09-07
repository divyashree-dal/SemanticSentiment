from pymongo import MongoClient
import csv
from prettytable import PrettyTable

hostname = 'localhost'
port = 27017
print("Connecting to mongo client")
client = MongoClient("mongodb://127.0.0.1:27017")
# Creation of mongodb database
db = client['myMongoTweet']
# Creating a collection
collection = db['twitterCollection']

if __name__ == "__main__":
    try:
        polarities = {}
        with open('AFINN-111.csv', 'r') as f:
            line = csv.reader(f, delimiter='\t')
            for everyLine in line:
                word, polarity = everyLine[0], everyLine[1]
                polarities[word] = polarity

        # Retrieved the cleaned messages from mongoDb
        myResults = list(collection.distinct('text_tweet'))

        # Bag of words created for every tweet message
        count_of_tweets = 0
        list_tweet_polarity_details = []
        pretty_table = PrettyTable()
        pretty_table.field_names = ["Tweet", "Message/tweets", "Match", "Polarity"]
        for everyTweet in myResults:
            bag_words = dict()
            tweet = everyTweet.split(' ')
            for i in tweet:
                if i in bag_words.keys():
                    bag_words[i] += 1
                else:
                    bag_words[i] = 1

            # Polarity assigned for every tweet message
            match_words = []
            sum_polarities_words = 0
            for key in bag_words.keys():
                if key in polarities.keys():
                    match_words.append(key)

            for x in match_words:
                sum_polarities_words += int(polarities[x])

            if sum_polarities_words > 1:
                polarity = "Positive"
            elif sum_polarities_words < -1:
                polarity = "Negative"
            else:
                polarity = "Neutral"

            if len(match_words) > 0:
                count_of_tweets += 1
                pretty_table.add_row([count_of_tweets, everyTweet, ', '.join(match_words), polarity])
        print(pretty_table)

    except Exception as exception:
        print(exception)
