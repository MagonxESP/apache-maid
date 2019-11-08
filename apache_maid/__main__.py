import argparse
import apache_maid.settings
import apache_maid.functions

settings = apache_maid.settings.Settings()

if settings.exits() is False:
    settings = apache_maid.settings.configure()

settings.load()

parser = argparse.ArgumentParser(prog='apache-maid', description='Apache virtualhost manager')
parser.add_argument('option', type=str, help='See --options')
parser.add_argument('arguments', nargs='*', default=None, type=str, help='See --help=option')

args = parser.parse_args()

if args.option == 'config':
    settings = apache_maid.settings.configure()
elif args.option == 'create':
    pass
elif args.option == 'disable':
    pass
elif args.option in ['list', 'ls']:
    apache_maid.functions.list_virtual_hosts(settings.get('sites_available'), settings.get('sites_enabled'))
elif args.option == 'remove':
    pass
elif args.option == 'enable':
    pass
