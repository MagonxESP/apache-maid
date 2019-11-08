from apache_maid.virtualhost import VirtualHostReader, VirtualHost, SSLVirtualHost


def print_table(list_dict):
    keys = list_dict[0].keys()
    row_format = ''

    for key in keys:
        max_len = 0

        for item in list_dict:
            len_value = len(str(item[key]))

            if len_value > max_len:
                max_len = len_value

        row_format += ('{:<' + str(max_len) + '} ')

    header = row_format.format(*keys)
    print(header)

    for data_row in list_dict:
        print(row_format.format(*data_row.values()))


def list_virtual_hosts(sites_available_path, sites_enabled_path):
    reader = VirtualHostReader(sites_available_path)
    available = [item.__dict__ for item in reader.get_available()]
    available_list = []
    max_len = 0
    keys = []

    for item in available:
        keys_len = len(item.keys())

        if keys_len > max_len:
            keys = tuple(item.keys())
            max_len = keys_len

    for item in available:
        item_dict = {}

        for key in keys:
            new_key = key.replace('_', ' ').lstrip(' ').upper()

            if key not in item:
                item_dict[new_key] = ''
            elif key != '_server_alias':
                item_dict[new_key] = item[key]

        available_list.append(item_dict)

    print_table(available_list)
