from transformers import AutoTokenizer, AutoModel
import yake
import re

TOKENIZER = "allenai/scibert_scivocab_uncased"
MODEL = 'allenai/scibert_scivocab_uncased'


class SciBERT:
    def __init__(self):
        print("Loading SciBERT model")
        self.tokenizer = AutoTokenizer.from_pretrained(TOKENIZER)
        self.model = AutoModel.from_pretrained(MODEL)

    def vectorize(self, text):
        kw_extractor = yake.KeywordExtractor()
        keywords = kw_extractor.extract_keywords(text)
        text = re.sub('[^a-zA-Z]', '', str(keywords))
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        outputs = outputs[0].mean(dim=0).mean(dim=0)
        return outputs.detach().numpy()
