def define_subs(char_arr):
    """
    Define a dictionary of potential substitutions 

    Args:
        char_arr (arr): Array of strings of characters

    Output:
        subs_dict (dictionary): A dictionary of guessed substitutions
    """

    subs_dict = {}


    subs_dict["01"] = "A"
    subs_dict["02"] = "M"
    subs_dict["03"] = "S"
    subs_dict["05"] = "C"
    subs_dict["07"] = "G"
    subs_dict["08"] = "R"
    subs_dict["13"] = "P"
    subs_dict["14"] = "E"
    subs_dict["15"] = "B"
    subs_dict["21"] = "O"
    subs_dict["29"] = "F"
    subs_dict["31"] = "V"
    subs_dict["35"] = "N"
    subs_dict["37"] = "H"
    subs_dict["45"] = "I"
    subs_dict["48"] = "L"
    subs_dict["53"] = "U"
    subs_dict["60"] = "T"
    subs_dict["79"] = "D"

    
    return subs_dict