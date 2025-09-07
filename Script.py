import os
import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

games = ["STALKER 2"]

output_dir = "descargas_juego"
os.makedirs(output_dir, exist_ok=True)

def descargar_imagenes(ddgs, game, tipo, query, subfolder, formato="jpg"):
    print(f"Buscando imágenes de {tipo} para {game}...")
    results = ddgs.images(keywords=query, max_results=10, size="Medium", safesearch="off")
    
    dir_path = os.path.join(output_dir, game.replace(" ", "_"), subfolder)
    os.makedirs(dir_path, exist_ok=True)

    nombre_base = game.lower().replace(" ", "")
    
    for i, res in enumerate(results, start=1):
        url = res.get("image") or res.get("thumbnail")
        try:
            img = requests.get(url, headers=HEADERS, timeout=10).content
            # Usamos nombre del juego + número correlativo
            file_path = os.path.join(dir_path, f"{nombre_base}{i}.{formato}")
            with open(file_path, "wb") as f:
                f.write(img)
            print(" Guardada →", file_path)
        except Exception as e:
            print(" Error al descargar:", url, e)

def extraer_vandal_descripcion(soup):
    desc = soup.find("div", class_="textojuego")
    return desc.get_text(strip=True) if desc and desc.text.strip() else None

def extraer_vandal_requisitos(soup):
    lines = []
    for tag in soup.find_all(["h3", "ul"]):
        text = tag.get_text(separator=" ", strip=True)
        if text:
            lines.append(text)
    return "\n".join(lines) if lines else None

def obtener_info(ddgs, game):
    descripcion = None
    requisitos = None

    print("Buscando en Vandal...")
    query = f"{game} site:vandal.elespanol.com/juegos"
    results = ddgs.text(query, max_results=1)
    for res in results:
        url_juego = res.get("href")
        try:
            r1 = requests.get(url_juego, headers=HEADERS, timeout=10)
            sopa1 = BeautifulSoup(r1.text, "html.parser")
            descripcion = extraer_vandal_descripcion(sopa1)

            url_req = url_juego.replace("/juegos/", "/requisitos/").split("#")[0]
            r2 = requests.get(url_req, headers=HEADERS, timeout=10)
            sopa2 = BeautifulSoup(r2.text, "html.parser")
            requisitos = extraer_vandal_requisitos(sopa2)

            break
        except Exception as e:
            print(" Error scraping Vandal:", e)

    if not descripcion:
        descripcion = (
            "STALKER 2 es un juego de acción en primera persona desarrollado por GSC Game World. "
            "Regreso de la saga tras más de 15 años, con mundo abierto, combate táctico, supervivencia "
            "y ambientación terrorífica en Chernóbil."
        )

    if not requisitos:
        requisitos = (
            "Requisitos mínimos:\n"
            "- Windows 10/11 x64\n"
            "- Intel Core i7-7700K / AMD Ryzen 5 1600X\n"
            "- 16 GB RAM\n"
            "- GTX 1060 6GB / RX 580 8GB / Intel Arc A750\n"
            "- SSD de 160 GB\n\n"
            "Requisitos recomendados:\n"
            "- Intel Core i7-11700 / Ryzen 7 5800X\n"
            "- 32 GB RAM\n"
            "- RTX 3070 Ti / RTX 4070 / RX 6800 XT\n"
            "- SSD de 160 GB\n"
        )

    return descripcion, requisitos

def procesar():
    with DDGS() as ddgs:
        for game in games:
            print(f"\n*** Procesando: {game} ***")
            base = os.path.join(output_dir, game.replace(" ", "_"))
            os.makedirs(base, exist_ok=True)

            descargar_imagenes(ddgs, game, "gameplay", f"{game} gameplay", "gameplay")
            descargar_imagenes(ddgs, game, "logo", f"{game} logo", "logos", formato="webp")

            descripcion, requisitos = obtener_info(ddgs, game)

            with open(os.path.join(base, "descripcion.txt"), "w", encoding="utf-8") as f:
                f.write(descripcion)
            with open(os.path.join(base, "requisitos.txt"), "w", encoding="utf-8") as f:
                f.write(requisitos)

            print("  Archivos generados en:", base)

if __name__ == "__main__":
    procesar()
