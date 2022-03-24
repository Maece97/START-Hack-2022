import datetime

from .sentiment_analysis import sentiment_vader, Sentiment
from typing import List
from datetime import datetime


class Message:
    def __init__(self, username: str, message_text: str, timestamp: int):
        self.username: str = username
        self.message_text: str = message_text
        self.timestamp: datetime = datetime.fromtimestamp(timestamp / 1000)
        self.sentiment: Sentiment = sentiment_vader(message_text)


def is_not_older_than_x_seconds(timestamp: datetime, seconds: int = 30):
    difference: datetime.timedelta = datetime.now() - timestamp
    return difference.seconds < seconds


class ReceivedMessages:
    def __init__(self):
        self.messages: List[Message] = []

    def _get_relevant_messages(self):
        return [message for message in self.messages if is_not_older_than_x_seconds(message.timestamp)]

    def add_message(self, message: Message):
        self.messages += [message]
        relevant_messages: List[Message] = self._get_relevant_messages()
        positive, negative, neutral, compound = (0, 0, 0, 0)
        n = len(relevant_messages)
        for message in relevant_messages:
            positive += message.sentiment.positive
            neutral += message.sentiment.neutral
            negative += message.sentiment.negative
            compound += message.sentiment.compound
        positive /= n
        neutral /= n
        negative /= n
        compound /= n

        return Sentiment(
            positive=positive, negative=negative, neutral=neutral, compound=compound
        )
