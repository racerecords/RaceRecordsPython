import pdb
import uuid
import json

class JSONModel:

    def __init__(self, name):
        self.uuid = int()
        self.name = name
        self.dir = 'js/%s/' % self.name

    def save(self):
        if self.uuid == 0:
            self.new_id()
        with open('%s%s.json' % (self.dir,self.uuid), 'w') as outfile:
            json.dump(self.__dict__, outfile)

    def load(self, uuid):
        with open('%s%s.json' % (self.dir,uuid)) as json_data:
            data = json.load(json_data)
        self.__dict__ = data
        return data

    def new_id(self):
        self.uuid = uuid.uuid4().int
        return self.uuid

    def parse_json(self,data):
        for key, value in data.items():
          self.__dict__[key] = value[0]
        return self.__dict__

class Record(JSONModel):

    def __init__(self):
        with open('template.json') as json_data:
            data = json.load(json_data)
        self.__dict__ = data
        JSONModel.__init__(self,'record')

    def get_readings(self):
        reading = Reading()
        lst = list()
        for uuid in self.readings:
            lst.append(reading.load(uuid))
        return lst

    def new_reading(self):
        reading = Reading()
        reading.save()
        self.readings.append(reading.uuid)
        return self.readings

class Reading(JSONModel):
    
    def __init__(self):
        self.number = int()
        self.carclass = str()
        self.reading = str()
        JSONModel.__init__(self,'reading')
