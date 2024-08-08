def freq_analysis(char_arr,bars=True):
    """
    Perform frequency analysis on an array of strings and 

    Args:
        char_arr (arr): Array of strings of characters

    Opt:
        bars (logical): Whether or not to plot bar graph
    """

    # import functions from other files
    from char_freq import char_freq
    from char_freq_percent import char_freq_percent
    from doubles_freq import doubles_freq
    # import standard functions
    import numpy as np
    import matplotlib.pyplot as plt

    # create a list of unique character strings in order   
    char_list = sorted(np.unique(char_arr))

    # Count frequency of characters (and percentage)
    freq_dict = char_freq(char_arr)
    pcnt_dict = char_freq_percent(freq_dict,char_list,char_arr)
    len_dict = len(freq_dict)

    # Count doubles
    doubles_dict = doubles_freq(char_arr)

    # Print summaries to screen
    print ('Number of unique sets of characters: ', len_dict)

    print ('Frequency distribution:')
    print ('=======================')
    i = 0 
    while i < len_dict :
        char = char_list[i]

        print ('{:5s} : {:5d} : {:4.1f}%'.format(char,int(freq_dict[char]),pcnt_dict[char]))

        i += 1
    print()

    print ('Doubles distribution:')
    print ('=====================')
    i = 0 
    while i < len_dict :
        char = char_list[i]
        if char in doubles_dict.keys():
            print ('{:5s} : {:5d}'.format(char,int(doubles_dict[char])))

        i += 1
    print()


    if bars:
        # plot a bar graph of %ages
        D = pcnt_dict
        plt.bar(range(len(D)), list(D.values()), align='center')
        plt.xticks(range(len(D)), list(D.keys()))
        plt.show()

    return