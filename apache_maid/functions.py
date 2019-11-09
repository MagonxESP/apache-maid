from apache_maid.virtualhost import VirtualHostReader, SSLVirtualHost


def print_table(list_dict):
    keys = list_dict[0].keys()
    row_format = ''

    for key in keys:
        max_len = 0

        for item in list_dict:
            len_value = len(str(item[key]))

            if len_value > max_len:
                max_len = len_value

        if max_len < len(key):
            max_len = len(key)

        row_format += ('{:<' + str(max_len) + '} ')

    header = row_format.format(*keys)
    print(header)

    for data_row in list_dict:
        print(row_format.format(*data_row.values()))


def list_virtual_hosts(sites_available_path):
    reader = VirtualHostReader(sites_available_path)
    available = []

    for item in reader.get_available():
        item_dict = {
            'SERVER NAME': item.server_name,
            'DOCUMENT ROOT': item.document_root,
            'PORT': item.port,
            'ENABLED': item.is_enabled()
        }

        if isinstance(item, SSLVirtualHost):
            item_dict['SSL'] = 'On'
        else:
            item_dict['SSL'] = 'Off'

        available.append(item_dict)

    print_table(available)
