import json


def json_convert(dict_with_info: dict, limit: str):
    json_date = None

    output = {'Feed': [],
              'Entries': []
              }
    temp = {'Title': [],
            'Date': [],
            'Links': [],
            'Info': []
            }
    if type(dict_with_info) == dict:
        output['Feed'] = dict_with_info['Feed']
        for index in range(int(len(limit))):
            temp['Title'] = dict_with_info['Title'][index]
            temp['Date'] = dict_with_info['Date'][index]
            temp['Links'] = dict_with_info['Links'][index]
            temp['Info'] = dict_with_info['Info'][index]
            output['Entries'].append(temp)
        json_date = json.dumps(output, ensure_ascii=False)
    return json_date


