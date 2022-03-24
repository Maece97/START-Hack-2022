from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from domain import Sentiment


# calculate the negative, positive, neutral and compound scores, plus verbal evaluation
def sentiment_vader(sentence: str) -> Sentiment:
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    sentiment_dict = sid_obj.polarity_scores(sentence)
    negative: int = sentiment_dict['neg']
    neutral: int = sentiment_dict['neu']
    positive: int = sentiment_dict['pos']
    compound: int = sentiment_dict['compound']

    return Sentiment(
        positive=positive, negative=negative, neutral=neutral, compound=compound
    )
