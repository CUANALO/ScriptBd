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
    path =('/home/cecilio/Documentos/Django/Address/Script/file.js')
    with open(path) as fd:
        leer = json.load(fd)
    conn = psycopg2.connect(database='data',user='postgres',password='root', host='localhost')
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
    #
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
    rest=tamjson-tamcode

#for query in cur2:

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

    for data in queryAddres:
#    print 'count a 0'
        contador=0
        for q in code:
            city=q['Name']
            contador=lista.count(city)
#            print 'contador'
#            print contador
            if q['IATA'] == data.code_oag:
                if data.code==None:
                    print ('registrando codigo')
                    dt = data.id
                    jss = q['Code']
                    update=IndexAddress.objects.get(id=dt)
                    update.code=jss
                    update.save()
            if contador == 0:
                if data.code_oag == q['IATA']:
                    print ('no existe se registra')
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
