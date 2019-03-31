class Config:
    def __init__(self,
                 tokenizer=None,
                 actives=None,
                 model=None,
                 max_len=None):
        self.tokenizer = tokenizer
        self.actives = actives
        self.model = model
        self.max_len = max_len
