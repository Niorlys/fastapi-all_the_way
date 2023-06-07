from typing import Type, Any
#Method to set all statics attributes of a object whose values comes in form of a dict
def set_statics(instance:Type[Any], data:dict):
    attrs = instance.__annotations__.keys()
    assert all(attr in data for attr in attrs), "Data provided does not fit with class's static attributes, check keys."
    for attr in attrs:
        setattr(instance, attr, data[attr])
