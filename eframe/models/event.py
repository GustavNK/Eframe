class Event:
    def __init__(self, summary, start_datetime):
        self.summary = summary
        self.start_datetime = start_datetime

    def __eq__(self, other):
        summary = self.summary == other.summary
        date = self.start_datetime == other.start_datetime
        return (summary or date)
