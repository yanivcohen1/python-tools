def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts

coins_lst = [100, 50, 25]
print(total(*coins_lst), "Knuts")

coins_dict = {"galleons": 100, "sickles": 50, "knuts": 25}
print(total(**coins_dict), "Knuts")

print("is the same:", total(*coins_lst) == total(**coins_dict))
