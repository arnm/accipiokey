from elasticsearch.helpers import bulk

def index_str_list(client, index, doc_type, str_list, normalize_func=lambda string: string.lower()):

    actions = []
    for id, string in enumerate(str_list):
        index_dict = {'index': {'_index': index, '_type': doc_type, '_id': id}}
        value_dict = {'string': normalize_func(string)}
        actions.append(index_dict)
        actions.append(value_dict)
    bulk(client, actions)






