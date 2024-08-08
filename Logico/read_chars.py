def read_chars(filename,n):
    """
    Reads in characters from a file and saves them into an array

    Args:
        filename (str): The name of the input file.
        n (int): The number of characters to read and save in the array

    Returns:
        char_arr (arr): Array of strings of n characters
    """

# open file as read only
    file = open(filename,'r') 

    # initialise an array to hold the characters
    char_arr = []

# read in text n characters at a time
    while 1:
     
        # read in n characters and append the array
        char = file.read(n)          
        if not char: 
            break
         
        char_arr.append(char)
 
    file.close()

    return char_arr