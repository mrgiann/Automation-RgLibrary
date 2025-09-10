import os
import requests
from duckduckgo_search import DDGS
import webbrowser
import pyautogui
import time
import pyperclip

HEADERS = {"User-Agent": "Mozilla/5.0"}
output_dir = "descargas_juego"
os.makedirs(output_dir, exist_ok=True)

games = ["Left4Dead2", "Postal1"]  # Lista de juegos

def descargar_imagenes(ddgs, game, query, subfolder, formato="jpg"):
    print(f"Buscando imágenes para {game}...")
    results = ddgs.images(keywords=query, max_results=10, size="Medium", safesearch="off")
    
    dir_path = os.path.join(output_dir, game.replace(" ", "_"), subfolder)
    os.makedirs(dir_path, exist_ok=True)
    nombre_base = game.lower().replace(" ", "")
    
    for i, res in enumerate(results, start=1):
        url = res.get("image") or res.get("thumbnail")
        try:
            img = requests.get(url, headers=HEADERS, timeout=10).content
            file_path = os.path.join(dir_path, f"{nombre_base}{i}.{formato}")
            with open(file_path, "wb") as f:
                f.write(img)
            print(" Guardada →", file_path)
        except Exception as e:
            print(" Error al descargar:", url, e)

def procesar_juegos():
    with DDGS() as ddgs:
        for game in games:
            print(f"\n*** Procesando: {game} ***")
            base = os.path.join(output_dir, game.replace(" ", "_"))
            os.makedirs(base, exist_ok=True)

            # Descargar imágenes de gameplay y logo
            descargar_imagenes(ddgs, game, f"{game} gameplay", "gameplay")
            descargar_imagenes(ddgs, game, f"{game} logo", "logos", formato="webp")

            # Generar prompt para ChatGPT
            prompt = f"""Quiero que me des la información del juego "{game}" siguiendo exactamente este formato: {game.replace(' ','').lower()}: {{ title: "{game}", description: "Descripción breve del juego", requisitos: {{ SO: "Sistema operativo mínimo", Procesador: "Procesador mínimo", Memoria: "Memoria RAM mínima", Almacenamiento: "Espacio en disco requerido", Tarjeta: "Tarjeta gráfica mínima", }}, images: ["{game.replace(' ','').lower()}1.jpg", "{game.replace(' ','').lower()}2.jpg", "{game.replace(' ','').lower()}3.jpg"], downloadLinks: [{{ url: "#", label: "No disponible" }}], }}, Solo reemplaza cada campo con la información correspondiente del juego "{game}", sin explicaciones adicionales ni texto extra. La respuesta debe estar lista para copiar y pegar en código."""

            # Abrir ChatGPT si no está abierto
            webbrowser.open("https://chat.openai.com/")
            time.sleep(10)

            # Escribir prompt y enviar
            pyautogui.write(prompt, interval=0.005)
            time.sleep(0.3)
            pyautogui.press('enter')

            # Esperar respuesta
            time.sleep(25)

            # Seleccionar solo bloque de respuesta
            pyautogui.moveTo(500, 400)
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.keyDown('shift')
            for _ in range(30):  # Ajusta según la longitud
                pyautogui.press('down')
                time.sleep(0.05)
            pyautogui.keyUp('shift')

            # Copiar y limpiar
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.3)
            texto = pyperclip.paste()
            # Si hay script de pyautogui, eliminar primeras 2 líneas
            lineas = texto.splitlines()
            texto_limpio = "\n".join(lineas[2:]) if len(lineas) > 2 else texto

            # Guardar en .txt
            with open(os.path.join(base, f"{game.replace(' ','_')}_chatgpt.txt"), "w", encoding="utf-8") as f:
                f.write(texto_limpio)

            print(f"Guardado ChatGPT → {base}/{game.replace(' ','_')}_chatgpt.txt")

            # Recarga página
            pyautogui.hotkey('ctrl', 'r')
            time.sleep(12)

if __name__ == "__main__":
    procesar_juegos()
