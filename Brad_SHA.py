
def add_mod_2_32(x, y):
    return (x + y) % 0x100000000  

def string_to_ascii_binary(msg):
    ret = ""
    for char in msg:
        ret += str(bin(ord(char))[2:].zfill(8))
    return ret

def int_to_64bit_binary_string(value):
    return bin(value & 0xFFFFFFFFFFFFFFFF)[2:].zfill(64)

def shr(x,n):
    return (x>>n) & 0xFFFFFFFF

def rotl32(x,n):
    return ((x<<n) | (x>> (32-n))) & 0xFFFFFFFF

def rotr32(x,n):
    return ((x>>n) | (x<< (32-n))) & 0xFFFFFFFF

def Ch(x,y,z):
    return ((x & y) ^ (~x & z))

def Maj(x,y,z):
    return ((x & y) ^ (x & z) ^ (y & z))

def big_sigma0(x):
    return (rotr32(x,2) ^ rotr32(x,13) ^ rotr32(x,22))

def big_sigma1(x):
    return (rotr32(x,6) ^ rotr32(x,11) ^ rotr32(x,25))

def little_sigma0(x):
    return (rotr32(x,7) ^ rotr32(x,18) ^ shr(x,3))

def little_sigma1(x):
    return (rotr32(x,17) ^ rotr32(x,19) ^ shr(x,10))

def sha2_256(msg="",bitlength=None):
    if bitlength is None:
        bitlength = len(msg) * 8

    digest = ""

    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    M_block_list = []

    bin_msg = string_to_ascii_binary(msg)
    while (len(bin_msg) >=512):
        remain_msg = 


    # padding_msg = string_to_ascii_binary(msg) + "1" + (512-64-1-len(msg))*"0" +int_to_64bit_binary_string(bitlength)

    # print(padding_msg)



    return digest

if __name__ == '__main__':
    sha2_256("abc",bitlength = 24)