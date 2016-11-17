# AC15
import requests
import re
import json

url_inicio = "http://ac15-aaossa.rhcloud.com/inicio"

response1 = requests.request("GET", url_inicio)
work1 = response1.json()['lista']

string1 = ""

for email in work1:
    if re.match('[a-z]*[\.]?[a-z]*@gmail.(com|arg|cn|eu|cl)', email):
        string1 += email

to_send1 = json.dumps({"username": "isidoravs", "string": string1})
post1 = requests.post(url_inicio,
                      headers={"content-Type": "application/json"},
                      data=to_send1)
url2 = post1.json()['url']

response2 = requests.request("GET", url2)
work2 = response2.json()['lista']

string2 = ""
for word in work2:
    if re.match('[bB][bastianBASTIAN]*[nN]', word):
        string2 += word

to_send2 = json.dumps({"username": "isidoravs", "string": string2})
post2 = requests.post(url2,
                      headers={"content-Type": "application/json"},
                      data=to_send2)

url3 = post2.json()['url']
response3 = requests.request("GET", url3)
work3 = response3.json()['lista']

string3 = ""
for word in work3:
    if re.match('el[+](terrible|odiado|amado\?)x1[0]*', word):
        string3 += word

    elif re.match('el[+](terrible|odiado|amado\?)[jJ][eE][fF][eE]x1[0]*', word):
        string3 += word

    elif re.match('el[+](terrible|odiado|amado\?)[bB][oO][sS][sS]x1[0]*', word):
        string3 += word

to_send3 = json.dumps({"username": "isidoravs", "string": string3})
post3 = requests.post(url3,
                      headers={"content-Type": "application/json"},
                      data=to_send3)

url4 = post3.json()['url']
response4 = requests.request("GET", url4)
work4 = response4.json()['lista']

string4 = ""
for word in work4:
    if re.search('tarealograda', word) is not None:
        string4 += word

to_send4 = json.dumps({"username": "isidoravs", "string": string4})
post4 = requests.post(url4,
                      headers={"content-Type": "application/json"},
                      data=to_send4)

password = post4.json()['password']

access = json.dumps({"password": password, "username": "isidoravs"})

ayudantes_post = requests.post("http://ac15-aaossa.rhcloud.com/ayudantes",
                               headers = {"content-Type": "application/json"},
                               data = access)

alumnos_post = requests.post("http://ac15-aaossa.rhcloud.com/alumnos",
                             headers = {"content-Type": "application/json"},
                             data = access)

def check_ayudante(ide):
    post = requests.post("http://ac15-aaossa.rhcloud.com/ayudantes/{}".format(str(ide)),
                         headers={"content-Type": "application/json"},
                         data=access)
    return post.json()

def check_alumno(ide):
    post = requests.post("http://ac15-aaossa.rhcloud.com/alumnos/{}".format(str(ide)),
                         headers={"content-Type": "application/json"},
                         data=access)
    return post.json()


# CONSULTAS

alumnos = alumnos_post.json()
my_id = alumnos['isidoravs']

# ayudantes que me aman
ayudantes = ayudantes_post.json()

print(" 1. Numero de alumnos amados por cada ayudante que me ama")

recorregir = 300
recorregir_ayudante = ""

for nombre in ayudantes:
    ayudante_id = ayudantes[nombre]

    # reviso si me ama
    relacion_ayud = check_ayudante(ayudante_id)
    if relacion_ayud[my_id] == 1:
        amados = relacion_ayud.count(1)

        if amados < recorregir:
            recorregir = amados
            recorregir_ayudante = nombre

        print("{}, {}".format(nombre, str(amados)))

print("Debo ir a recorregir con {}".format(recorregir_ayudante))  # alguno de los dos

print("\n 3. Ayudante mas tierno")

mas_tierno = ""
ama_a = 0

for (nombre_ayud, id_ayud) in ayudantes.items():
    relaciones = check_ayudante(id_ayud)
    amor = relaciones.count(1)
    if amor > ama_a:
        ama_a = amor
        mas_tierno = nombre_ayud

print("  > {}".format(mas_tierno))

print("\n 2. Ayudante mas odiado")

mas_odiado = ""
odio = 0

for (nombre_ayud, id_ayud) in ayudantes.items():
    odian_ayud = 0
    for (nombre_alum, id_alum) in alumnos.items():
        relacion_alum = check_alumno(id_alum)
        if relacion_alum[id_ayud] == 2:
            odian_ayud += 1

    if odian_ayud > odio:
        odio = odian_ayud
        print("Ya no es {}, es {}".format(mas_odiado, nombre_ayud))
        mas_odiado = nombre_ayud

print("  > {}".format(mas_odiado))


print("\n 3. Ayudante mas tierno")

mas_tierno = ""
ama_a = 0

for (nombre_ayud, id_ayud) in ayudantes.items():
    relaciones = check_ayudante(id_ayud)
    amor = relaciones.count(1)
    if amor > ama_a:
        ama_a = amor
        mas_tierno = nombre_ayud

print("  > {}".format(mas_tierno))




