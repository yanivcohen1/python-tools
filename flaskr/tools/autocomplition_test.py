from dataclasses import dataclass

class Result:
    id: str
    addressId: str

    def __getattr__(self, name):
        return name

print(Result().id) # print "id"
print(Result().addressId) # print "addressId"

# ====== no need setters/getters with dataclass ======
@dataclass
class Result2:
    id: str
    address_id: str

r = Result2("123", "456")
print(r.id) # print "123"
print(r.address_id) # print "456"
