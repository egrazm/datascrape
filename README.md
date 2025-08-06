# 📚 Book Data Scraper & Analyzer

Este proyecto consiste en un scraping completo del sitio [Books to Scrape](https://books.toscrape.com/), su almacenamiento en una base de datos relacional SQLite, modelado con relaciones `muchos a muchos` entre libros y autores, y análisis exploratorio mediante consultas SQL y notebooks en Jupyter.

---

## 📦 Estructura del proyecto

Database/
├── scraper.py # Script de scraping web (requests + BeautifulSoup)
├── libros.db # Base de datos SQLite relacional
├── libros_exportados.csv # CSV con los libros scrapeados
├── order.sql # Script de creación e inserción SQL (DDL + DML)
├── analisis_libros.ipynb # Notebook de análisis exploratorio SQL
├── querys_practica_libros.ipynb # Consultas avanzadas de práctica
├── .gitignore # Archivos y carpetas excluidos del repo
├── README.md # Este archivo
├── key.env # ⚠️ No subir a GitHub: contiene tu API key (ignorada por Git)
└── .venv/ # Entorno virtual (excluido del repo)



---

## 🚀 ¿Qué hace este proyecto?

- Scrapea **todos los libros** del sitio Books to Scrape.
- Almacena datos como: título, categoría, precio, disponibilidad, calificación, etc.
- Exporta los datos a un archivo `.csv`.
- Crea una base de datos relacional con `libros`, `categorias`, `autores`, y relaciones entre ellos.
- Realiza consultas SQL complejas usando `JOIN`, `subconsultas`, `funciones de ventana`, y más.
- Genera análisis estadísticos y visualizaciones desde Jupyter Notebooks.

---

## 🛠️ Tecnologías utilizadas

- **Python**: lenguaje principal.
- **BeautifulSoup4** y **requests**: scraping.
- **SQLite**: base de datos relacional embebida.
- **SQL**: lenguaje para creación de tablas y consultas.
- **Pandas**: manipulación de datos y exportación CSV.
- **Jupyter Notebook**: entorno interactivo de análisis.
- **Git**: control de versiones.

---

## ⚙️ Requisitos

- Python 3.9 o superior
- Entorno virtual (`.venv`) activado
- Instalar dependencias con:

```bash
pip install -r requirements.txt
▶️ Cómo ejecutar
Activar entorno virtual:

# En Windows
source .venv/Scripts/activate
Ejecutar el scraper:

python scraper.py
Crear la base de datos:


sqlite3 libros.db < order.sql
Abrir los notebooks para análisis exploratorio:


jupyter notebook
📂 Archivos sensibles
Asegúrate de que el archivo key.env esté en el .gitignore y no se suba nunca al repositorio remoto, ya que contiene claves privadas.

📈 Consultas SQL interesantes
¿Cuáles son las 5 categorías con mayor cantidad de libros?

¿Qué autores tienen más de un libro publicado?

¿Cuál es el precio promedio por categoría?

¿Cuál es el libro más caro disponible?
