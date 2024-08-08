def print_plaintext_colour(char_arr,subs_dict,reverse=False):
    """
    Print the array of character strings with some formatting and substitutions
    
    Args:
        char_arr (arr): Array of strings of characters
        subs_dict (arr): Dictionary of substitutions to use
    """

    # import modules
    from colorama import init
    from termcolor import colored

    init()
    text_colours = ['blue','green']
    # Print headers
    print ('Guessed plaintext:')
    print ('==================')

    if reverse:
        char_arr = reversed(char_arr)
    # Loop through arrary printing character followed by a space
    icol = 0
    for char in char_arr:
        # Substitute character if 
        if char in subs_dict.keys():
            if len(subs_dict[char]) > 0: 
#               print(colored('{:2s}'.format(subs_dict[char],end=' '),text_colours[icol],'on_black'))
                print(colored(subs_dict[char],text_colours[icol]),end='')
            else:
                print(colored(char,text_colours[icol]),end='')
        else:
            print(colored(char,text_colours[icol]),end='')
        icol = ( icol + 1 ) % 2
    # End with new line and a blank line
    print()
    print()
    return