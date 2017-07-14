from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
import json
import os
from Script.models import IndexAddress
from django.http import JsonResponse
# Create your views here.

def index(request):
    print('hola')
    path =('/home/creatur/Documentos/python/django/ScriptBd/Address/Script/file.js')
    with open(path) as fd:
        leer = json.load(fd)
    conn = psycopg2.connect(database='Reservations1',user='usuario',password='root', host='localhost')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM "Index_address" """)
#    leer=json.loads(open('file.js').read())
    zone=leer['ZoneList']
    jsons=zone['Zone']
    queryAddres= IndexAddress.objects.all()
    # for datos in cur:
    #     data= IndexAddress()
    #     data.city=datos[1]
    #     data.code_oag=datos[2]
    #     data.description = datos[4]
    #     data.zip_code = datos[5]
    #     data.country = datos[6]
    #     data.latitude = datos[7]
    #     data.longitude = datos[8]
    #     data.operation_time = datos[9]
    #     data.save()

######################################################################################################################
##### Este bloque compara los datos de la BD y el archivo JSON ,toma los datos de ambos que coincidan por codigo IATA
    code=[]
    code2=[]
    lista=[]
    lista2=[]
    tamjson= len( jsons)
    for query in queryAddres:
        lista.append(query.city)
        lista2.append(query.code)
        for js in jsons:
            if '_IATA' in js:
                if len(js['_IATA']) > 2:
                    if js['_IATA'] == query.code_oag:
                        object={
                            "Name":str(js['Name'].upper()),
                            "IATA":query.code_oag,
                            "Code":str(js['_Code'])
                        }
                        code.append(object)
    tamcode=len(code)
###############################FIN DEL BLOQUE###########################################################################
######################################################################################################################

#################################################################################3#####################################
#######################################################################################################################
    # Bloque que genera diccionario con registros del JSOn sin codigo IATA que se registraran en la BD
    rest=tamjson-tamcode

    for js in jsons:
        if not '_IATA' in js:
            cont = 0
            city = str(js['Name'].upper())
            cont = len(code2)
            if cont < rest:
                object = {
                    "Name": str(js['Name'].upper()),
                    "Code": str(js['_Code'])
                }
                code2.append(object)

    print (len(code2))
################################################FIN DEL BLOQUE##############################################################
#########################################################################################################################

#############################################################################################################################33333
##############################################################################################################################
# Este boque regisstra los datos del primer diccionario , de los lugares no registrados en la BD pero coinciden con codigos IATA del Arcvhio JSON
    for data in queryAddres:
###########3 VARIABLE CONTADOR SIRVE PARA SABER SI LA CIUDAD O LUGAR EXISTE EN LA BD,SE RELLENA CONTANDO LAS VECES QUE APARECE EN LA BD
        contador=0
        for q in code:
            city=q['Name']
            contador=lista.count(city)
#            print 'contador'
#            print contador
############ EN ESTA SECCION SE REGISTRA EL CODE DEL JSON A LOS LUGARES DE LA BD TOMANDO COMO REFERENCIA DE COMPRACION EL CODIGO IATA
            if q['IATA'] == data.code_oag:
###########para SABER SI YA TIENE code REGISTRADO SE PREGUNTA SI EL VALOR ES == None
                if data.code==None:
                    dt = data.id
                    jss = q['Code']
                    update=IndexAddress.objects.get(id=dt)
                    update.code=jss
                    update.save()
############CUANDO LA CIUDAD NO ESTA REGISTRADA EL CONTADOR SERA ==0 LO QUE NOS DICE QUE DEBEMOS REGISTRARLA
            if contador == 0:
                #########cuando coincian se realiza el registro
                if data.code_oag == q['IATA']:
                    City= q['Name']
                    Oag= q['IATA']
                    Description=data.description
                    Zip=data.zip_code
                    Country=data.country
                    Latitude=data.latitude
                    Longitude=data.longitude
                    Operation=data.operation_time
                    conts=lista2.count(code)
                    Code=q['Code']
                    query=IndexAddress()
                    query.city=City
                    query.code_oag=Oag
                    query.description=Description
                    query.zip_code=Zip
                    query.country=Country
                    query.latitude=Latitude
                    query.longitude=Longitude
                    query.operation_time=Operation
                    query.code=Code
                    query.save()
####################################################################################################################
##########################FIN DEL BLOQUE############################################################################
######################################################################################################################

########################################################################################################################
#######################################################################################################################
#rEGISTRA EN L A BD LOS DATOS DEL SEGUNDO DICCIONARIO CREADO
    for datas in code2:
        conts=0
        code=datas['Code']
        conts=lista2.count(code)
#print conts
        if conts ==0:
            City=datas['Name']
            Code=datas['Code']
            query2=IndexAddress()
            query2.city=City
            query2.code=Code
            query2.save()
        else:
            print ('No')



    return HttpResponse("Hello, world. You're at the polls index.")
