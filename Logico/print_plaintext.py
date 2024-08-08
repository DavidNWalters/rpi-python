def print_plaintext(char_arr,subs_dict,reverse=False):
    """
    Print the array of character strings with some formatting and substitutions
    
    Args:
        char_arr (arr): Array of strings of characters
        subs_dict (arr): Dictionary of substitutions to use
    """

    # Print headers
    print ('Guessed plaintext:')
    print ('==================')
    # Loop through arrary printing character followed by a space
    ichar = 0
    if reverse:
        char_arr = reversed(char_arr)
    for char in char_arr:
        # Substitute character if 
        if char in subs_dict.keys():
            if len(subs_dict[char]) > 0: 
#               print(colored('{:2s}'.format(subs_dict[char],end=' '),text_colours[icol],'on_black'))
                print(subs_dict[char],end=' ')
            else:
                print(char,end=' ')
        else:
            print(char,end=' ')
        if (ichar % 19) == 18:
            print() 
        ichar += 1
    # End with new line and a blank line
    print()
    print()
    return