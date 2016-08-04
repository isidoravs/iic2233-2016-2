import string
abc = string.ascii_lowercase
key = input()
encr = input()
clave = []
cifr = list(encr)
texto = []

k = -1
for i in range(len(cifr)):
    k += 1
    if k == len(key):
        k -= len(key)
    clave.append(key[k])

for j in range(len(cifr)):
            i_encr = abc.index(cifr[j])
            i_key = abc.index(clave[j])
            if i_encr >= i_key:
                texto.append(i_encr-i_key)
            else:
                texto.append(i_encr-i_key+26)

password = ""
for n in texto:
    password += abc[n]

print(password)