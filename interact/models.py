from django.db import models
from jsonfield import JSONField
# Create your models here.


class User(models.Model):
    account = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    name = models.CharField(max_length=128)

    @classmethod
    def create_user(cls, account, password, name):
        user = cls(account=account, password=password, name=name)
        user.save()
        return user

    class Meta:
        db_table = "users"


class Explore(models.Model):
    account = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    records = JSONField(null=True)

    @classmethod
    def init_explore(cls, account, name):
        explore = cls(account=account, name=name, records=[])
        explore.save()
        return explore

    class Meta:
        db_table = "explore"


class Database(models.Model):
    '''
    Example format:
    name = 'car_database'
    trained_models = {"test": {"path":"test.bin","intro":"使用坠新科技打造地船新版本，是尊贵的您的不二之选。"}}
    intro = {"item_num":43234,
            "attrs":{"discrete": ["seller", "offerType", "abtest", "vehicleType", "gearbox","model","fuelType","brand","notRepairedDamage"],
             "continuous": ["price", "powerPS", "kilometer", "Age"]
            },
            "attr_details":{
                "discrete":{
                    "vehicleType": {
                        "limousine": 11707,
                        "kleinwagen": 9434,
                        "kombi": 8297,
                        "bus": 3722,
                        "NaN": 2832,
                        "rest": 7242
                        }
                    },
                "continuous": {
                    "price": {
                        "min": 100,
                        "max": 145000,
                        "counter": [
                            42420,
                            714,
                            76,
                            14,
                            10
                        ]
                    },
                }
                }
            }
            }
    '''
    name = models.CharField(max_length=256)
    trained_models = JSONField(null=True)
    intro = JSONField(null=True)

    @classmethod
    def add_database(cls, name, trained_models,intro):
        db = cls(name=name, trained_models=trained_models,intro = intro)
        db.save()
        return db

    class Meta:
        db_table = "databases"
