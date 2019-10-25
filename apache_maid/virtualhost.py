

class VirtualHost:
    _document_root = ''
    _server_name = ''
    _server_alias = []
    _port = 80
    _is_ssl = False
    _ssl_crt_path = ''
    _ssl_key_path = ''

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

    def set_server_name(self, server_name):
        self._server_name = server_name

    def set_is_ssl(self, is_ssl):
        self._is_ssl = is_ssl

    def is_ssl(self):
        return self._is_ssl

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
