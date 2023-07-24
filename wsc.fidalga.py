import math
import requests
import json
import sys
from bs4 import BeautifulSoup


# WIP: FUNCTIONS SECTION
def getMaxPages(text_total, page_size):
    # print("text_total", text_total) // "e.g.: Mostrando 1 - 24 de 187 total"
    # Buscamos el índice del primer dígito del número
    indice_inicio = text_total.find("de") + 3
    # Buscamos el índice del último dígito del número
    indice_fin = text_total.find("total") - 1
    # Extraemos el número como una subcadena del texto original
    total = int(text_total[indice_inicio : indice_fin + 1])
    max_pages = total / int(page_size)
    # print("max_pages", max_pages, round(max_pages), math.ceil(max_pages))
    return math.ceil(max_pages)


# WIP: SCRAPING
# Received params from node app
requestUrl = sys.argv[1]  # type URL
# url = "https://www.fidalga.com/collections/limpieza-del-hogar"
url = requestUrl

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.fidalga.com/",
    "Cookie": "my_cookie=12345",
}

# Realizamos la peticion inicial para obtener los datos que necesitamos
req = requests.get(url, headers=headers)

# Comprobamos que la peticion nos devuelve un Status Code = 200
status_code = req.status_code
if status_code == 200:
    try:
        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text, "html.parser")
        # print("HTML >>>", html)

        # Obtenemos la cantidad total de paginas
        # "li", {"class": "pagination__page pagination__page--total"}
        pages_text = html.find("div", {"class": "page-total"}).text
        page_size = html.find("span", attrs={"name": "paginateBy"}).get_text(strip=True)

        max_pages = getMaxPages(pages_text, page_size)
        # print("max_pages", max_pages)

        # Inicializamos el array final
        final_data = []

        for page in range(1, max_pages + 1):
            # Construimos la URL de cada pagina
            page_url = f"{url}?page={page}"

            # Hacemos request simulando scroll
            req = requests.get(page_url, headers=headers)

            html = BeautifulSoup(req.text, "html.parser")

            # Obtenemos los productos
            # products = html.find_all("div", {"class": "product-bottom"})
            # Obtenemos todos los elementos (divs) de la class -> PARENT (ITEMS)
            main_products = html.find_all("div", {"class": "product-collection"})
            # Obtenemos todos los elementos (contenidos en div) de la class -> CHILD (ITEM)
            # product_container = main_products[0].find_all("div", class_="product-bottom")
            product_container = main_products[0].find_all("div", class_="inner-top")
            # print("product_container", product_container)
            # Extraemos datos
            # Recorremos todas las entradas para extraer el nombre y el precio
            for elements in product_container:
                name = elements.find("a", class_="product-title").text.strip()
                price = elements.find("div", class_="price-box")

                # Imprimimos el nombre y el precio de la entrada
                # print(name.text.strip())
                # print(price.get_text(strip=True, separator="***"))

                # Creamos el json y lo agregamos al array
                product_json = {
                    "name": name,  # strip() for remove \n..text..\n
                    "price": price.get_text(strip=True, separator="***"),
                }
                final_data.append(product_json)

        # Mostramos resultados finales en json
        print(json.dumps(final_data, indent=2))

    except Exception as e:
        # Capturar cualquier error
        sys.stderr.write(
            str(
                f"Se ha producido un error: {e}. Es probable que esté intentando consultar una página diferente (scraping no desarrollado), y la obtención de datos no ha sido completada. Si desea agregar el soporte/funcionalidad de esta página, ¡contáctenos! "
            )
        )
        sys.exit(1)

else:
    sys.stderr.write(
        str(
            f"Error al realizar la petición a la web, esta intentando consultar datos de la página: {url}; si reviso y funciona en un navegador, contáctenos!"
        )
    )
    sys.exit(1)
