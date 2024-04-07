import pint

ureg = pint.UnitRegistry()
mix_units = 3 * ureg.meter + 4 * ureg.cm
print(mix_units) # 3.04 meter

import numpy as np
mix_arry_units = [3, 4] * ureg.meter + [4, 3] * ureg.cm
print(mix_arry_units) # [3.04 4.03] meter
print(np.sum(mix_arry_units)) # 7.07 meter
print(np.mean(mix_arry_units)) # 3.535 meter
print(np.std(mix_arry_units)) # 0.4950000000000001 meter
