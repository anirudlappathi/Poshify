import numpy as np
import matplotlib.pyplot as plt

import skfuzzy as fuzz
from skfuzzy import control as ctrl

"""
Antecedents HSV
HUE: color represented by number from 0(red) - 360(violet)
{ WARM, COOL }

SATURATION: color saturation represented by number from 0(faded/gray color) - 100(full color)
{ GRAY, VERY_FADED, FADED, SATURATED, VERY_SATURATED }

VALUE: brightness represented by number 0(dark) - 100(light)
{ BLACK, VERY_DARK, DARK, BRIGHT, VERY_BRIGHT }
"""

hueFuzzy = ["WARM", "COOL", "WARM_"]
hue = ctrl.Antecedent(np.arange(0, 361, 1), "hue")
hue["WARM"] = fuzz.gaussmf(hue.universe, 0, 60)
hue["COOL"] = fuzz.gaussmf(hue.universe, 180, 60)
hue["WARM_"] = fuzz.gaussmf(hue.universe, 360, 60)

sat = ctrl.Antecedent(np.arange(0, 101, 1), 'saturation')
sat_fuzzy = ['GRAY', 'VERY_FADED', 'FADED', 'SATURATED', 'VERY_SATURATED']
sat['GRAY'] = fuzz.gaussmf(sat.universe, 0, 10)
sat['VERY_FADED'] = fuzz.gaussmf(sat.universe, 25, 10)
sat['FADED'] = fuzz.gaussmf(sat.universe, 50, 10)
sat['SATURATED'] = fuzz.gaussmf(sat.universe, 75, 10)
sat['VERY_SATURATED'] = fuzz.gaussmf(sat.universe, 100, 10)


val = ctrl.Antecedent(np.arange(0, 101, 1), 'value')
val_fuzzy = ['BLACK', 'VERY_DARK', 'DARK', 'BRIGHT', 'VERY_BRIGHT']
val['BLACK'] = fuzz.gaussmf(val.universe, 0, 10)
val['VERY_DARK'] = fuzz.gaussmf(val.universe, 25, 10)
val['DARK'] = fuzz.gaussmf(val.universe, 50, 10)
val['BRIGHT'] = fuzz.gaussmf(val.universe, 75, 10)
val['VERY_BRIGHT'] = fuzz.gaussmf(val.universe, 100, 10)