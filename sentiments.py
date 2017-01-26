import tweet_secrets as secret

from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key=secret.ALCHMY_KEY)


def getSentiment(tweet):
    result = alchemy_language.sentiment(text=tweet)
    if result['status'] == 'OK':
        sentimentsList = []
        for item in result['docSentiment'].items():
            sentimentsList.append(item[0] + ": " + item[1])
        return sentimentsList
