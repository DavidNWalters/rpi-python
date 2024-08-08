#!/usr/bin/python3

#main() function
def main():

    # import functions from other files
    from read_chars import read_chars
    from print_ciphertext import print_ciphertext
    from print_plaintext import print_plaintext
    from print_plaintext_colour import print_plaintext_colour
    from freq_analysis import freq_analysis
    from define_subs import define_subs
    # import standard functions
    import numpy as np

    # =======================================================
    # Read and count data
    # =======================================================

    # name of file containing ciphertext
    ctext_file = 'text'

    # read in text in pairs of characters into an array
    char_arr = read_chars(ctext_file,2)

    # create a list of unique character strings in order   
    char_list = sorted(np.unique(char_arr))

    # length of the array
    len_arr = len(char_arr)

    # =======================================================
    # Output data
    # =======================================================

    # print original text
    print_ciphertext(char_arr)

    # perform frequency analysis
    freq_analysis(char_arr)#,bars=False)

    subs_dict = define_subs(char_arr)

    # print guessed plaintext
    print_plaintext(char_arr,subs_dict)
    print_plaintext_colour(char_arr,subs_dict)


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()