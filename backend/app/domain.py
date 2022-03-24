import datetime

from .sentiment_analysis import sentiment_vader, Sentiment
from typing import List, Tuple, Dict
import datetime

SAMPLE_SCRIPT: Dict[int, str] = {
    10: "Hello I am Kristoffer",
    20: "I like turtles",
    21: "I like turtles i th",
    22: "I like turtles as",
    23: "I like turtlesewr",
    24: "I like turtles we",
    25: "I like turtles we",
    26: "I like turtles we",
    27: "I like turtles we",
    28: "I like turtles we",
    29: "I like turtles we",
}

REAL_SCRIPT = {
    3: "Hey guys welcome to the stream",
    11: "Whats up Marcel?",
    14: "Hey, Ruben!",
    22: "Nah, Alex! We're not playing Clash Royal today. We've got some division rivals to finish.",
    36: "Man this guy is so lucky Its crazy",
    51: "How have I not scored yet.",
    55: "This guy is so fucking bad!",
    60: "I swear my mother is better!",
    65: "No fucking way. You're kidding me!",
    70: "If that guy scored there I would've just quit",
    75: "This fucking virgin does not deserve anything man, rattiest player I've ever played against!",
    94: "Get in! Get in!",
    96: "Aight, boys! Let's keep it! Let's keep it clean!",
    107: "Are you fucking kidding me? This guy is so shit",
    115: "Nah he's just giving that away",
    120: "That was pretty lucky! That was pretty lucky!",
    127: "SIIIIIUUU!",
    138: "That was a rough game man! Rough game..."
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
        for end in range(window_size, n, window_size):
            current_timestamp = self.messages[end].timestamp
            if current_timestamp in timeline.keys():
                current_timestamp: datetime.datetime = (
                    current_timestamp + datetime.timedelta(microseconds=1)
                )
                assert current_timestamp not in timeline.keys()
            current_average_sentiment = self._compute_average_sentiment_over_messages(
                self.messages[start:end]
            )
            timeline[current_timestamp] = current_average_sentiment.compound
            start += window_size
        return timeline

    def get_sentence_value(
        self, current_timestamp: datetime, window_size_in_seconds=5
    ) -> float:
        timeline: Dict[datetime, float] = self.get_timeline(window_size=1)
        keys = timeline.keys()
        future_keys = [key for key in keys if key >= current_timestamp]
        print(f"Timestamp: {current_timestamp} ")
        # print(f"keys: {keys}")
        if len(future_keys) > 0:
            print(f"Future keys max:{max(future_keys)} ")
            start_dict_key = min(
                [
                    key
                    for key in keys
                    if key
                       >= current_timestamp - datetime.timedelta(seconds=window_size_in_seconds)
                ]
            )
            end_dict_key = min([key for key in keys if key >= current_timestamp])
            start_value = timeline[start_dict_key]
            end_value = timeline[end_dict_key]
            print(f"DIFF: {end_value - start_value}")
            return end_value - start_value
        else:
            return 0

    def get_sentence_map(
        self, video_start_timestamp: datetime.datetime, message_timestamp: datetime.datetime
    ) -> Dict[str, float]:
        current_time = message_timestamp
        relative_time = current_time - video_start_timestamp
        relative_time_seconds = relative_time.seconds
        closest_key = min(
            REAL_SCRIPT.keys(), key=lambda x: abs(x - (relative_time_seconds - 5))
        )
        print(f"closest_key: {closest_key}")
        sentence: str = REAL_SCRIPT[closest_key]

        sentence_value = self.get_sentence_value(current_timestamp=current_time)
        self.sentence_map.update(sentence=sentence, sentence_value=sentence_value)
        return self.sentence_map.get_sentences()


