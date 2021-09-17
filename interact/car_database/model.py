import random


class CarModel():
    def __init__(self):
        self.attrs = {"discrete": ["seller", "offerType", "abtest", "vehicleType", "gearbox", "model",
                                   "fuelType", "brand", "notRepairedDamage"],
                     "continuous": ["price", "powerPS", "kilometer", "Age"]}

    def generate(self, num):
        data = []
        for i in range(num):
            discrete = {}
            continuous = {}
            for name in self.attrs['discrete']:
                discrete[name] = random.randint(0, 10)
            for name in self.attrs['continuous']:
                continuous[name] = random.random()*100
            data.append({'discrete': discrete, 'continuous': continuous})
        return data

    def train(self, data):
        pass
