from Parser.Dictionaries import ReadyPartDict, EntitiesDict, GlueWordDict, PredicatesDict, CharactersDict
from Parser.Flexies import FlexiesDict


class Parser(object):
    flexies = [FlexiesDict()]
    dicts = [ReadyPartDict(), EntitiesDict(flexies), CharactersDict(flexies),  PredicatesDict(flexies)]
    gw = GlueWordDict()

    def parse_input(self, input_str):
        input_str = input_str.strip().upper()
        input_str = self.gw.transform(input_str)
        words = input_str.split()
        phrases = []
        for word in words:
            phrases.append(self.parse_word(word))
        return '\n'.join(str(x) for x in phrases)

    def parse_word(self, word):
        for one_dict in self.dicts:
            parse = one_dict.find(word)
            if parse is not None:
                return word + " - " + parse.to_string()
        return word + " Неопределенная часть речи"
