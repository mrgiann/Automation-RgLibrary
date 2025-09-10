import webbrowser
import pyautogui
import time
import pyperclip

# Lista de juegos
keywords = ["CsGo 2"]  # Puedes agregar más nombres

# Abre ChatGPT
webbrowser.open("https://chat.openai.com/")
time.sleep(10)  # Espera a que cargue y te loguees

for keyword in keywords:
    # Prompt en una sola línea
    prompt = f"""Quiero que me des la información del juego "{keyword}" siguiendo exactamente este formato: {keyword}: {{ title: "Título del juego", description: "Descripción breve del juego", requisitos: {{ SO: "Sistema operativo mínimo", Procesador: "Procesador mínimo", Memoria: "Memoria RAM mínima", Almacenamiento: "Espacio en disco requerido", Tarjeta: "Tarjeta gráfica mínima", }}, images: ["{keyword}1.jpg", "{keyword}2.jpg", "{keyword}3.jpg"], downloadLinks: [{{ url: "#", label: "No disponible" }}], }}, Solo reemplaza cada campo con la información correspondiente del juego "{keyword}", sin explicaciones adicionales ni texto extra. No coloques nada en el campo de link de descarga solo deja un '#'. La respuesta debe estar lista para copiar y pegar en código."""

    # Escribe el prompt completo
    pyautogui.write(prompt, interval=0.005)
    time.sleep(0.3)
    pyautogui.press('enter')

    # Espera a que se genere la respuesta
    time.sleep(25)

    # Haz clic al inicio del bloque de respuesta (ajusta las coordenadas)
    pyautogui.moveTo(500, 400)
    pyautogui.click()
    time.sleep(0.2)

    # Mantén Shift y usa flecha abajo varias veces para seleccionar solo la respuesta
    pyautogui.keyDown('shift')
    for _ in range(30):  # Ajusta según la longitud de la respuesta
        pyautogui.press('down')
        time.sleep(0.05)
    pyautogui.keyUp('shift')

    # Copia al portapapeles
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)

    # Obtiene el texto del portapapeles
    texto = pyperclip.paste()

    # Borra las dos primeras líneas (que son tu script) antes de guardar
    lineas = texto.splitlines()
    texto_limpio = "\n".join(lineas[2:])  # Empieza desde la tercera línea

    # Guarda en un archivo
    with open(f"{keyword}_chatgpt.txt", "w", encoding="utf-8") as f:
        f.write(texto_limpio)

    print(f"Guardado: {keyword}_chatgpt.txt")

    # Recarga la página
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(12)
