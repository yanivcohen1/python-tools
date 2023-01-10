""" If you are using python 3.6+, you can use:
pip install marshmallow-enum and
pip install marshmallow-dataclass

Its simple and type safe.

You can transform your class in a string-json and vice-versa:
 """
#https://pypi.org/project/marshmallow-dataclass/
# from marshmallow_dataclass import dataclass
import json
from marshmallow import Schema
# from dataclasses import field
# import datetime
from marshmallow_enum import Enum
# add
from dataclasses import dataclass, field
from typing import List, Optional, ClassVar, Type

import marshmallow
import marshmallow_dataclass

#Class definitions:
@dataclass # for serialization
class OrderStatus(Enum):
    CREATED = 'Created'
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    FAILED = 'Failed'

@dataclass
class User:
    def __init__(self, name, orderId, productName, quantity, status):
        self.name = name
        self.orderId = orderId
        self.productName = productName
        self.quantity = quantity
        self.status = status

    name: str
    orderId: str
    productName: str
    quantity: int
    status: OrderStatus
    Schema: ClassVar[Type[Schema]] = Schema # For the type checker

#From Object to String Json:
UserSchema = marshmallow_dataclass.class_schema(User)

user = User("Danilo","50","RedBull",15,OrderStatus.CREATED)
user_json_str = UserSchema().dumps(user)
#user_json_str = user_json.data
print(user_json_str) #print(user,flush=True)

#From String Json to Object:

json_str = {"name":"Danilo1", "orderId":"501", "productName":"RedBull1", "quantity":151, "status":"Pending"}
#user2, err = User.Schema().loads(json_str)
user_json = json.loads(user_json_str)
user2: User = UserSchema().load(user_json)
print(user2,flush=True)
if user2.status == OrderStatus.PENDING:
    print('Pending')

