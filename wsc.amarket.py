import requests
import json
import sys
from bs4 import BeautifulSoup

# Received params from node app
requestUrl = sys.argv[1]  # type URL
# url = "https://www.fidalga.com/collections/limpieza-del-hogar"
url = requestUrl

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://amarket.com.bo/",
    "Cookie": "my_cookie=12345",
}

# Realizamos la peticion a la web
req = requests.get(url, headers=headers)

# Comprobamos que la peticion nos devuelve un Status Code = 200
status_code = req.status_code
if status_code == 200:
    try:
        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text, "html.parser")
        # print("HTML >>>", html)

        # Obtenemos todos los elementos (divs) de la class -> PARENT (ITEMS)
        main_products = html.find_all("ul", {"class": "productgrid--items"})

        # Obtenemos todos los elementos (contenidos en div) de la class -> CHILD (ITEM)
        # product_container = main_products[0].find_all("div", class_="product-bottom")
        product_container = main_products[0].find_all("li", class_="productgrid--item")

        # Construimos el array formato json
        array_json = []

        # Recorremos todas las entradas para extraer el nombre y el precio
        for elements in product_container:
            name = elements.find("h2", class_="productitem--title")
            price = elements.find("div", class_="productitem--listview-price")

            # Imprimimos el nombre y el precio de la entrada
            # print(name.text.strip())
            # print(price.get_text(strip=True, separator="***"))

            # Creamos el json y lo agregamos al array
            product_json = {
                "name": name.text.strip(),  # strip() for remove \n..text..\n
                "price": price.get_text(strip=True, separator="***"),
            }
            array_json.append(product_json)

        # Mostramos el json
        print(json.dumps(array_json, indent=2))
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
