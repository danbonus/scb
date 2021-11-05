class HomeworkRecord:
    def __init__(self, homework_record):
        self.record = homework_record
        self.homework_id = self.record["homework_id"]
        self.subject = self.record["subject"]
        self.homework = self.record["homework"]
        self.attachments = self.record["attachments"]
        self.gdz = self.record["gdz"]
        self.timestamp = self.record["timestamp"]
        self.sender = self.record["sender"]

        if self.homework_id:
            self.filled = True
        else:
            self.filled = False
