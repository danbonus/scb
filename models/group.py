class Group:
    def __init__(self, raw_group):
        self.num = raw_group["num"]
        self.subjects = raw_group["subjects"]
        self.name = raw_group["name"]
