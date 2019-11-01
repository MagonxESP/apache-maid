# Virtualhost parseable variables
VIRTUALHOST_VARIABLES = [
    {'regex': r'<VirtualHost .*:(.*)>', 'variable': 'port', 'type': 'int'},
    {'regex': r'ServerName (.*)', 'variable': 'server_name', 'type': 'string'},
    {'regex': r'ServerAlias (.*)', 'variable': 'server_alias', 'type': 'list'},
    {'regex': r'DocumentRoot (.*)', 'variable': 'document_root', 'type': 'string'},
    {'regex': r'SSLEngine on', 'variable': 'is_ssl', 'type': 'bool'},
    {'regex': r'SSLCertificateFile (.*)', 'variable': 'ssl_crt_path', 'type': 'string'},
    {'regex': r'SSLCertificateKeyFile (.*)', 'variable': 'ssl_key_path', 'type': 'string'},
]

# virtualhost data struct
VIRTUALHOST_STRUCT = {
    'document_root': '',
    'server_name': '',
    'server_alias': [],
    'port': 0,
    'is_ssl': False,
    'ssl_crt_path': '',
    'ssl_key_path': ''
}
