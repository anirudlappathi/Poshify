from .database import dbsession, Base
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import colorsys

class Clothes(Base):
    __tablename__ = 'Clothes'
    
    clothes_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    clothing_type = Column(String(255))
    color = Column(String(255))
    is_clean = Column(Boolean)

def create_cloth(user_id, clothing_type, color, is_clean):
    try:
        print(f"Starting Function: {user_id}, {clothing_type}, {color}, {is_clean}")
        new_cloth = Clothes(user_id=user_id, clothing_type=clothing_type, color=color, is_clean=is_clean)
        dbsession.add(new_cloth)
        dbsession.commit()
        print(f"Added to Clothes DB: {user_id} {clothing_type}, {color}, {is_clean}")
        return "WORKING"
    except Exception as e:
        print(f"Create Cloth Error: {e}")
        return f"ERROR: {e}"

###
###
###
##3
### NEW CODE HERE
def get_clothing_type_by_user_id(user_id):
    try:
        clothing_types = dbsession.query(Clothes.clothing_type).filter_by(user_id=user_id).all()
        # Extract clothing types from the query result
        clothing_types = [type[0] for type in clothing_types]
        return clothing_types
    except Exception as e:
        print(f"Get Clothing Types Error: {e}")
        return None




# Read (Select) Users
# def get_all_users():
#     try:
#         select_query = "SELECT * FROM clothes"
#         cursor.execute(select_query)
#         clothes = cursor.fetchall()
#         return clothes
#     except mysql.connector.Error as err:
#         print(f"Get All Users Error: {err}")
#         return None

# def get_user_by_id(user_id):
#     try:
#         select_query = "SELECT * FROM clothes WHERE id = %s"
#         cursor.execute(select_query, (user_id,))
#         user = cursor.fetchone()
#         return user
#     except mysql.connector.Error as err:
#         print(f"Get User By ID Error: {err}")
#         return None

# # Update User Information
# def update_user(user_id, new_username, new_first_name, new_last_name, new_email, new_phone_number, new_user_photo_file_name):
#     try:
#         update_query = "UPDATE clothes SET user_id = %s username = %s, first_name = %s, last_name = %s, email = %s, phone_number = %s, user_photo_file_name = %s WHERE id = %s"
#         data = (user_id, new_username, new_first_name, new_last_name, new_email, new_phone_number, new_user_photo_file_name, user_id)
#         cursor.execute(update_query, data)
#         conn.commit()
#         print("User updated successfully.")
#     except mysql.connector.Error as err:
#         print(f"Update User Error: {err}")

# # Delete User
# def delete_user(user_id):
#     try:
#         delete_query = "DELETE FROM clothes WHERE id = %s"
#         cursor.execute(delete_query, (user_id,))
#         conn.commit()
#         print("User deleted successfully.")
#     except mysql.connector.Error as err:
#         print(f"Delete User Error: {err}")

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
    if verbose:
        print("TONE CRISP VALUE: ", tone_output)
        print("TONE FUZZY VALUE: ", tone_membership)
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
    if verbose:
        print("TEMP. CRISP VALUE: ", hue_val)
        print("TEMP. FUZZY VALUE: ", temp_membership)
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


"""
Iterate outfit over all color schemes and get all valid matches
INPUT:
outfit - tuple(top, bot, shs)
    top - hsv
    bot - hsv
    shs - hsv
OUTPUT:
    All names of valid outfit matches
"""
def GetValidMatches(outfit):
    top = GetColorDesc(outfit[0])
    bot = GetColorDesc(outfit[1])
    shs = GetColorDesc(outfit[2])
    outfit_desc = (top, bot, shs)
    
    rules = {"Basic": BasicMatch, "Neutral": NeutralMatch,
             "Analogous": AnalogousMatch, "Summer": SummerMatch,
            "Winter": WinterMatch}
    valid_matches = []
    for key in rules:
        if rules[key](outfit_desc):
            valid_matches.append(key)
    return valid_matches


##PLAN TO CREATE ALGORITHM
#for now have user insert HSV values 