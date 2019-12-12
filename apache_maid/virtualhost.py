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


class VirtualHostElement:

    def __str__(self):
        raise NotImplementedError


class Directive(VirtualHostElement):
    name = ''
    value = None

    """
    Directive constructor
    
    :param str name: The directive name
    :param str value: The directive value
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return "{} {}".format(self.name, self.value)


class Section(VirtualHostElement):
    _section_start = '<{name}{args}>'
    _section_end = '</{name}>'
    _directives = []
    _child_sections = []
    name = ''
    args = ''

    """
    Section constructor
    
    :param str name: The section name
    :param str args: Section args
    """
    def __init__(self, name, args=""):
        self.name = name
        self.args = args

    """
    Add a directive
    
    :param Directive directive:
    """
    def add_directive(self, directive):
        self._directives.append(directive)

    """
    Remove directive
    
    :param str name: The name of directive
    """
    def remove_directive(self, name):
        for i, directive in self._directives:
            if directive.name == name:
                self._directives.pop(i)

    """
    Update directive in this section
    
    :param Directive directive:
    """
    def set_directive(self, directive):
        for i, _directive in self._directives:
            if _directive.name == directive.name:
                self._directives[i] = directive

    """
    Get directive by name
    
    :param str name: The name of directive
    :return Directive:
    """
    def get_directive(self, name):
        for directive in self._directives:
            if directive.name == name:
                return directive

        return None

    """
    Add child section
    
    :param Section section:
    """
    def add_child_section(self, section):
        self._child_sections.append(section)

    """
    Remove child section
    
    :param str name: The section name
    """
    def remove_child_section(self, name):
        for i, section in self._child_sections:
            if section.name == name:
                self._child_sections.pop(i)

    """
    Get child section
    
    :param str name:
    """
    def get_child_section(self, name):
        for section in self._child_sections:
            if section.name == name:
                return section

        return None

    """
    Update section
    
    :param Section section:
    """
    def set_child_section(self, section):
        for i, _section in self._child_sections:
            if _section.name == section.name:
                self._child_sections[i] = section

    def __str__(self):
        section_args = ''
        directives = ''

        if self.args != '':
            section_args = " {}".format(self.args)

        start = self._section_start.format(name=self.name, args=section_args) + "\n"
        end = self._section_end.format(name=self.name) + "\n"

        for directive in self._directives:
            directives += "\t{}\n".format(str(directive))

        section_str = start + directives

        if len(self._child_sections) > 0:
            for child_section in self._child_sections:
                section_str += "\t" + str(child_section)

        section_str += end

        return section_str


class VirtualHostDocument:
    root_section = None

    """
    :param Section root_section:
    """
    def __init__(self, root_section):
        self.root_section = root_section

    def __str__(self):
        return str(self.root_section)


class Reader:

    _file_path = ''

    """
    Reader constructor
    
    :param str path: The virtualhost conf file path
    """
    def __init__(self, path):
        self._file_path = path

    """
    Parse section string and return Section object
    
    :param str line:
    :return Section:
    """
    def _get_section(self, line):
        regex = re.compile('<([A-Za-z])( ?.*)>')
        matches = regex.findall(line)
        section = None

        if len(matches) > 0:
            name = matches[0]
            args = str(matches[1]).lstrip(' ')
            section = Section(name, args)

        return section

    """
    Parse string directive and return a Directive object
    
    :param str line:
    :return Directive:
    """
    def _get_directive(self, line):
        regex = re.compile('([A-Za-z])( ?.*)')
        matches = regex.findall(line)
        directive = None

        if len(matches) > 0:
            name = matches[0]
            value = matches[1]
            directive = Directive(name, value)

        return directive

    """
    Gets the file content
    
    :return list:
    """
    def _get_file_content(self):
        content = []

        if os.path.exists(self._file_path) and os.path.isfile(self._file_path):
            with open(self._file_path, 'r') as file:
                for i, line in enumerate(file):
                    content.append(line)

        return content

    """
    Read the virtualhost conf file and return VirtualHostDocument object
    
    :return VirtualHostDocument:
    """
    def read(self):
        file_lines = self._get_file_content()

        for line in file_lines:
            pass
