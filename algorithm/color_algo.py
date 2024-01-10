import numpy as np
import matplotlib.pyplot as plt

import skfuzzy as fuzz
from skfuzzy import control as ctrl

##ALGORITHM IMPLEMENTATION

hue_range = np.arange(0, 361, 1)
hue_fuzzy = ['WARM', 'COOL', 'WARM_']
hue = ctrl.Antecedent(hue_range, 'hue')
hue['WARM'] = fuzz.gaussmf(hue.universe, 0, 60)
hue['COOL'] = fuzz.gaussmf(hue.universe, 180, 60)
hue['WARM_'] = fuzz.gaussmf(hue.universe, 360, 60)


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


"""
Consequents
TONE: mix of Saturation and Value that indicate if color is neutral or dark/bright
{ NEUTRAL, DARK, BRIGHT }
"""
tone_range = np.arange(0, 12, 1)
tone_fuzzy = ['NEUTRAL', 'DARK', 'BRIGHT']
tone = ctrl.Consequent(tone_range, 'tone')

tone['NEUTRAL'] = fuzz.trapmf(tone.universe, [0, 0, 1, 2])
tone['DARK'] = fuzz.gbellmf(tone.universe, 2, 1, 3)
tone['BRIGHT'] = fuzz.gbellmf(tone.universe, 4, 1, 9.5)
#tone['NEUTRAL_'] = fuzz.trimf(tone.universe, [10, 11, 11])


"""
RULES
"""
rule1 = ctrl.Rule(val['BLACK'] | sat['GRAY'] | sat['VERY_FADED'], tone['NEUTRAL'], 'Dark colors without color (low brightness/dark) considered neutral')
rule2 = ctrl.Rule(val['VERY_DARK'] & sat['SATURATED'], tone['NEUTRAL'], 'Very dark colors with high saturation')
rule3 = ctrl.Rule(val['DARK'] & sat['FADED'], tone['DARK'], 'Dark color with normal saturation')
rule4 = ctrl.Rule(val['DARK'] & sat['VERY_SATURATED'], tone['BRIGHT'], 'Dark color with high saturation')
rule5 = ctrl.Rule(val['BRIGHT'] & sat['SATURATED'], tone['BRIGHT'], 'Bright color with high saturation')
rule6 = ctrl.Rule(val['VERY_BRIGHT'] & sat['FADED'], tone['BRIGHT'], 'Very bright color with some saturation')
rule7 = ctrl.Rule(val['VERY_BRIGHT'] & sat['VERY_SATURATED'], tone['BRIGHT'], 'Very bright color with high saturation')
rule8 = ctrl.Rule(val['VERY_DARK'] & sat['FADED'], tone['NEUTRAL'], 'Very dark color with faded saturation')

"""
Control system
for tones
"""
tone_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])


"""
GetMembership
Returns String representing the Fuzzy value given a variable's range, model, and crisp value
"""
def GetMembership(fuzzy_values, var_range, var_model, crisp_value):
    max_membership = 0
    membership_name = fuzzy_values[0]
    for i in range(len(fuzzy_values)):
        temp_memb = fuzz.interp_membership(var_range, var_model[fuzzy_values[i]].mf, crisp_value)
        if temp_memb > max_membership:
            max_membership = temp_memb
            membership_name = fuzzy_values[i]
    return membership_name

"""
Given Saturation and Value, returns a String indicating if the combination 
of both values results in a 'NEUTRAL', 'DARK', or 'BRIGHT' tone.
INPUT:
values - tuple(sat, val)
    + sat - value from 0-100
    + val - value from 0-100
verbose - prints both crisp value and fuzzy value
"""
def GetTone(values, verbose=False):
    tone_sim = ctrl.ControlSystemSimulation(tone_ctrl)
    tone_sim.input['saturation'] = values[0]
    tone_sim.input['value'] = values[1]
    tone_sim.compute()
    tone_output = tone_sim.output['tone']
    tone_membership = GetMembership(tone_fuzzy, tone_range, tone, tone_output)
    return tone_membership

"""
Given Hue, returns a String indicating if the color belongs
to 'WARM' or 'COOL' colors.
INPUT:
hue - value from 0-360
verbose - prints both crisp value and fuzzy value
"""
def GetColorTemp(hue_val, verbose=False):
    temp_membership = GetMembership(hue_fuzzy, hue_range, hue, hue_val)
    return temp_membership


"""
Given Hue, Saturation, and Value, returns a String describing
the specified color. The output is composed of both the tone of
the color, and the temperature of the color.
INPUT:
hsv - tuple(hue, sat, val)
    + hue - value from 0-360
    + sat - value from 0-100
    + val - value from 0-100
OUTPUT: (TONE, TEMP) ex. (DARK, WARM)
"""
def GetColorDesc(hsv):
    tone = GetTone((hsv[1], hsv[2]))
    temp = GetColorTemp(hsv[0])
    if temp == "WARM_": temp = "WARM"
    return (tone, temp)




def BasicMatch(outfit):
    top = outfit[0]
    bot = outfit[1] 
    shoes = outfit[2]
    
    bright_count = len([i for i in outfit if i[0] == 'BRIGHT'])
    if bright_count > 1: return False
    # Check for high contrast
    
    return True

def AnalogousMatch(outfit):
    top = outfit[0]
    bot = outfit[1] 
    shoes = outfit[2]
    
    cool_count = len([color for color in outfit if color[1] == 'COOL'])
    warm_count = len(outfit) - cool_count
    if cool_count < len(outfit) and warm_count < len(outfit):
        return False
    
    return True

def NeutralMatch(outfit):
    top = outfit[0]
    bot = outfit[1] 
    shoes = outfit[2]
    
    neutral = [color for color in outfit if color[0] == 'NEUTRAL']
    if len(neutral) != len(outfit):
        return False
    
    return True

def ContrastMatch(outfit):
    top = outfit[0]
    bot = outfit[1] 
    shoes = outfit[2]
    
    warm_count = len([color for color in outfit if color[1] == 'WARM'])
    if warm_count < 1: return False
    
    dark_count = len([color for color in outfit if color[0] == 'DARK'])
    bright_count = len([color for color in outfit if color[0] == 'BRIGHT'])
    if dark_count < 1 or bright_count < 1:
        return False
    
    return True

def SummerMatch(outfit):
    top = outfit[0]
    bot = outfit[1] 
    shoes = outfit[2]
    
    non_neutral = [color for color in outfit if color[0] != 'NEUTRAL']
    
    warm_count = len([color for color in non_neutral if color[1] == 'WARM'])
    if warm_count < 2: return False
    
    dark_count = len([color for color in non_neutral if color[0] == 'DARK'])
    if dark_count > 1: return False
    
    bright_count = len(non_neutral) - dark_count
    if bright_count < 1: return False
    
    return True

def WinterMatch(outfit):
    top = outfit[0]
    bot = outfit[1] 
    shoes = outfit[2]
    
    non_neutral = [color for color in outfit if color[0] != 'NEUTRAL']
    
    dark_count = len([color for color in non_neutral if color[0] == 'DARK'])
    if dark_count < 1: return False
    
    bright_count = len(non_neutral) - dark_count
    if bright_count > 0: return False
    
    return True

def GetStyleOutfits(tops, bots, shoes, calendarInfo, cloth_ids):
    
    matchingOutfits = []

    if not (tops and bots and shoes): return matchingOutfits
    for top in tops:
        if not top["is_clean"]: continue
        topdesc = GetColorDesc((top["hue"], top["saturation"], top["value"]))
        for bot in bots:
            if not bot["is_clean"]: continue
            botdesc = GetColorDesc((bot["hue"], bot["saturation"], bot["value"]))
            for shoe in shoes:

                if f"{top['id']},{bot['id']},{shoe['id']}" in cloth_ids: continue
                if not shoe["is_clean"]: continue

                outfitRules = []

                shoedesc = GetColorDesc((shoe["hue"], shoe["saturation"], shoe["value"]))
                for rule in [BasicMatch, NeutralMatch, AnalogousMatch, SummerMatch, WinterMatch]:
                    if rule((topdesc, botdesc, shoedesc)):
                        outfitMatch = str(rule).split()[1][:-5]
                        outfitRules.append(outfitMatch)

                if len(outfitRules) > 0:
                    matchingOutfits.append((outfitRules, (top["clothing_name"], top["url"], top["id"]), (bot["clothing_name"], bot["url"], bot["id"]), (shoe["clothing_name"], shoe["url"], shoe["id"])))

    return matchingOutfits


