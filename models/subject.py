class SingleSubject:
    def __init__(self, raw_subject):
        self.raw_subject = raw_subject
        # self.lang = raw_subject
        self.label = raw_subject["label"]
        self.cases = raw_subject["cases"]
        self.nomn = self.cases["nomn"]
        self.gent = self.cases["gent"]
        self.datv = self.cases["datv"]
        self.accs = self.cases["accs"]
        self.ablt = self.cases["ablt"]
        self.loct = self.cases["loct"]

        self.shorts = raw_subject["shorts"]
        self.emoji = raw_subject["emoji"]

        self.lang_group = raw_subject["lang_group"]
        self.ege_group = raw_subject["ege_group"]