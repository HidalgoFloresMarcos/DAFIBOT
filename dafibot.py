## -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import urllib.request
import os
import pywhatkit
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import unicodedata
from dotenv import load_dotenv

def cargar_variables_entorno():
    load_dotenv()
    return os.getenv("FACEBOOK_USER"), os.getenv("FACEBOOK_PASSWORD")

def iniciar_sesion_facebook(usuario, contraseña):
    driver.maximize_window()
    driver.get("https://www.facebook.com/login/")
    time.sleep(3)
    username = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
    password = driver.find_element(By.CSS_SELECTOR, "input[name='pass']")
    username.clear()
    password.clear()
    username.send_keys(usuario)
    password.send_keys(contraseña)
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(4)

def obtener_texto_publicacion():
    post_text_element = driver.find_element(By.CSS_SELECTOR, 'div[dir="auto"][style*="text-align: start;"]')
    if post_text_element:
        return post_text_element.text
    else:
        print("No se encontró el texto de la publicación.")
        return ""

def obtener_url_imagen():
    images = driver.find_elements(By.CSS_SELECTOR, 'img')
    if images:
        return images[0].get_attribute('src')
    else:
        print("No se encontraron imágenes.")
        return ""

def descargar_imagen(url, save_path):
    image_data = urllib.request.urlopen(url).read()
    with open(save_path, 'wb') as handler:
        handler.write(image_data)
    print(f"Imagen descargada como '{save_path}'")

def cerrar_navegador():
    driver.quit()

def eliminar_tildes(texto):
    texto = texto.replace("ñ", "#").replace("Ñ", "%")
    return unicodedata.normalize("NFKD", texto)\
                     .encode("ascii", "ignore").decode("ascii")\
                     .replace("#", "ñ").replace("%", "Ñ")

# Cargar variables de entorno
FACEBOOK_USER, FACEBOOK_PASSWORD = cargar_variables_entorno()

# Configuración del WebDriver
service = Service('chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Iniciar sesión en Facebook
iniciar_sesion_facebook("josuehf40@gmail.com", "foraneos123")

# Navegar a la URL de búsqueda en Facebook
driver.get("https://www.facebook.com/profile/100068575179258/search?q=MENU&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9In0%3D")
time.sleep(2)

# Obtener el texto de la publicación
publicacion = obtener_texto_publicacion()
print(f"Texto de la publicación: {publicacion}")

# Obtener la URL de la primera imagen
image_url = obtener_url_imagen()
print(f"URL imagen: {image_url}")

# Ruta de guardado para la imagen
save_path = 'menu.jpg'

# Descargar la imagen
descargar_imagen(image_url, save_path)

# Cerrar el WebDriver
cerrar_navegador()

# Eliminar tildes del texto de la publicación
publicacion_sin_tildes = eliminar_tildes(publicacion)

# Envío del menú a WhatsApp
pywhatkit.sendwhats_image("Ketg30yLNJi2QwMfpYfXDd", "menu.jpg", f"Hola soy DAFIBOT y:\n {publicacion_sin_tildes}", close_time=3)
