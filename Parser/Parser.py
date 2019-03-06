from Parser.Dictionaries import ReadyPartDict, FlexiesDict, EntitiesDict


class Parser(object):
    dicts = [ReadyPartDict(), EntitiesDict([FlexiesDict()])]

    def parse_input(self, input_str):
        input_str = input_str.strip().upper()
        words = input_str.split(" ")
        phrases = []
        for word in words:
            phrases.append(self.parse_word(word))
        return phrases

    def parse_word(self, word):
        for one_dict in self.dicts:
            parse = one_dict.find(word)
            if parse is not None:
                return word + " " + parse.to_string()
        return word + " Неопределенная часть речи"
