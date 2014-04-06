from elasticutils import MappingType

class WordMappingType(MappingType):

    @classmethod
    def get_index(cls):
        return 'accipiokey-index'

    @classmethod
    def get_mapping_type_name(cls):
        return 'word'

    @classmethod
    def get_mapping(cls):
        return {
            'word': {
                'properties': {
                    'type': 'completion',
                    'index_analyzer': 'simple',
                    'search_analyzer': 'simple',
                    'payloads': True
                }
            }
        }
