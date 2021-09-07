from pymongo import MongoClient
import math
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
    # Retrieved the cleaned messages from mongoDb
    myResults = list(collection.distinct('text_tweet'))
    totalTweets = len(myResults)

    tweets_containing_flu = []
    tweets_containing_snow = []
    tweets_containing_cold = []

    # Append each search term tweets to different lists
    for everyTweet in myResults:
        if 'flu' in everyTweet:
            tweets_containing_flu.append(everyTweet)
        if 'snow' in everyTweet:
            tweets_containing_snow.append(everyTweet)
        if 'cold' in everyTweet:
            tweets_containing_cold.append(everyTweet)

    # To calculate the the length, log value for flu, snow, and cold
    totalByLengthOfFlu = int(len(myResults) / len(tweets_containing_flu))
    logToBase10Flu = math.floor(math.log10(totalByLengthOfFlu))

    totalByLengthOfSnow = int(len(myResults) / len(tweets_containing_snow))
    logToBase10Snow = math.floor(math.log10(totalByLengthOfSnow))

    totalByLengthOfCold = int(len(myResults) / len(tweets_containing_cold))
    logToBase10Cold = math.ceil(math.log10(totalByLengthOfCold))

    # To print the table containing total count of tweets / documents
    pretty_document_table = PrettyTable()
    pretty_document_table.field_names = ['Total Documents']
    pretty_document_table.add_row([len(myResults)])
    print(pretty_document_table)

    # To print the above calculated details in a table format
    pretty_tf_idf_table = PrettyTable()
    pretty_tf_idf_table.field_names = ["Search Query", "Document containing the term (df)",
                                       "Total Documents(N)/ number of documents term appeared (df)",
                                       "Log10(N/df)"]

    pretty_tf_idf_table.add_row(['flu', len(tweets_containing_flu), totalByLengthOfFlu, logToBase10Flu])
    pretty_tf_idf_table.add_row(['snow', len(tweets_containing_snow), totalByLengthOfSnow, logToBase10Snow])
    pretty_tf_idf_table.add_row(['cold', len(tweets_containing_cold), totalByLengthOfCold, logToBase10Cold])

    print(pretty_tf_idf_table)

    print()
    print("---------------||||||------------------------------SNOW"
          "--------------------------------------------|||||-----")

    # To perform frequency count of word 'snow' per document/tweet
    pretty_term_snow_table = PrettyTable()
    pretty_term_snow_table.field_names = (['Term'])
    pretty_term_snow_table.add_row(['snow'])
    print(pretty_term_snow_table)

    length_snow = len(tweets_containing_snow)
    article_number = 0
    pretty_frequency_snow_count_table = PrettyTable()
    pretty_frequency_snow_count_table.field_names = ["Snow appeared in " + str(length_snow) + " documents",
                                                     "Total Words (m)",
                                                     "Frequency (f)"]
    highest_relative_frequency_snow_list = []
    dictionary_snow_frequencies = dict()
    for tweet in tweets_containing_snow:
        article_number += 1
        list_tweets = tweet.split(' ')
        list_tweets = [item.lower() for item in list_tweets]
        pretty_frequency_snow_count_table.add_row(
            ["Article #" + str(article_number), len(list_tweets), list_tweets.count('snow')])

        # To calculate the highest relative frequency for word snow
        calculated_relative_frequency_value = list_tweets.count('snow') / len(list_tweets)
        highest_relative_frequency_snow_list.append(calculated_relative_frequency_value)

        dictionary_snow_frequencies[tweet] = calculated_relative_frequency_value

    snow_key_maximum_value = max(dictionary_snow_frequencies, key=dictionary_snow_frequencies.get)

    print(pretty_frequency_snow_count_table)

    print("Highest relative frequency for word 'snow' is = {} and the tweet is = {}".format
          (max(highest_relative_frequency_snow_list), snow_key_maximum_value))

    print()
    print("---------------||||||------------------------------COLD"
          "--------------------------------------------|||||-----")

    # To perform frequency count of word 'cold' per document/tweet
    pretty_term_cold_table = PrettyTable()
    pretty_term_cold_table.field_names = (['Term'])
    pretty_term_cold_table.add_row(['cold'])
    print(pretty_term_cold_table)

    length_cold = len(tweets_containing_cold)
    article_number = 0
    pretty_frequency_cold_count_table = PrettyTable()
    pretty_frequency_cold_count_table.field_names = ["cold appeared in " + str(length_cold) + " documents",
                                                     "Total Words (m)",
                                                     "Frequency (f)"]
    highest_relative_frequency_cold_list = []
    dictionary_cold_frequencies = dict()
    for tweet in tweets_containing_cold:
        article_number += 1
        list_tweets = tweet.split(' ')
        list_tweets = [item.lower() for item in list_tweets]
        pretty_frequency_cold_count_table.add_row(
            ["Article #" + str(article_number), len(list_tweets), list_tweets.count('cold')])

        # To calculate the highest relative frequency for word cold
        calculated_relative_frequency_value = list_tweets.count('cold') / len(list_tweets)
        highest_relative_frequency_cold_list.append(calculated_relative_frequency_value)

        dictionary_cold_frequencies[tweet] = calculated_relative_frequency_value

    cold_key_maximum_value = max(dictionary_cold_frequencies, key=dictionary_cold_frequencies.get)

    print(pretty_frequency_cold_count_table)

    print("Highest relative frequency for word 'cold' is = {} and the tweet is = {}".format(
        max(highest_relative_frequency_cold_list), cold_key_maximum_value))
