import pickle

# write list to binary file
def write_list(a_list):
    # store list in binary file so 'wb' mode
    with open('week29/packets.bin', 'wb') as fp:
        pickle.dump(a_list, fp)

# Read list to memory
def read_list():
    # for reading also binary mode is important
    with open('week29/packets.bin', 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list