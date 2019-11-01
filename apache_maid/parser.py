import re


class RegexParser:

    _regex = ''
    _string = ''
    _type = ''

    def __init__(self, regex, string, _type):
        self._regex = regex
        self._string = string
        self._type = _type

    def _get_matches(self):
        test = re.compile(self._regex)

        if test.match(self._string):
            return test.findall(self._string)
        else:
            return None

    def parse(self):
        values = []

        for match in self._get_matches():
            if self._type == 'int':
                values.append(int(match))
            else:
                values.append(str(match))

        return values


class RegexListParser(RegexParser):

    def parse(self):
        values = self._get_matches()
        return str(values[0]).split(' ')


class RegexBoolParser(RegexParser):

    def parse(self):
        if self._get_matches():
            return True
        else:
            return False
