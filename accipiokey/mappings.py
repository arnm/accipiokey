from accipiokey import settings
from elasticutils import MappingType

class WordMappingType(MappingType):

    @classmethod
    def get_index(cls):
        return settings.INDEX

    @classmethod
    def get_mapping_type_name(cls):
        return 'word'

    @classmethod
    def get_mapping(cls):
        return {
            cls.get_mapping_type_name() : {
                'properties': {
                    'user': {'type': 'string'},
                    'text': {
                        'type': 'completion',
                        'index_analyzer': 'simple',
                        'search_analyzer': 'simple',
                        'payloads': True
                    }
                }
            }
        }
