import struct


def swap32(i):
    return struct.unpack("<I", struct.pack(">I", i))[0]


message = "i love crypt"
message_dec = []

for i in range(len(message)):
    message_dec.append(ord(message[i]))

# append 1 and zeroes so len = 448 (mod 512)
message_dec.append(128)
padding = 56 - len(message_dec)
for i in range(padding):
    message_dec.append(0)
message_dec.append(len(message) * 8)

padding = 64 - len(message_dec)

for i in range(padding):
    message_dec.append(0)

counter = 0
M = []
for i in range(16):
    char1 = message_dec[counter]
    char2 = message_dec[counter + 1]
    char3 = message_dec[counter + 2]
    char4 = message_dec[counter + 3]
    chunk = (char1 << 24) + (char2 << 16) + (char3 << 8) + char4
    chunk = swap32(chunk)
    M.append(chunk)
    counter += 4


s = []
offset = [[7, 12, 17, 22], [5, 9, 14, 20], [4, 11, 16, 23], [6, 10, 15, 21]]

for i in range(4):
    for j in range(4):
        s.extend(offset[i])

K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
     0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
     0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
     0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
     0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
     0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
     0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
     0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
     0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
     0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
     0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
     0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
     0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
     0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
     0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
     0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391, ]

a0 = 0x67452301
b0 = 0xefcdab89
c0 = 0x98badcfe
d0 = 0x10325476

A = a0
B = b0
C = c0
D = d0


x = [0, 0, 0, 0]
# main function
for i in range(64):

    # roll A,B,C,D
    x[i % 4] = A
    x[(i + 1) % 4] = B
    x[(i + 2) % 4] = C
    x[(i + 3) % 4] = D

    if i < 16:
        F = (x[1] & x[2]) | ((~x[1]) & x[3])
        g = i % 16
    elif i < 32:
        F = (x[3] & x[1]) | ((~x[3]) & x[2])
        g = (5 * i + 1) % 16
    elif i < 48:
        F = x[1] ^ x[2] ^ x[3]
        g = (3 * i + 5) % 16
    else:
        F = x[2] ^ (x[1] | (~x[3]))
        g = (7 * i) % 16

    F += x[0] + K[i] + M[g]
    F = F % 2 ** 32

    # shift the bits
    F = (F << s[i]) % 2 ** 32 | (F >> (32 - s[i]) % 2 ** 32)

    x[0] = (x[1] + F) % 2 ** 32

    if i % 4 == 0:
        A = x[0]
    if i % 4 == 1:
        D = x[0]
    if i % 4 == 2:
        C = x[0]
    if i % 4 == 3:
        B = x[0]

# consolidate final register values
AA = (a0 + A) % 2 ** 32
BB = (b0 + B) % 2 ** 32
CC = (c0 + C) % 2 ** 32
DD = (d0 + D) % 2 ** 32

MD5 = format(swap32(AA), '08x') + format(swap32(BB), '08x') + format(swap32(CC), '08x') + format(swap32(DD), '08x')

print(MD5)

import hashlib  # for comparison purposes

m = hashlib.md5()
m.update(message.encode('utf-8'))
MD5_python = m.hexdigest()
print("message: " + message)
print("My MD5: " + MD5)
print("Library MD5: "+MD5_python)

if MD5 == MD5_python:
    print("Success!")
else:
    print("Failure!")
