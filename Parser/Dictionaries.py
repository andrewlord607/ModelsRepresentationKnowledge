from abc import ABC, abstractmethod

folder_dict = "Dictionaries/"


class DictionaryEntity(ABC):
    @abstractmethod
    def to_string(self) -> str:
        pass


class Dictionary(ABC):
    @abstractmethod
    def find(self, word) -> DictionaryEntity:
        pass


Part_of_speech = {
    'СУ': 'Существительное',
    'ПП': 'Полное прилагательное',
    'КП': 'Краткое прилагательное',
    'ДЕ': 'Деепричастие',
    'ГЛ': 'Глагол',
    'НА': 'Наречие',
    'ЧИ': 'Числительное',
    'МЕ': 'Местоимение',
    'СО': 'Союз',
    'ПР': 'Предлог'}

Genders = {
    'МР': 'Мужской род',
    'ЖР': 'Женский род',
    'СР': 'Средний род'}

Cases = {
    'ИП': 'Именительный падеж',
    'РП': 'Родительный падеж',
    'ДП': 'Дательный падеж',
    'ВП': 'Винительный падеж',
    'ТП': 'Творительный падеж',
    'ПП': 'Предложный падеж'}

Numbers = {
    'ЕЧ': 'Единственное число',
    'МЧ': 'Множественное число'}


class Entity(DictionaryEntity):
    part_speech = ""
    type_change = ""
    category = ""

    def __init__(self, line):
        line = line.lstrip()
        str_parts = line.split(" ")
        self.part_speech = str_parts[3]
        self.type_change = str_parts[4]

    def to_string(self):
        return Part_of_speech[self.part_speech]


class Flexion(object):
    def __init__(self) -> None:
        self.parts = []

    def add_line(self, line):
        line = line.lstrip()
        line_parts = line.split(" ")
        part = Flexion.__Part()
        part.part_speech = line_parts[0]
        part.part_gender = line_parts[1]
        part.part_case = line_parts[2]
        part.part_number = line_parts[3]
        i = 5
        while line_parts[i] != "]":
            part.types_change.append(line_parts[i])
            i += 1
        self.parts.append(part)

    class __Part(DictionaryEntity):
        def to_string(self):
            return Part_of_speech[self.part_speech] + " " + Genders[self.part_gender] + " " + Cases[
                self.part_case] + " " + Numbers[self.part_number]

        part_speech = ""
        part_gender = ""
        part_case = ""
        part_number = ""
        types_change = []


class ReadyPartDict(Dictionary):
    def __init__(self) -> None:
        self.dict = {}
        f = open(folder_dict + 'ReadyWords.dct')
        line = f.readline().strip()
        while line:
            parts = line.split(" ")
            self.dict[parts[1]] = ReadyPartDict.__ReadyWord(parts[2])
            line = f.readline().strip()
        f.close()

    def find(self, word):
        return self.dict.get(word)

    class __ReadyWord(DictionaryEntity):
        def to_string(self):
            return Part_of_speech[self.word]

        def __init__(self, word):
            self.word = word


class FlexiesDict(object):
    def __init__(self) -> None:
        f = open(folder_dict + 'Flexies.dct')
        line = f.readline().strip()
        self.dict = {}
        while line:
            parts = line.split(" ")
            flexion = Flexion()
            for i in range(int(parts[2])):
                line = f.readline().strip()
                flexion.add_line(line)
            self.dict[parts[1]] = flexion
            line = f.readline().strip()
        f.close()

    def find(self, flexie, part, type_change) -> []:
        if self.dict.get(flexie) is None:
            return None
        list1 = list(
            filter(lambda x: x.part_speech == part and type_change in x.types_change, self.dict.get(flexie).parts))
        if len(list1) > 0:
            return list1[0]
        else:
            return None


class BaseDict(Dictionary):
    def __init__(self, dict_file, flexies) -> None:
        f = open(folder_dict + dict_file)
        line = f.readline().strip()
        self.dict = {}
        self.flexies = []
        while line:
            parts = line.split(" ")
            entity = Entity(line)
            self.dict[parts[1]] = entity
            line = f.readline().strip()
        f.close()
        self.flexies = flexies

    def find(self, word):
        for flex in self.flexies:
            a = word
            b = "_"
            while len(a) > 1:
                base = self.dict.get(a)
                if base is not None:
                    flexie = flex.find(b, base.part_speech, base.type_change)
                    if flexie is not None:
                        return flexie
                if b == "_":
                    b = ""
                b = a[-1:] + b
                a = a[0:-1]


class EntitiesDict(BaseDict):
    def __init__(self, flexies) -> None:
        super().__init__('Entities.dct', flexies)


class CharactersDict(BaseDict):

    def __init__(self, flexies) -> None:
        super().__init__('Characters.dct', flexies)
