from dataclasses import dataclass
from typing import NamedTuple

class Result:
    id: str
    addressId: str

    def __getattr__(self, name):
        return name

print(Result().id) # print "id"
print(Result().addressId) # print "addressId"


# ====== no need __getattr__ ======
class Result4():
    id: str = "id"
    addressId: str = "addressId"

print(Result4().id) # print "id"
print(Result4().addressId) # print "addressId"


# ====== NamedTuple for existing class ======
class Result3(NamedTuple):
    id: str
    addressId: str

r= Result3("id", "addressId")
print(r.id) # print "id"
print(r.addressId) # print "addressId"


# ====== dataclass for existing class ======
@dataclass
class Result2:
    id: str
    address_id: str

r = Result2("123", "456")
print(r.id) # print "123"
print(r.address_id) # print "456"


# ====== for getting the name of class, function, module, or instance ======
def nameof(obj):
    """Return a reasonable name for classes, functions, modules or instances."""
    if hasattr(obj, "__name__"):
        return obj.__name__
    return type(obj).__name__

print(nameof(Result))  # Output: Result
print(nameof(r))        # Output: Result2
print(nameof(42))       # Output: int
print(nameof("hello"))  # Output: str
print(nameof(nameof))   # Output: nameof
