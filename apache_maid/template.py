import os.path


class Template:

    _name = ''
    _path = ''
    _content = []

    def __init__(self, name, dir_path):
        self._name = name
        self._path = dir_path

    def load(self):
        file_path = self._path + '/' + self._name

        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                for i, line in enumerate(file):
                    self._content.append(line)

    def save(self):
        file_path = self._path + '/' + self._name

        try:
            file = open(file_path, 'w')
            file.writelines(self._content)
        except IOError as e:
            print(e)

    def get_line(self, index):
        content_lenght = len(self._content)

        if content_lenght > 0 and 0 <= index < content_lenght:
            return self._content[index]
        else:
            return ''

    def set_line(self, index, content):
        content_lenght = len(self._content)

        if content_lenght > 0 and 0 <= index < content_lenght:
            self._content[index] = content
