


def xor_int_str(val, str):
    return val ^ int(str, 10)


def swap(a, b):
    t = S[a]
    S[a] = S[b]
    S[b] = t


def rc4(key, data):
    # KSA
    j = 0
    for i in range(0, 256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        swap(S[i], S[j])

    # PRGA
    i = j = 0
    for k in range(0, len(data)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        swap(S[i], S[j])
        #val = xor_int_str(ord(data[k]), str(S[(S[i] + S[j]) % 256]))
        val = ord(data[k]) ^ S[(S[i] + S[j]) % 256]
        has.append(chr(val))

S = [i for i in range(0, 256)]
has = []
skey = "Topesp"
sdata = 'KÂ®~·'

rc4(skey, sdata)
print(has)
print("Criptografando")
for i in has:
    print(i, end="")

# has = []
# S = [i for i in range(0, 256)]
# sdata = "outra msg"
# rc4(skey, sdata)
#
# print("\nCriptografando")
# for i in has:
#     print(i, end="")


