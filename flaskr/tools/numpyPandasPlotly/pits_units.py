import pint

ureg = pint.UnitRegistry()
mix_units = 3 * ureg.meter + 4 * ureg.cm
print(mix_units)
