import re
from apache_maid.template import Template
import os
from apache_maid import VIRTUALHOST_STRUCT, VIRTUALHOST_VARIABLES, conf
import apache_maid.parser


class VirtualHost:

    document_root = ''
    server_name = ''
    server_alias = []
    port = 80
    file_path = ''
    _enabled_link_path = ''

    def __init__(self, name):
        self.server_name = name

    def add_server_alias(self, alias):
        if alias not in self.server_alias:
            self.server_alias.append(alias)

    def remove_server_alias(self, alias):
        self.server_alias.remove(alias)

    def is_enabled(self):
        sites_enabled_path = conf.get('sites_enabled')
        links = os.scandir(sites_enabled_path)

        for link in links:
            if os.path.islink(link.path):
                link_origin_filename = os.path.basename(os.readlink(link.path))
                file_name = os.path.basename(self.file_path)

                if link_origin_filename == file_name:
                    self._enabled_link_path = os.path.join(sites_enabled_path, link.name)
                    return True

        return False

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

    ssl_crt_path = ''
    ssl_key_path = ''
    port = 443


class VirtualHostReader:

    _sites_available_path = ''
    _template = None

    def __init__(self, sites_available_path):
        self._sites_available_path = sites_available_path
        self._filename_regex = re.compile(r'(ssl_)?([a-zA-Z.\-_]+)_([0-9]*)\.conf')

    def _parse_line(self, line, data):
        for variable in VIRTUALHOST_VARIABLES:
            if variable['type'] == 'list':
                value = apache_maid.parser.RegexListParser(variable['regex'], line).parse()
            elif variable['type'] == 'bool':
                value = apache_maid.parser.RegexBoolParser(variable['regex'], line).parse()
            else:
                value = apache_maid.parser.RegexParser(variable['regex'], line).parse()

                if value:
                    value = value.pop()

            if value:
                data[variable['variable']] = value

    def _get_virtual_host(self):
        content = self._template.get_content()
        virtualhost_data = VIRTUALHOST_STRUCT

        for content_line in content:
            self._parse_line(content_line, virtualhost_data)

        if virtualhost_data['is_ssl']:
            virtualhost = SSLVirtualHost(virtualhost_data['server_name'])
            virtualhost.ssl_crt_path = virtualhost_data['ssl_crt_path']
            virtualhost.ssl_key_path = virtualhost_data['ssl_key_path']
        else:
            virtualhost = VirtualHost(virtualhost_data['server_name'])

        virtualhost.document_root = virtualhost_data['document_root']
        virtualhost.port = virtualhost_data['port']
        virtualhost.server_alias = virtualhost_data['server_alias']
        virtualhost.file_path = self._template.get_full_path()

        return virtualhost

    def read_by_name(self, virtualhost):
        files = os.scandir(path=self._sites_available_path)

        for file in files:
            if file.is_file() and self._filename_regex.match(file.name):
                matches = self._filename_regex.findall(file.name)

                if matches[1] == virtualhost:
                    return self.read(file.name)

    def read(self, virtualhost_file_name):
        self._template = Template(virtualhost_file_name, self._sites_available_path)
        self._template.load()
        return self._get_virtual_host()

    def get_available(self):
        files = os.scandir(path=self._sites_available_path)
        virtualhosts = []

        for file in files:
            if file.is_file():
                virtualhosts.append(self.read(file.name))

        return virtualhosts


class VirtualHostWritter:

    _reader = None
    _sites_available_path = ''

    def __init__(self, sites_available_path):
        self._sites_available_path = sites_available_path
        self._reader = VirtualHostReader(sites_available_path)

    def _write_line(self, template_line):
        pass

    def write(self, virtualhost):
        template = Template(virtualhost.get_server_name(), self._sites_available_path)

        if isinstance(virtualhost, SSLVirtualHost):
            template.load_empty(True)
        else:
            template.load_empty()

        content = template.get_content()

        for i,value in content:
            pass
