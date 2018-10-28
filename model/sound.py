import pdb
import uuid
import json

class JSONModel:

    def __init__(self):
#        with open('js/template.json') as json_data:
#            data = json.load(json_data)
#        self.__dict__ = data
        self.id = int()
        self.track = str()
        self.date = str()
        self.region = str()
        self.classes = list()
        self.ambientBefore = str()
        self.groupNumber = str()
        self.reader = str()
        self.recorder = str()
        self.siteCertificationDate = str()
        self.factoryCalibrationDate = str()
        self.fieldCalibrationTime = str()
        self.batteryLevel = str()
        self.microphoneLocation = str()
        self.start = str()
        self.end = str()
        self.temperature = str()
        self.humidity = str()
        self.barometer = str()
        self.weather = str()
        self.windSpeed = str()
        self.windDirection = str()
        self.readings = list()

    def save(self):
        if self.id == 0:
            self.new()
        with open(f'js/{self.id}.json', 'w') as outfile:
            json.dump(self.__dict__, outfile)

    def read(self):
        with open(f'js/{self.id}.json') as json_data:
            data = json.load(json_data)
        self.__dict__ = data

    def new(self):
        self.id = uuid.uuid4().int

    def update_reading(self, id):
        self.id = id
        self.read()

    def new_reading(self, lst):
        self.read()
        car = dict()
        car['carnumber'] = lst[0]
        car['carclass'] = lst[1]
        car['reading'] = lst[2]
        self.readings.append(car)
        self.save()
