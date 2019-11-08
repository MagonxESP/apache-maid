import re


class RegexParser:

    _regex = ''
    _string = ''

    def __init__(self, regex, string):
        self._regex = regex
        self._string = string

    def _get_matches(self):
        test = re.compile(self._regex)
        return test.findall(self._string)

    def parse(self):
        matches = self._get_matches()
        values = []

        for match in matches:
            if type(match) is str:
                values.append(str(match).strip('\t\n '))
            else:
                values.append(match)

        return values


class RegexListParser(RegexParser):

    def parse(self):
        values = self._get_matches()

        if values:
            return str(values.pop()).split(' ')
        else:
            return []


class RegexBoolParser(RegexParser):

    def parse(self):
        if self._get_matches():
            return True
        else:
            return False
