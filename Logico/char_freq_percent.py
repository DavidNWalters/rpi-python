def char_freq_percent(freq_dict,char_list,char_arr):
    """
    Takes a dictionary of frequency analysis and calculates these as percent of the total

    Args:
        freq_dict (dict): Dictionary containing frequency of character strings
        char_list (list): List of the keys of the dictionary
        char_arr (array): Full list of characters
          
    Returns:
        freq_dict_percent (dict): Dictionary containing percentage frequency of character strings

    """

# Set up output dictionary as a copy of the input dictionary
    freq_dict_percent = {}

    for char in char_list:
        
        freq_dict_percent[char] = ( float(freq_dict[char]) / len(char_arr) ) * 100

    return freq_dict_percent