import yaml
import os.path


class Settings:

    _settings_path = '.config/apache_maid'
    _settings_file_name = 'conf.yml'
    _settings_full_path = ''
    _settings = {}

    def __init__(self):
        self._settings_path = os.path.expanduser('~') + '/' + self._settings_path
        self._settings_full_path = self._settings_path + '/' + self._settings_file_name

    def load(self):
        try:
            with open(self._settings_full_path, 'r') as file:
                self._settings = yaml.load(file)
        except yaml.YAMLError as e:
            print(e)

    def save(self):
        try:
            if os.path.exists(self._settings_path) is False:
                os.makedirs(self._settings_path)

            with open(self._settings_full_path, 'w') as file:
                yaml.dump(self._settings, file)
        except yaml.YAMLError as e:
            print(e)

    def set(self, key, value):
        self._settings[key] = value

    def get(self, key):
        return self._settings[key]

    def exits(self):
        return os.path.exists(self._settings_full_path)


def configure():
    settings = Settings()
    default_sites_available_path = '/etc/apache2/sites-available'
    default_sites_enable_path = '/etc/apache2/sites-enabled'
    default_ports_conf = '/etc/apache2/ports.conf'

    sites_available = input('Sites available directory path (' + default_sites_available_path + '): ')

    if sites_available == '\n' or sites_available == '':
        sites_available = default_sites_available_path

    settings.set('sites_available', sites_available)

    sites_enabled = input('Sites enabled directory path (' + default_sites_enable_path + '): ')

    if sites_enabled == '\n' or sites_enabled == '':
        sites_enabled = default_sites_enable_path

    settings.set('sites_enabled', sites_enabled)

    ports = input('Ports file path (' + default_ports_conf + '): ')

    if ports == '\n' or ports == '':
        ports = default_ports_conf

    settings.set('ports_conf', ports)
    settings.save()

    return settings
