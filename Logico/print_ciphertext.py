def print_ciphertext(char_arr):
    """
    Print the array of character strings with some formatting
    
    Args:
        char_arr (arr): Array of strings of characters
    """

# Print headers
    print ('Ciphertext:')
    print ('===========')
# Loop through arrary printing character followed by a space
    ichar = 0
    for char in char_arr:
        print(char,end=' ')
        if (ichar % 19) == 18:
            print()
        ichar += 1
# End with new line and a blank line
    print()
    print()
    return