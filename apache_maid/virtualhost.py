import re
from apache_maid.template import Template
import os
from apache_maid import VIRTUALHOST_STRUCT, VIRTUALHOST_VARIABLES
import apache_maid.parser


class VirtualHost:

    _document_root = ''
    _server_name = ''
    _server_alias = []
    _port = 80

    def __init__(self, name):
        self._server_name = name

    def get_server_name(self):
        return self._server_name

    def get_document_root(self):
        return self._document_root

    def get_server_alias(self):
        return self._server_alias

    def set_document_root(self, document_root):
        self._document_root = document_root

    def add_server_alias(self, alias):
        if alias not in self._server_alias:
            self._server_alias.append(alias)

    def remove_server_alias(self, alias):
        self._server_alias.remove(alias)

    def set_server_alias(self, server_alias_list):
        self._server_alias = server_alias_list

    def set_server_name(self, server_name):
        self._server_name = server_name

    def set_port(self, port):
        self._port = port

    def get_port(self):
        return self._port

    def save(self):
        pass

    def enable(self):
        pass

    def disable(self):
        pass

    def remove(self):
        self.disable()
        # TODO remove config file


class SSLVirtualHost(VirtualHost):

    _ssl_crt_path = ''
    _ssl_key_path = ''
    _port = 443

    def get_ssl_crt(self):
        return self._ssl_crt_path

    def set_ssl_crt(self, ssl_crt_path):
        self._ssl_crt_path = ssl_crt_path

    def get_ssl_key(self):
        return self._ssl_key_path

    def set_ssl_key(self, ssl_key_path):
        self._ssl_key_path = ssl_key_path


class VirtualHostReader:

    _sites_available_path = ''
    _template = None

    def __init__(self, sites_available_path):
        self._sites_available_path = sites_available_path
        self._filename_regex = re.compile(r'(ssl_)?([a-zA-Z.\-_]+)_([0-9]*)\.conf')

    def _parse_line(self, line, data):
        for variable in VIRTUALHOST_VARIABLES:
            if variable['type'] == 'list':
                parser = apache_maid.parser.RegexListParser(variable['regex'], line, variable['type'])
            elif variable['type'] == 'bool':
                parser = apache_maid.parser.RegexBoolParser(variable['regex'], line, variable['type'])
            else:
                parser = apache_maid.parser.RegexParser(variable['regex'], line, variable['type'])

            value = parser.parse()

            if value:
                data[variable['variable']] = value

    def _get_virtual_host(self):
        content = self._template.get_content()
        virtualhost_data = VIRTUALHOST_STRUCT

        for content_line in content:
            self._parse_line(content_line, virtualhost_data)

        if virtualhost_data['is_ssl']:
            virtualhost = SSLVirtualHost(virtualhost_data['server_name'])
            virtualhost.set_ssl_crt(virtualhost_data['ssl_crt_path'])
            virtualhost.set_ssl_key(virtualhost_data['ssl_key_path'])
        else:
            virtualhost = VirtualHost(virtualhost_data['server_name'])

        virtualhost.set_document_root(virtualhost_data['document_root'])
        virtualhost.set_port(virtualhost_data['port'])
        virtualhost.set_server_alias(virtualhost_data['server_alias'])

        return virtualhost

    def read(self, virtualhost):
        files = os.scandir(path=self._sites_available_path)

        for file in files:
            if file.is_file() and self._filename_regex.match(file.name):
                matches = self._filename_regex.findall(file.name)

                if matches[1] == virtualhost:
                    self._template = Template(file.name, self._sites_available_path)
                    self._template.load()
                    return self._get_virtual_host()
