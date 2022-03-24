import datetime

from .sentiment_analysis import sentiment_vader, Sentiment
from typing import List, Tuple, Dict
import datetime


SAMPLE_SCRIPT: Dict[int, str] = {
    10: "Hello I am Kristoffer",
    20: "I like turtles",
}


class Message:
    def __init__(self, username: str, message_text: str, timestamp: float):
        self.username: str = username
        self.message_text: str = message_text
        self.timestamp: datetime.datetime = datetime.datetime.fromtimestamp(
            timestamp / 1000
        )
        self.sentiment: Sentiment = sentiment_vader(message_text)


def is_not_older_than_x_seconds(timestamp: datetime.datetime, seconds: int = 30):
    difference: datetime.timedelta = datetime.datetime.now() - timestamp
    return difference.seconds < seconds


class SentenceMap:
    def __init__(self):
        self.sentences: Dict[str, float] = {}

    def clear(self):
        self.sentences = {}

    def update(self, sentence: str, sentence_value: float):
        if sentence in self.sentences.keys():
            self.sentences[sentence] += sentence_value
        else:
            self.sentences[sentence] = sentence_value

    def get_sentences(self):
        return self.sentences

class ReceivedMessages:
    def __init__(self):
        self.messages: List[Message] = []
        self.sentence_map = SentenceMap()

    def clear(self):
        self.messages = []
        self.sentence_map.clear()

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

    def get_timeline(self, window_size: int = 10) -> Dict[datetime.datetime, float]:
        start = 0
        n = len(self.messages)
        timeline: Dict[datetime.datetime, float] = {}
        for end in range(0, n, window_size):
            current_timestamp = self.messages[end].timestamp
            current_average_sentiment = self._compute_average_sentiment_over_messages(
                self.messages[start:end]
            )
            timeline[current_timestamp] = current_average_sentiment.compound
        return timeline

    def get_sentence_value(
        self, timestamp: datetime, window_size_in_seconds=5
    ) -> float:
        timeline: Dict[datetime, float] = self.get_timeline()
        keys = timeline.keys()
        future_keys = [
            key
            for key in keys
            if key >= (timestamp + datetime.timedelta(seconds=window_size_in_seconds))
        ]
        if len(future_keys) > 0:
            start_dict_key = min([key for key in keys if key >= timestamp])
            end_dict_key = min(
                [
                    key
                    for key in keys
                    if key
                    >= (timestamp + datetime.timedelta(seconds=window_size_in_seconds))
                ]
            )
            start_value = timeline[start_dict_key]
            end_value = timeline[end_dict_key]
            return end_value - start_value
        else:
            return 0

    def get_sentence_map(self, video_start_timestamp: datetime.datetime) -> Dict[str, float]:
        current_time = datetime.datetime.now()
        relative_time = current_time - video_start_timestamp
        relative_time_seconds = relative_time.seconds
        closest_key = min(SAMPLE_SCRIPT.keys(), key=lambda x: abs(x - relative_time_seconds))
        sentence: str = SAMPLE_SCRIPT[closest_key]
        self.receive_spoken_sentence(
            timestamp=current_time,
            sentence=sentence,
        )
        return self.sentence_map.get_sentences()

    def receive_spoken_sentence(self, timestamp, sentence):
        sentence_value = self.get_sentence_value(timestamp=timestamp)
        self.sentence_map.update(sentence=sentence, sentence_value=sentence_value)
