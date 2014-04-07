from accipiokey import settings
from elasticutils import MappingType

class UserMappingType(MappingType):
    @classmethod
    def get_index(cls):
        return settings.INDEX

    @classmethod
    def get_mapping_type_name(cls):
        return 'user'

    @classmethod
    def get_mapping(cls):
        return {
            cls.get_mapping_type_name() : {
                'properties': {
                    'username': { 'type': 'string' },
                    'password': { 'type': 'string', 'index': 'not_analyzed' }
                }
            }
        }

class StatSheetMappingType(MappingType):
    @classmethod
    def get_index(cls):
        return settings.INDEX

    @classmethod
    def get_mapping_type_name(cls):
        return 'statsheet'

    @classmethod
    def get_mapping(cls):
        return {
            cls.get_mapping_type_name() : {
                '_parent': { 'type': 'user' },
                'properties': {
                    'words_recorded': { 'type': 'integer' },
                    'words_corrected': { 'type': 'integer' },
                    'generations_completed': { 'type': 'integer' },
                    'keystrokes_saved': { 'type': 'integer' }
                }
            }
        }

class WritingMappingType(MappingType):
    @classmethod
    def get_index(cls):
        return settings.INDEX

    @classmethod
    def get_mapping_type_name(cls):
        return 'writing'

    @classmethod
    def get_mapping(cls):
        return {
            cls.get_mapping_type_name() : {
                '_parent': { 'type': 'user' },
                'properties': {
                    'content': { 'type': 'string' }
                }
            }
        }

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
                '_parent': { 'type': 'user' },
                'properties': {
                    'text': {
                        'type': 'completion',
                        'index_analyzer': 'simple',
                        'search_analyzer': 'simple',
                        'payloads': True
                    }
                }
            }
        }
