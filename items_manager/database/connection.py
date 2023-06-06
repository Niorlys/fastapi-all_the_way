import redis
import ujson
from typing import Type, Any, Union
"""
Pendant: Validations of field by unicity, etc using db!=0"""

class Connection(redis.Redis):
    def __init__(self,config=None):
        """
            Basic config by default
            {
                "host":"localhost",
                "port":6379,
                "db":0

            }
        """
        self.config = config
        if not config:
            return super().__init__()
        return super().__init__(**config)
    
    def create_record(self, instance:Any, attr_id:Union[int, None] =None, *fields:str):
        cls_name=type(instance).__name__
        instance.id  = getattr(instance, attr_id) if attr_id != None else int(self.get(f'{cls_name}_last_id') or '0') + 1
        serialized_data = self.serialize_instance(instance,*fields)
        self.set(f'{cls_name}_{instance.id}',serialized_data)
        if not self.sismember(cls_name, instance.id):
            self.sadd(f'{cls_name}',instance.id)
            self.set(f'{cls_name}_last_id',instance.id)
        return instance
    
    def update_record(self,cls:Type[Any], id:int, **fields_dict):
        cls_name = cls.__name__
        key =  f'{cls_name}_{id}'
        data = ujson.loads(self.get(key))
        data.update(fields_dict)
        self.set(key,ujson.dumps(data))
        return data

    def get_record(self,cls:Type[Any], id:int):
        data = ujson.loads(self.get(f'{cls.__name__}_{id}'))
        return data
    
    def get_all(self, cls:Type[Any]):
        return [self.retrieve_record(cls,id.decode()) for id in self.smembers(cls.__name__)]
    

    def get_filtered(self, cls:Type[Any], lasts:int, desc:bool = True): # Do it more flexible
        last_id = int(self.get_last(cls))
        _lasts = []
        while lasts and last_id:
            if self.sismember(cls.__name__, last_id):
                _lasts.append(ujson.loads(self.get(f'{cls.__name__}_{last_id}')))
                lasts = lasts - 1
            last_id = last_id - 1
        if not desc:
            _lasts.reverse()
        return _lasts

    def delete_record(self,cls:Type[Any],id:int):
        name = cls.__name__
        if id == self.get(f'{name}_last_id'):
            for i in range(id,0,-1):
                new_last = self.get(f'{name}_id')
                if new_last:
                    self.set(f'{name}_last_id', new_last)
                    break
            else:
                self.set(f'{name}_last_id', 1)
        self.delete(f'{name}_{id}')
        return self.srem(name, id) #1 if somtheing was remove else 0


    def serialize_instance(self,instance:Any,*fields:str):
        instance_map = vars(instance)
        if not len(fields):
            fields = instance.__annotations__.keys()
        return ujson.dumps({key:instance_map[key] for key in fields})
    
    def get_last(self, cls:Type[Any]):
        return self.get(f'{cls.__name__}_last_id')



