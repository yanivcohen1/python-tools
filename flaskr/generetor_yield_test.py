def rev_str(my_str):
    length = len(my_str)
    # reverse the string  range(start_from_end, to 0 include, in step -1)
    for i in range(length - 1, -1, -1): 
        yield my_str[i]


# For loop to reverse the string
for char in rev_str("hello"):
    print(char)