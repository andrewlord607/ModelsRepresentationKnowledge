from abc import ABC, abstractmethod

from Parser.StaticDicts import Part_of_speech

folder_dict = "Dictionaries/"


class DictionaryEntity(ABC):
    @abstractmethod
    def to_string(self) -> str:
        pass


class Dictionary(ABC):
    @abstractmethod
    def find(self, word) -> DictionaryEntity:
        pass


class BaseEntity(DictionaryEntity):
    def __init__(self, line):
        line = line.lstrip()
        str_parts = line.split()
        self.quaziBase = str_parts[1]
        self.canonic_form = ""
        if str_parts[2] != '_':
            self.canonic_form = str_parts[2]
        self.part_speech = str_parts[3]
        self.type_change = str_parts[4]

    def to_string(self):
        return self.quaziBase + " " + self.canonic_form + " " + Part_of_speech[
            self.part_speech]


class DictEntity(BaseEntity):
    def __init__(self, line):
        super().__init__(line)
        line = line.lstrip()
        str_parts = line.split()
        self.category = str_parts[5]

    def to_string(self):
        return super().to_string() + " " + self.category


class ReadyPartDict(Dictionary):
    def __init__(self) -> None:
        self.dict = {}
        f = open(folder_dict + 'ReadyWords.dct')
        for line in f:
            parts = line.split()
            self.dict[parts[1]] = ReadyPartDict.__ReadyWord(parts[2])
        f.close()

    def find(self, word):
        return self.dict.get(word)

    class __ReadyWord(DictionaryEntity):
        def to_string(self):
            return Part_of_speech[self.word]

        def __init__(self, word):
            self.word = word


class BaseDict(Dictionary):
    def __init__(self, dict_file, flexies, entity_class) -> None:
        f = open(folder_dict + dict_file)
        self.dict = {}
        self.flexies = []
        for line in f:
            parts = line.split()
            entity = entity_class(line)
            if parts[1] in self.dict:
                self.dict[parts[1]].append(entity)
            else:
                self.dict[parts[1]] = [entity]
        f.close()
        self.flexies = flexies

    def find(self, word):
        for flex in self.flexies:
            a = word
            b = "_"
            while len(a) > 1:
                base = self.dict.get(a)
                if base is not None:
                    for entity in base:
                        flexie = flex.find(b, entity.part_speech, entity.type_change)
                        if flexie is not None:
                            return entity
                if b == "_":
                    b = ""
                b = a[-1:] + b
                a = a[0:-1]


class EntitiesDict(BaseDict):
    def __init__(self, flexies) -> None:
        super().__init__('Entities.dct', flexies, DictEntity)


class CharactersDict(BaseDict):
    def __init__(self, flexies) -> None:
        super().__init__('Characters.dct', flexies, BaseEntity)


class PredicatesDict(BaseDict):
    def __init__(self, flexies) -> None:
        super().__init__('Predicates.dct', flexies, BaseEntity)


class GlueWordDict(object):
    def __init__(self) -> None:
        self.dict = {}
        f = open(folder_dict + 'GluedWords.dct')
        for line in f:
            parts = line.split()
            not_glue = ' '.join(str(x) for x in parts[1:])
            self.dict[not_glue] = not_glue.replace(' ', '_')
        f.close()

    def transform(self, input_str):
        for gw in self.dict:
            if gw in input_str:
                input_str = input_str.replace(gw, self.dict[gw])
        return input_str
