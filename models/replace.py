class Replace:
    def __init__(self, raw_record):
        self.replace_id = raw_record["replace_id"]
        self.grade = raw_record["grade"]
        self.timestamp = raw_record["timestamp"]
        self.lesson = raw_record["lesson"]
        self.subject = raw_record["subject"]
        self.type = raw_record["type"]
        self.text = raw_record["text"]
