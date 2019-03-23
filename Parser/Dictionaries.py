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
    'СР': 'Средний род',
    'НР': 'Неопределённый род'}

Cases = {
    'ИП': 'Именительный падеж',
    'РП': 'Родительный падеж',
    'ДП': 'Дательный падеж',
    'ВП': 'Винительный падеж',
    'ТП': 'Творительный падеж',
    'ПП': 'Предложный падеж'}

Numbers = {
    'ЕЧ': 'Единственное число',
    'МЧ': 'Множественное число',
    'НЧ': 'Неопределённое число'}

Times = {
    'НВ': 'Настоящее время',
    'ПВ': 'Прошедшее время',
    'ИН': 'Инфинитив'}

Aspect = {
    'СВ': 'Совершенный вид',
    'НВ': 'Несовершенный вид'}

Persons = {
    '1Л': 'Первое лицо',
    '2Л': 'Второе лицо',
    '3Л': 'Третье лицо',
    'НЛ': 'Неопределённое лицо'}


class Entity(DictionaryEntity):
    part_speech = ""
    type_change = ""
    category = ""
    canonic_form = ""  # Окончание в ИП ЕД
    quaziBase = ""  # Квазиоснова(слово без окончания)

    supposed_flexion = None

    def __init__(self, line):
        line = line.lstrip()
        str_parts = line.split()
        self.quaziBase = str_parts[1]
        if str_parts[2] != '_':
            self.canonic_form = str_parts[2]
        self.part_speech = str_parts[3]
        self.type_change = str_parts[4]

    def to_string(self):
        if self.supposed_flexion is None:
            return self.quaziBase + " " + self.canonic_form + " " + Part_of_speech[self.part_speech] + " " + self.category
        else:
            return self.quaziBase + self.canonic_form + ": " + self.supposed_flexion.to_string()


class Flexion(object):
    def __init__(self) -> None:
        self.parts = []

    def add_line(self, line):
        line = line.lstrip()
        line_parts = line.split()
        part = Flexion.__Part()
        # TODO: хотелось бы сделать это покрасивее
        part.part_speech = line_parts[0]
        if part.part_speech == 'СУ' or part.part_speech == 'ПП':
            part.part_gender = line_parts[1]
            part.part_case = line_parts[2]
            part.part_number = line_parts[3]
            i = 5
        elif part.part_speech == 'КП':
            part.part_gender = line_parts[1]
            part.part_number = line_parts[2]
            i = 4
        elif part.part_speech == 'ДЕ':
            part.part_time = line_parts[1]
            part.part_aspect = line_parts[2]
            i = 4
        elif part.part_speech == 'ГЛ':
            part.part_time = line_parts[1]
            part.part_person = line_parts[2]
            part.part_gender = line_parts[3]
            part.part_number = line_parts[4]
            part.part_aspect = line_parts[5]
            i = 7

        while line_parts[i] != "]":
            part.types_change.append(line_parts[i])
            i += 1
        self.parts.append(part)

    class __Part(DictionaryEntity):
        # TODO: хотелось бы сделать это покрасивее, как и в add_line
        def to_string(self):
            if self.part_speech == 'СУ' or self.part_speech == 'ПП':
                return Part_of_speech[self.part_speech] + ", " + Genders[self.part_gender] + ", " + Cases[
                    self.part_case] + ", " + Numbers[self.part_number]
            elif self.part_speech == 'КП':
                return Part_of_speech[self.part_speech] + ", " + Genders[self.part_gender] + ", " + Numbers[
                    self.part_number]
            elif self.part_speech == 'ДЕ':
                return Part_of_speech[self.part_speech] + ", " + Times[self.part_time] + ", " + Aspect[
                    self.part_aspect]
            elif self.part_speech == 'ГЛ':
                return Part_of_speech[self.part_speech] + ", " + Times[self.part_time] + ", " + Persons[
                    self.part_person] + ", " + Genders[self.part_gender] + ", " + Numbers[self.part_number] + ", " + Aspect[
                    self.part_aspect]

        part_speech = ""
        part_gender = ""
        part_case = ""
        part_number = ""
        part_time = ""
        part_aspect = ""
        part_person = ""
        types_change = []


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


class FlexiesDict(object):
    def __init__(self) -> None:
        f = open(folder_dict + 'Flexies.dct')
        line = f.readline().strip()
        self.dict = {}
        while line:
            parts = line.split()
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
        self.dict = {}
        self.flexies = []
        for line in f:
            parts = line.split()
            entity = Entity(line)
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
                            entity.supposed_flexion = flexie
                            return entity
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


class PredicatesDict(BaseDict):
    def __init__(self, flexies) -> None:
        super().__init__('Predicates.dct', flexies)

class GlueWordDict(object):
    # TODO: Переписать более эффективно?
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



