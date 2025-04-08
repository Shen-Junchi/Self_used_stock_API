import numpy as np
import math

def MA(stock_data,col_name,window):
    """
    Calculate the moving average of a given column in stock data.

    :param stock_data: DataFrame containing stock data
    :param col_name: Name of the column to calculate the moving average for
    :param window: Window size for the moving average
    :return: DataFrame with the moving average column added
    """
    stock_data = stock_data.copy()  # Create a copy of the DataFrame to avoid modifying the original
    stock_data[f'{col_name}_MA{window}'] = stock_data[col_name].rolling(window=window).mean()

    return stock_data[f'{col_name}_MA{window}']


# Example usage:
# Assuming you have a DataFrame called 'stock_data' with a column 'Close'
# stock_data = pd.DataFrame({'Close': [100, 101, 102, 103, 104]})
# MA_1 = MA(stock_data, 'Close', 3)
# MA_2 = MA(stock_data, 'Close', 5)

def nature_log(MA_1, MA_2):
    """
    Calculate the natural logarithm of a given column in stock data.

    :param stock_data: DataFrame containing stock data
    :param col_name: Name of the column to calculate the natural logarithm for
    :return: DataFrame with the natural logarithm column added
    """
    return np.log(MA_1 / MA_2)


# Example usage:
# As for nature log
# log_result = nature_log(MA_1, MA_2)
# print(log_result)


def Fuzzification(nature_log, fuzzi_parameter):
    """
    Fuzzification of the natural logarithm value based on Figure 1 definitions.

    :param nature_log: The input value x (e.g., x = ln(MA_short / MA_long))
    :param fuzzi_parameter: The fuzzification parameter w (must be positive)
    :return: A dictionary containing the membership degrees for each fuzzy set 
             {'NL', 'NM', 'NS', 'AZ', 'PS', 'PM', 'PL'}
    """
    x = nature_log
    w = fuzzi_parameter

    if w <= 0:
        raise ValueError("fuzzi_parameter (w) must be positive")

    memberships = {}

    # AZ (Around Zero)
    if -w <= x <= w:
        memberships['AZ'] = 1 - abs(x) / w
    else:
        memberships['AZ'] = 0.0

    # PS (Positive Small)
    if 0 <= x <= 2 * w:
        memberships['PS'] = 1 - abs(x - w) / w
    else:
        memberships['PS'] = 0.0

    # PM (Positive Medium)
    if w <= x < 2 * w:
        memberships['PM'] = (x - w) / w
    elif 2 * w <= x <= 3 * w:
        memberships['PM'] = (3 * w - x) / w
    else:
        memberships['PM'] = 0.0
        
    # PL (Positive Large)
    if x < 2 * w:
        memberships['PL'] = 0.0
    elif 2 * w <= x <= 3 * w:
        memberships['PL'] = (x - 2 * w) / w
    else: # x > 3*w
        memberships['PL'] = 1.0

    # NS (Negative Small) - Mirror of PS
    if -2 * w <= x <= 0:
        memberships['NS'] = 1 - abs(x + w) / w
    else:
        memberships['NS'] = 0.0

    # NM (Negative Medium) - Mirror of PM
    if -3 * w <= x < -2 * w:
        memberships['NM'] = (x + 3 * w) / w
    elif -2 * w <= x <= -w:
        memberships['NM'] = (-w - x) / w
    else:
        memberships['NM'] = 0.0
        
    # NL (Negative Large) - Mirror of PL
    if x > -2 * w:
        memberships['NL'] = 0.0
    elif -3 * w <= x <= -2 * w:
        memberships['NL'] = (-2 * w - x) / w
    else: # x < -3*w
        memberships['NL'] = 1.0
        
    # Ensure numerical precision doesn't create values slightly outside [0, 1]
    for key in memberships:
        memberships[key] = max(0.0, min(1.0, memberships[key]))

    return memberships

# Example usage:
# w_param = 0.01
# x_input = 0.003
# fuzzified_values = Fuzzification(x_input, w_param)
# print(f"For x = {x_input} and w = {w_param}:")
# print(fuzzified_values)
# Expected output approx: {'AZ': 0.7, 'PS': 0.3, 'PM': 0.0, 'PL': 0.0, 'NS': 0.0, 'NM': 0.0, 'NL': 0.0}

# x_input_2 = 0.016
# fuzzified_values_2 = Fuzzification(x_input_2, w_param)
# print(f"\nFor x = {x_input_2} and w = {w_param}:")
# print(fuzzified_values_2)
# Expected output approx: {'AZ': 0.0, 'PS': 0.4, 'PM': 0.6, 'PL': 0.0, 'NS': 0.0, 'NM': 0.0, 'NL': 0.0}


def rule_activation_rule1(fuzzified_input):
    """
    Determines the activation strength for the output fuzzy sets based on 
    Rule 1 Group and the fuzzified input.

    Rule 1 Group (from paper Eq. 7):
    1: IF PS THEN BS
    2: IF PM THEN BB
    3: IF PL THEN SM
    4: IF NS THEN SS
    5: IF NM THEN SB
    6: IF NL THEN BM
    7: IF AZ THEN N

    :param fuzzified_input: A dictionary containing the membership degrees 
                             for input fuzzy sets (e.g., output of Fuzzification function).
                             Example: {'AZ': 0.7, 'PS': 0.3, 'PM': 0.0, ...}
    :return: A dictionary where keys are the output fuzzy set labels 
             (e.g., 'BS', 'N') and values are their corresponding activation strengths.
             Only rules with activation > 0 are included.
    """
    
    # Define the mapping from input fuzzy set (premise) to output fuzzy set (consequence)
    # based on Rule 1 Group (Eq. 7)
    rule_mapping = {
        'PS': 'BS',
        'PM': 'BB',
        'PL': 'SM',
        'NS': 'SS',
        'NM': 'SB',
        'NL': 'BM',
        'AZ': 'N'
    }

    activated_outputs = {}

    # Iterate through the input fuzzy sets and their membership degrees
    for input_set, activation_strength in fuzzified_input.items():
        # Check if the rule associated with this input set is activated
        if activation_strength > 0:
            # Find the corresponding output fuzzy set label from the rule mapping
            if input_set in rule_mapping:
                output_set_label = rule_mapping[input_set]
                # Store the activation strength for this output set.
                # If multiple rules conclude the same output set (not in this specific rule set,
                # but possible in others), different fuzzy logic systems might handle it 
                # differently (e.g., max, sum). Here, since each input maps to a unique 
                # output in Rule 1 Group, we just assign it.
                activated_outputs[output_set_label] = activation_strength

    return activated_outputs

# Example usage (using the result from the previous Fuzzification example):

# Case 1: x = 0.003 -> fuzzified_input = {'AZ': 0.7, 'PS': 0.3, 'PM': 0.0, 'PL': 0.0, 'NS': 0.0, 'NM': 0.0, 'NL': 0.0}
# fuzzified_input_1 = {'AZ': 0.7, 'PS': 0.3, 'PM': 0.0, 'PL': 0.0, 'NS': 0.0, 'NM': 0.0, 'NL': 0.0}
# activated_rules_1 = rule_activation_rule1(fuzzified_input_1)
# print(f"For fuzzified_input_1: {fuzzified_input_1}")
# print(f"Activated output sets and strengths: {activated_rules_1}")
# Expected output: {'N': 0.7, 'BS': 0.3} 
# (Rule 7 'IF AZ THEN N' activated with 0.7, Rule 1 'IF PS THEN BS' activated with 0.3)

# Case 2: x = 0.016 -> fuzzified_input = {'AZ': 0.0, 'PS': 0.4, 'PM': 0.6, 'PL': 0.0, 'NS': 0.0, 'NM': 0.0, 'NL': 0.0}
# fuzzified_input_2 = {'AZ': 0.0, 'PS': 0.4, 'PM': 0.6, 'PL': 0.0, 'NS': 0.0, 'NM': 0.0, 'NL': 0.0}
# activated_rules_2 = rule_activation_rule1(fuzzified_input_2)
# print(f"\nFor fuzzified_input_2: {fuzzified_input_2}")
# print(f"Activated output sets and strengths: {activated_rules_2}")
# Expected output: {'BS': 0.4, 'BB': 0.6}
# (Rule 1 'IF PS THEN BS' activated with 0.4, Rule 2 'IF PM THEN BB' activated with 0.6)

# Case 3: x = 0.02 -> fuzzified_input = {'AZ': 0.0, 'PS': 0.0, 'PM': 1.0, 'PL': 0.0, 'NS': 0.0, 'NM': 0.0, 'NL': 0.0}
# fuzzified_input_3 = {'AZ': 0.0, 'PS': 0.0, 'PM': 1.0, 'PL': 0.0, 'NS': 0.0, 'NM': 0.0, 'NL': 0.0}
# activated_rules_3 = rule_activation_rule1(fuzzified_input_3)
# print(f"\nFor fuzzified_input_3: {fuzzified_input_3}")
# print(f"Activated output sets and strengths: {activated_rules_3}")
# Expected output: {'BB': 1.0}
# (Rule 2 'IF PM THEN BB' activated with 1.0)
