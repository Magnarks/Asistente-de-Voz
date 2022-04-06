import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib #para emails
import webbrowser as wb 
import os
import pyautogui
import psutil
import pyjokes
import python_weather
import asyncio
from googletrans import Translator
#import geocoder

engine= pyttsx3.init()
#Cambiar la voz
voz=engine.getProperty("voices")
engine.setProperty("voice", voz[0].id) #0 español 1 en ingles
#la velocidad de hablar
velocidadvoz= 120
engine.setProperty("rate", velocidadvoz)
def hablar(audio):
    engine.say(audio)
    engine.runAndWait()

def Hora():
    hora=datetime.datetime.now().strftime("%I:%M:%S")
    hablar("La hora es")
    hablar(hora)

def Fecha():
    año= int(datetime.datetime.now().year)
    mes= int(datetime.datetime.now().month) 
    dia= int(datetime.datetime.now().day)
    hablar("La fecha actual es")
    hablar(dia)
    hablar(mes)
    hablar(año)

def Saludo():
    hablar("Bienvenido de vuelta, como esta?")
    tiempo= datetime.datetime.now().hour
    if tiempo>=6 and tiempo <12:
        hablar("Buenos Dias")
    if tiempo>=12 and tiempo <18:
        hablar("Buenas Tardes")
    if tiempo>=18 and tiempo <24:
        hablar("Buenas Noches") 
    hablar("Tu asistente de Python al servicio, Como puedo ayudarte?")

def Enviaremail(para, contenido):
    servidor= smtplib.SMTP("smtp.gmail.com", 587)
    servidor.ehlo()
    servidor.starttls()
    servidor.login("*************", "***********")
    servidor.sendmail("*************", para, contenido)
    servidor.close()

#Funcion para reconocimiento de voz
def Escuchar():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.pause_threshold=1 #Tiempo para escuchar
        r.adjust_for_ambient_noise(source, duration=1) #hace el proceso mas rapido
        audior=r.listen(source)
    try:
        print("Reconociendo...")
        query=r.recognize_google(audior, language="es")
    except Exception as e:
        print(e)
        hablar("Repite de nuevo...")
        return "None"
    return query

def Pantallazo():
    imagen= pyautogui.screenshot()
    imagen.save("C:/Users/diego/Pictures/Python/Pantallazo.png")

def EstadoDelSistema():
    uso_de_cpu= str(psutil.cpu_percent())
    frequencia_de_cpu= str(psutil.cpu_freq())
    #uso_de_disco= str(psutil.disk_usage(path=))
    hablar("El uso de CPU es de" + uso_de_cpu)
    hablar("La frequencia del procesador es" + frequencia_de_cpu)
    #hablar("La uso del disco es de" + uso_de_disco)

def Chistes():
    hablar(pyjokes.get_joke(language="es"))

async def Clima():
    cliente=python_weather.Client(format=python_weather.METRIC) 
    hablar("Di tu ciudad")
    ciudad= Escuchar()
    clima= await cliente.find(ciudad)
    hablar(ciudad)
    hablar(str(clima.current.temperature) + "grados centigrados")
    #traducir= Translator()
    #traducir.translate(text=clima.current.sky_text, dest="es", src="en").text
    #hablar(traducir)
    for forecast in clima.forecasts:
        hablar(str(forecast.date) + str(forecast.sky_text) + str(forecast.temperature))
    await cliente.close()

#def Localizacion():
    #miUbicacion=geocoder.ip(location="me")
    #zonaCiudad=miUbicacion.city
    #zonaState=miUbicacion.state
    #zonaPais=miUbicacion.country
    #print(miUbicacion)
    #hablar(zonaCiudad + zonaState+ zonaPais)

#Funcion Principal
if __name__ == "__main__":
    Saludo()
    while True:
        query=Escuchar().lower()
        print(query)
        if "hora" in query:
            Hora()
        elif "fecha" in query:
            Fecha()
        elif "wikipedia" in query:
            hablar("Buscando...")
            wikipedia.set_lang("es")
            query=query.replace("wikipedia", "")
            resultado= wikipedia.summary(query, sentences=2)
            hablar(resultado)
        elif "enviar email" in query:
            try:
                hablar("¿Para quien es el correo? escriba el correo en el teclado")
                para= input()
                hablar(para)
                hablar("¿Que deberia decir el correo?")
                contenido= Escuchar()
                Enviaremail(para, contenido)
                hablar("El email ah sido enviado")
            except Exception as e:
                print(e)
                hablar("Imposible enviar el email")
        elif "ir a sitio web" in query:
            hablar("Que sitio deberia yo buscar")
            navegadorpath= "C:/Users/diego/AppData/Local/Programs/Opera GX/launcher.exe %s"
            busqueda= Escuchar().lower()
            print(busqueda)
            hablar(busqueda)
            wb.get(navegadorpath).open_new_tab(busqueda + ".com")
        elif "buscar en el navegador" in query:
            hablar("¿Que deberia yo buscar?")
            navegadorpath= "C:/Users/diego/AppData/Local/Programs/Opera GX/launcher.exe %s"
            busqueda= Escuchar()
            print(busqueda)
            hablar(busqueda)
            wb.get(navegadorpath).open_new_tab("https://www.google.com/search?client=opera-gx&q="+busqueda+"&sourceid=opera&ie=UTF-8&oe=UTF-8")
        elif "buscar canción" in query:
            hablar("¿Que canción deberia buscar?")
            navegadorpath= "C:/Users/diego/AppData/Local/Programs/Opera GX/launcher.exe %s"
            busqueda= Escuchar()
            print(busqueda)
            hablar(busqueda)
            wb.get(navegadorpath).open_new_tab("https://www.youtube.com/results?search_query="+busqueda)
        elif "cerrar sesión" in query:
            os.system("shutdown - 1")
        elif "reiniciar sistema" in query:
            os.system("shutdown /r /t 1")
        elif "apagar sistema" in query:
            os.system("shutdown /s /t 1")
        elif "canciones" in query:
            directorio_canciones= "C:/Users/diego/Music"
            canciones= os.listdir(directorio_canciones)
            for i in canciones:
                os.startfile(os.path.join(directorio_canciones, i))
        elif "cerrar sesion" in query:
            os.system("shutdown - 1")
        elif "guardar un recordatorio" in query:
            hablar("¿Que deberia yo recordar?")
            data= Escuchar()
            hablar("Tu me diste a recordar" + data)
            recordar= open("data.txd", "w")
            recordar.write(data)
            recordar.close()
        elif "recuérdame algo" in query:
            recordar= open("data.txd", "r")
            hablar("Me pediste que te recordara que " + recordar.read())
        elif "pantallazo" in query:
            Pantallazo()
            hablar("¡¡Pantallazo Listo!!")
        elif "estado del sistema" in query:
            EstadoDelSistema()
        elif "chiste" in query:
            Chistes()
        elif "clima" in query:
            bucle=asyncio.get_event_loop()
            bucle.run_until_complete(Clima())
        elif "lambón" in query:
            hablar("Alejando Meneses")
        #elif "ubicación" in query:
            #Localizacion()
        elif "apaga te" in query:
            hablar("Nos Vemos")
            quit()
        elif "apágate" in query:
            hablar("Adiós")
            quit()
        elif "apagar" in query:
            hablar("Chao")
            quit()

#hablar("Hola este es un Asistente en Python")
#Hora()
#Fecha()