import cloudpickle

class Mloader():

    def __init__(self,model_path):
        self.model = cloudpickle.load(open(model_path,'rb'))
    
    def generate(self,num):
        return self.model.generate(num)

    def update(self,label):
        self.model.train(label)
