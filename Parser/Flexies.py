from Parser.Dictionaries import DictionaryEntity, folder_dict
import re

from Parser.StaticDicts import Part_of_speech, Genders, Cases, Numbers, Times, Persons, Aspect


def extract_types_change(line):
    types = re.match('.*\[(.*)\].*', line).group(1)
    parts = types.split()
    i = 0
    result = []
    for part in parts:
        result.append(part)
        i += 1
    return result


class PartCY(DictionaryEntity):

    def __init__(self, line) -> None:
        line_parts = line.split()
        self.part_speech = line_parts[0]
        self.part_gender = line_parts[1]
        self.part_case = line_parts[2]
        self.part_number = line_parts[3]
        self.types_change = extract_types_change(line)

    def to_string(self):
        return Part_of_speech[self.part_speech] + ", " + Genders[self.part_gender] + ", " + Cases[
            self.part_case] + ", " + Numbers[self.part_number]


class PartKP(DictionaryEntity):

    def __init__(self, line) -> None:
        line_parts = line.split()
        self.part_speech = line_parts[0]
        self.part_gender = line_parts[1]
        self.part_number = line_parts[2]
        self.types_change = []

    def to_string(self):
        return Part_of_speech[self.part_speech] + ", " + Genders[self.part_gender] + ", " + Numbers[
            self.part_number]


class PartDE(DictionaryEntity):

    def __init__(self, line) -> None:
        line_parts = line.split()
        self.part_speech = line_parts[0]
        self.part_time = line_parts[1]
        self.part_aspect = line_parts[2]
        self.types_change = []

    def to_string(self):
        return Part_of_speech[self.part_speech] + ", " + Times[self.part_time] + ", " + Aspect[
            self.part_aspect]


class PartGL(DictionaryEntity):

    def __init__(self, line) -> None:
        line_parts = line.split()
        self.part_speech = line_parts[0]
        self.part_time = line_parts[1]
        self.part_person = line_parts[2]
        self.part_gender = line_parts[3]
        self.part_number = line_parts[4]
        self.part_aspect = line_parts[5]
        self.types_change = []

    def to_string(self):
        return Part_of_speech[self.part_speech] + ", " + Times[self.part_time] + ", " + Persons[
            self.part_person] + ", " + Genders[self.part_gender] + ", " + Numbers[self.part_number] + ", " + Aspect[
                   self.part_aspect]


flexions_by_type = {"СУ": PartCY, "ПП": PartCY, "КП": PartKP, "ДЕ": PartDE, "ГЛ": PartGL}


class Flexion(object):
    def __init__(self) -> None:
        self.parts = []

    def add_line(self, line):
        part_speech = line.split()[0]
        part = flexions_by_type[part_speech](line)
        self.parts.append(part)


class FlexiesDict(object):
    def __init__(self) -> None:
        f = open(folder_dict + 'Flexies.dct', encoding='utf-8')
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
