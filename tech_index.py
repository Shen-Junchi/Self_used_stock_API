import numpy as np
import math
import pandas as pd

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

# Assuming the Fuzzification function from the previous step is available:
def Fuzzification(nature_log, fuzzi_parameter):
    """
    Fuzzification of the natural logarithm value based on Figure 1 definitions.
    (Implementation provided previously)
    """
    x = nature_log
    w = fuzzi_parameter
    if w <= 0:
        raise ValueError("fuzzi_parameter (w) must be positive")
    memberships = {}
    # AZ
    memberships['AZ'] = max(0.0, 1 - abs(x) / w) if -w <= x <= w else 0.0
    # PS
    memberships['PS'] = max(0.0, 1 - abs(x - w) / w) if 0 <= x <= 2 * w else 0.0
    # PM
    if w <= x < 2 * w: memberships['PM'] = (x - w) / w
    elif 2 * w <= x <= 3 * w: memberships['PM'] = (3 * w - x) / w
    else: memberships['PM'] = 0.0
    # PL
    if x < 2 * w: memberships['PL'] = 0.0
    elif 2 * w <= x <= 3 * w: memberships['PL'] = (x - 2 * w) / w
    else: memberships['PL'] = 1.0
    # NS
    memberships['NS'] = max(0.0, 1 - abs(x + w) / w) if -2 * w <= x <= 0 else 0.0
    # NM
    if -3 * w <= x < -2 * w: memberships['NM'] = (x + 3 * w) / w
    elif -2 * w <= x <= -w: memberships['NM'] = (-w - x) / w
    else: memberships['NM'] = 0.0
    # NL
    if x > -2 * w: memberships['NL'] = 0.0
    elif -3 * w <= x <= -2 * w: memberships['NL'] = (-2 * w - x) / w
    else: memberships['NL'] = 1.0
        
    for key in memberships:
        memberships[key] = max(0.0, min(1.0, memberships[key]))
    return memberships


def calculate_ed1(fuzzified_input):
    """
    Calculates the excess demand ed1 based on the fuzzified input and 
    Rule 1 Group using the formula from Eq. 8.

    :param fuzzified_input: A dictionary containing the membership degrees 
                             for input fuzzy sets (output of Fuzzification).
                             Example: {'AZ': 0.7, 'PS': 0.3, ...}
    :return: The calculated excess demand value ed1.
    """

    # Define the input fuzzy sets A_i (indices match paper's formula)
    # A1=PS, A2=PM, A3=PL, A4=NS, A5=NM, A6=NL, A7=AZ
    input_sets_ordered = ['PS', 'PM', 'PL', 'NS', 'NM', 'NL', 'AZ']

    # Define the corresponding output centers c_i based on Rule 1 Group and Fig. 2
    # Rule 1: IF PS THEN BS (c1=0.1)
    # Rule 2: IF PM THEN BB (c2=0.4)
    # Rule 3: IF PL THEN SM (c3=-0.2)
    # Rule 4: IF NS THEN SS (c4=-0.1)
    # Rule 5: IF NM THEN SB (c5=-0.4)
    # Rule 6: IF NL THEN BM (c6=0.2)
    # Rule 7: IF AZ THEN N  (c7=0)
    output_centers = {
        'PS': 0.1,  # c1
        'PM': 0.4,  # c2
        'PL': -0.2, # c3
        'NS': -0.1, # c4
        'NM': -0.4, # c5
        'NL': 0.2,  # c6
        'AZ': 0.0   # c7
    }

    numerator = 0.0
    denominator = 0.0

    # Calculate sum(ci * mu_Ai(x)) and sum(mu_Ai(x))
    for input_set_label in input_sets_ordered:
        # Get membership degree mu_Ai(x) from the input dictionary
        mu = fuzzified_input.get(input_set_label, 0.0) # Default to 0 if key not found
        
        # Get corresponding output center ci
        c = output_centers.get(input_set_label) 
        
        if mu > 0 and c is not None: # Only consider activated rules
            numerator += c * mu
            denominator += mu

    # Calculate ed1 using Eq. 8
    if denominator == 0:
        # If no rules were activated (e.g., input was way outside defined ranges)
        # return 0 (Neutral)
        ed1 = 0.0
    else:
        ed1 = numerator / denominator

    return ed1

# --- Example Usage ---

# Define parameters
# w_param = 0.01

# Example 1: Input from previous step
# x_input_1 = 0.003 
# fuzzified_1 = Fuzzification(x_input_1, w_param) 
# # fuzzified_1 is approx {'AZ': 0.7, 'PS': 0.3, 'PM': 0.0, 'PL': 0.0, 'NS': 0.0, 'NM': 0.0, 'NL': 0.0}
# ed1_output_1 = calculate_ed1(fuzzified_1)
# print(f"For x = {x_input_1}:")
# print(f"  Fuzzified Input: {fuzzified_1}")
# print(f"  Calculated ed1: {ed1_output_1:.4f}") # Expected: 0.0300
