import datetime

from .sentiment_analysis import sentiment_vader, Sentiment
from typing import List, Tuple
from datetime import datetime


class Message:
    def __init__(self, username: str, message_text: str, timestamp: float):
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
        return [
            message
            for message in self.messages
            if is_not_older_than_x_seconds(message.timestamp)
        ]

    def _compute_average_sentiment_over_messages(
        self, messages: List[Message]
    ) -> Sentiment:
        positive, negative, neutral, compound = (0, 0, 0, 0)
        n = len(messages)
        if n > 0:
            for message in messages:
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

    def add_message(self, message: Message) -> Message:
        self.messages.append(message)
        return message

    def get_avg_sentiment(self):
        relevant_messages: List[Message] = self._get_relevant_messages()
        return self._compute_average_sentiment_over_messages(relevant_messages)

    def get_word_map(self):
        pass

    def get_timeline(self, window_size: int = 10) -> List[Tuple[datetime, float]]:
        start = 0
        n = len(self.messages)
        timeline: List[Tuple[datetime, float]] = []
        for end in range(0, n, window_size):
            current_timestamp = self.messages[end].timestamp
            current_average_sentiment = self._compute_average_sentiment_over_messages(
                self.messages[start:end]
            )
            timeline.append((current_timestamp, current_average_sentiment.compound))
        return timeline
