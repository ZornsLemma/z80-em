from __future__ import print_function

hybrid_flag_s = 1 << 7
hybrid_flag_p = 1 << 6
hybrid_flag_h = 1 << 4
hybrid_flag_n = 1 << 2
hybrid_flag_z = 1 << 1
hybrid_flag_c = 1 << 0

def mybin(i):
    return ("00000000"+bin(i)[2:])[-8:]

print("; AUTO-GENERATED, DO NOT EDIT! Edit make-tables.py instead.")
print("")

print("    align &100")
print(".parity_table")
for i in range(256):
    parity = (1 + bin(i).count("1")) % 2
    print("    equb &%02x ; &%02x" % (parity * hybrid_flag_p, i))

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
    j |=      0b00101000 # unused flag bits are always set TODO: That's not true, see z80-documented.pdf, but not worrying about it for now
    print("    equb %%%s ; &%02x %%%s" % (mybin(j), i, mybin(i)))

print("")
print("    align &100")
print(".dec_flag_table")
for new_val in range(256):
    flags = hybrid_flag_n
    if new_val == 0:
        flags |= hybrid_flag_z
    if new_val >= 0x80:
        flags |= hybrid_flag_s
    if new_val == 0x7f:
        flags |= hybrid_flag_p
    old_val = (new_val + 1) & 0xff
    # SFTODO? if (((i + 1) & 8) == 0) and ((i & 8) != 0):
    if ((old_val & 8) == 0) and (((old_val - 1) & 8) != 0):
        flags |= hybrid_flag_h
    print("    equb %%%s ; &%02x %%%s" % (mybin(flags), new_val, mybin(new_val)))

print("")
print("    align &100")
print(".inc_flag_table")
for new_val in range(256):
    flags = 0
    if new_val == 0:
        flags |= hybrid_flag_z
    if new_val >= 0x80:
        flags |= hybrid_flag_s
    if new_val == 0x80:
        flags |= hybrid_flag_p
    # SFTODO? if (i & 16) != ((i - 1) & 16):
    # SFTODO? if ((((i - 1) & 0x0f) + 1) & 0x10) != 0:
    old_val = (new_val - 1) & 0xff
    if (((old_val & 0xf) + 1) & 0x10) != 0:
        flags |= hybrid_flag_h
    print("    equb %%%s ; &%02x %%%s" % (mybin(flags), new_val, mybin(new_val)))
