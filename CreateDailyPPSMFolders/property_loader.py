import configparser

class PropertyLoader:
    property_file_path = None
    properties = configparser.ConfigParser()

    @classmethod
    def load_properties(cls):
        if cls.property_file_path is None:
            raise ValueError("Property file path is not set.")
        cls.properties.read(cls.property_file_path)

    @classmethod
    def get_property(cls, key):
        return cls.properties['DEFAULT'].get(key, None)
