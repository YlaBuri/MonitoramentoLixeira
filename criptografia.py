S = [i for i in range(0, 256)]
has = []


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

has2=[]
S2 = [i for i in range(0, 256)]
def rc4Des(key, data):
    # KSA
    j = 0
    for i in range(0, 256):
        j = (j + S2[i] + ord(key[i % len(key)])) % 256
        swap(S2[i], S2[j])

    # PRGA
    i = j = 0
    for k in range(0, len(data)):
        i = (i + 1) % 256
        j = (j + S2[i]) % 256
        swap(S2[i], S2[j])
        print("s[(s[i] + s[j])- ", S2[(S[i] + S2[j]) % 256])
        print("s[i]- ",S2[i])
        print("data- ", ord(data[k]))
        #val = xor_int_str(ord(data[k]), str(S[(S[i] + S[j]) % 256]))
        val = ord(data[k]) ^ S2[(S[i] + S2[j]) % 256]
        has2.append(chr(val))
        print("has-", has2[k])


skey = "Andre"
sdata = "Essa msg sera criptografada"

rc4(skey, sdata)

print("Criptografando")
for i in has:
    print(i, end="")


print("\ndescriptografando")
rc4Des(skey, has)
for i in has2:
    print(i, end="")