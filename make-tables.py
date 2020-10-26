from __future__ import print_function

def mybin(i):
    return ("00000000"+bin(i)[2:])[-8:]

with open("tables.beebasm", "w") as f:
    parity_bit = 1 << 2
    print("    align &100")
    print(".parity_table")
    for i in range(256):
        parity = (1 + bin(i).count("1")) % 2
        print("    equb &%02x ; &%02x" % (parity * parity_bit, i))

    print("")
    print("    align &100")
    print(".flag_permutation_table")
    for i in range(256):
        # We just need to swap bits 1 and 6
        j = i & 0b10111101
        if i & (1 << 1) != 0:
            j |= 1 << 6
        if i & (1 << 6) != 0:
            j |= 1 << 1
        print("    equb %%%s ; &%02x %%%s" % (mybin(j), i, mybin(i)))

