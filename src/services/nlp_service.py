from typing import List
#import spacy

class NLPService:
    def __init__(self):
        pass
       # self.nlp = spacy.load("en_core_web_sm")

    def extract_product_names(self, text: str) -> List[str]:
        """
        Извлекает названия продуктов из текста.

        :param text: Введенный пользователем текст
        :return: Список названий продуктов
        """
        #doc = self.nlp(text)
        return ""#[ent.text for ent in doc.ents if ent.label_ == "PRODUCT"]
