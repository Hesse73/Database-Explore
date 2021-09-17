import model
import cloudpickle

cloudpickle.register_pickle_by_value(model)
cloudpickle.dump(model.CarModel(),open('test.bin','wb'))