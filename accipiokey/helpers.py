from elasticsearch.helpers import bulk

def index_str_list(client, index, doc_type, str_list, normalize_func=lambda s: s.lower().rstrip()):

    actions = []
    for id, string in enumerate(str_list):
        action = {'_id': id, 'text' : normalize_func(string)}
        actions.append(action)
    bulk(client, actions, index=index, doc_type=doc_type)






