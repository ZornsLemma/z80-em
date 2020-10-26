from __future__ import print_function

def mybin(i):
    return ("00000000"+bin(i)[2:])[-8:]

with open("tables.beebasm", "w") as f:
    parity_bit = 1 << 6
    print("    align &100")
    print(".parity_table")
    for i in range(256):
        parity = (1 + bin(i).count("1")) % 2
        print("    equb &%02x ; &%02x" % (parity * parity_bit, i))

    print("")
    print("    align &100")
    print(".z80_to_hybrid_flag_table")
    for i in range(256):
        j  =  i & 0b10010001
        j |= (i & 0b01000000) >> 5
        j |= (i & 0b00000100) << 4
        j |= (i & 0b00000010) << 1
        print("    equb %%%s ; &%02x %%%s" % (mybin(j), i, mybin(i)))

    print("")
    print("    align &100")
    print(".hybrid_to_z80_flag_table")
    for i in range(256):
        j  =  i & 0b10010001
        j |= (i & 0b01000000) >> 4
        j |= (i & 0b00000100) >> 1
        j |= (i & 0b00000010) << 5
        j |=      0b00101000 # unused flag bits are always set
        print("    equb %%%s ; &%02x %%%s" % (mybin(j), i, mybin(i)))
