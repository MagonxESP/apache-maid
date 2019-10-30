import os.path
import re


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

    def get_content(self):
        return self._content


class VirtualHostReader:

    _sites_available_path = ''
    _template = None

    def __init__(self, sites_available_path):
        self._sites_available_path = sites_available_path
        self._filename_regex = re.compile(r'(ssl_)?([a-zA-Z.\-_]+)_([0-9]*)\.conf')

    def _get_virtual_host(self):
        content = self._template.get_content()

        for content_line in content:
            pass  # TODO read virtualhost conf file content

    def read(self, virtualhost):
        files = os.scandir(path=self._sites_available_path)

        for file in files:
            if file.is_file() and self._filename_regex.match(file.name):
                matches = self._filename_regex.findall(file.name)

                if matches[1] == virtualhost:
                    self._template = Template(file.name, self._sites_available_path)
                    self._template.load()



