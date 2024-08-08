def char_freq(char_arr):
    """
    Takes an array of character strings counts the frequency of each element

    Args:
        char_arr (arr): Array of strings of characters

    Returns:
        freq_dict (dict): Dictionary containing frequency of character strings
    """

# Set up an empty dictionary
    freq_dict = {}

# Loop through arrary 
    for char in char_arr:
        
        # Increment count if 
        if char in freq_dict.keys():
            freq_dict[char] += 1  
        else:
            freq_dict[char] = 1

    return freq_dict