class Sentiment:
    def __init__(self, positive):
        self.positive = positive


class Message:
    def __init__(self, username: str, message_text: str, timestamp: int):
        self.username: str = username
        self.message_text: str = message_text
        self.timestamp: int = timestamp
        self.sentiment = None
