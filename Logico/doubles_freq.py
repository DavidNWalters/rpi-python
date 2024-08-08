def doubles_freq(char_arr):
    """
    Takes an array of character strings counts the frequency of doubles

    Args:
        char_arr (arr): Array of strings of characters

    Returns:
        doubles_dict (dict): Dictionary containing frequency of double character strings
    """

# Set up an empty dictionary
    doubles_dict = {}

    last_char = ''
# Loop through arrary 
    for char in char_arr:
        if char == last_char:
            # Increment count if it was a double
            if char in doubles_dict.keys():
                doubles_dict[char] += 1  
            else:
                doubles_dict[char] = 1
        last_char = char
    return doubles_dict