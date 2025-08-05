import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_URL = "http://books.toscrape.com/"

def get_con_reintento(url, max_reintentos=5):
    for intento in range(max_reintentos):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except (requests.exceptions.RequestException, requests.exceptions.Timeout):
            time.sleep(2)
    return None

def obtener_autor_por_titulo(titulo):
    params = {
        'q': f'intitle:{titulo}',
        'key': API_KEY,
        'maxResults': 1
    }
    try:
        response = requests.get("https://www.googleapis.com/books/v1/volumes", params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                volume_info = data["items"][0]["volumeInfo"]
                autores = volume_info.get("authors", ["Desconocido"])
                return autores
    except:
        pass
    return ["Desconocido"]

def obtener_urls_categorias():
    response = get_con_reintento(BASE_URL + "index.html")
    if response is None:
        return []
    soup = BeautifulSoup(response.content, "html.parser")
    categorias = soup.select("div.side_categories ul li ul li a")
    urls = [BASE_URL + cat["href"] for cat in categorias]
    return urls

def obtener_urls_paginas_categoria(url_categoria):
    urls = []
    while True:
        urls.append(url_categoria)
        response = get_con_reintento(url_categoria)
        if response is None:
            break
        soup = BeautifulSoup(response.content, "html.parser")
        siguiente = soup.select_one("li.next > a")
        if siguiente:
            url_categoria = url_categoria.rsplit("/", 1)[0] + "/" + siguiente["href"]
        else:
            break
    return urls

def obtener_urls_libros_en_pagina(url_pagina):
    response = get_con_reintento(url_pagina)
    if response is None:
        return []
    soup = BeautifulSoup(response.content, "html.parser")
    libros = soup.select("article.product_pod h3 a")
    urls = [BASE_URL + "catalogue/" + libro["href"].replace("../../../", "") for libro in libros]
    return urls

def scrapear_detalles_libro(url_libro):
    response = get_con_reintento(url_libro)
    if response is None:
        return None
    soup = BeautifulSoup(response.content, "html.parser")
    titulo = soup.select_one("div.product_main h1").get_text(strip=True)
    precio = soup.select_one("p.price_color").get_text(strip=True)
    stock = soup.select_one("p.instock.availability").get_text(strip=True)
    clases = soup.select_one("p.star-rating")["class"]
    rating = [c for c in clases if c != "star-rating"][0]
    upc = soup.select_one("th:contains('UPC') + td")
    upc = upc.get_text(strip=True) if upc else "N/A"
    autores = obtener_autor_por_titulo(titulo)
    return {
        "titulo": titulo,
        "autores": autores,
        "precio": precio,
        "stock": stock,
        "rating": rating,
        "upc": upc,
        "url": url_libro
    }

def guardar_en_db(libros):
    conn = sqlite3.connect("libros.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price TEXT,
        stock TEXT,
        rating TEXT,
        upc TEXT UNIQUE,
        url TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS book_authors (
        book_id INTEGER,
        author_id INTEGER,
        PRIMARY KEY (book_id, author_id),
        FOREIGN KEY (book_id) REFERENCES books(id),
        FOREIGN KEY (author_id) REFERENCES authors(id)
    )""")
    for libro in libros:
        if libro is None:
            continue
        cursor.execute("""
            INSERT OR IGNORE INTO books (title, price, stock, rating, upc, url)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (libro["titulo"], libro["precio"], libro["stock"], libro["rating"], libro["upc"], libro["url"])
        )
        cursor.execute("SELECT id FROM books WHERE upc = ?", (libro["upc"],))
        libro_id = cursor.fetchone()[0]

        for autor in libro["autores"]:
            cursor.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)", (autor,))
            cursor.execute("SELECT id FROM authors WHERE name = ?", (autor,))
            autor_id = cursor.fetchone()[0]
            cursor.execute("INSERT OR IGNORE INTO book_authors (book_id, author_id) VALUES (?, ?)", (libro_id, autor_id))

    conn.commit()
    conn.close()

def main():
    categorias = obtener_urls_categorias()
    if not categorias:
        return
    libros_extraidos = []
    for url_categoria in categorias:
        paginas = obtener_urls_paginas_categoria(url_categoria)
        for url_pagina in paginas:
            libros_urls = obtener_urls_libros_en_pagina(url_pagina)
            for url_libro in libros_urls:
                detalles = scrapear_detalles_libro(url_libro)
                if detalles:
                    libros_extraidos.append(detalles)
                    print(f"Scrapeando: {detalles['titulo']} | Autores: {', '.join(detalles['autores'])}")
                    time.sleep(1)
    guardar_en_db(libros_extraidos)

if __name__ == "__main__":
    main()
