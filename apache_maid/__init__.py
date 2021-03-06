import apache_maid.settings

# Required configuration
conf = apache_maid.settings.Settings()

if conf.exits() is False:
    conf = apache_maid.settings.configure()

conf.load()

# Virtualhost parseable variables
# By default the virtual host reader parser get the last group value of the regex by default
VIRTUALHOST_VARIABLES = [
    {
        'regex': r'^(?!.*#.*).*<VirtualHost .*:(.*)>',
        'variable': 'port',
        'type': 'int'},
    {
        'regex': r'^(?!.*#.*).*ServerName(.*)',
        'variable': 'server_name',
        'type': 'string'
    },
    {
        'regex': r'^(?!.*#.*).*ServerAlias(.*)',
        'variable': 'server_alias',
        'type': 'list'
    },
    {
        'regex': r'^(?!.*#.*).*DocumentRoot(.*)',
        'variable': 'document_root', 'type': 'string'},
    {
        'regex': r'^(?!.*#.*).*SSLEngine on',
        'variable': 'is_ssl',
        'type': 'bool'
    },
    {
        'regex': r'^(?!.*#.*).*SSLCertificateFile(.*)',
        'variable': 'ssl_crt_path',
        'type': 'string'
    },
    {
        'regex': r'^(?!.*#.*).*SSLCertificateKeyFile(.*)',
        'variable': 'ssl_key_path',
        'type': 'string'
    },
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
