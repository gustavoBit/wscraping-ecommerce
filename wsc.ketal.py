import requests
import json
import sys
from bs4 import BeautifulSoup

# Received params from node app
requestUrl = sys.argv[1]  # type URL
# url = "https://www.ketal.com.bo/aseo-y-limpieza"
url = requestUrl
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.ketal.com.bo/",
    "Cookie": "my_cookie=12345",
}
# Realizamos la petición a la web
req = requests.get(url, headers=headers)

# Comprobamos que la petición nos devuelve un Status Code = 200
status_code = req.status_code
if status_code == 200:
    try:
        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text, "html.parser")

        # Obtenemos todos los elementos de la class "main-products"
        main_products = html.find_all("div", class_="main-products")

        # Obtenemos todos los elementos div con  class "caption"
        captions = main_products[0].find_all("div", class_="caption")

        # Construimos el array formato json
        array_json = []

        # Recorremos todas las captions y obtenemos los elementos con class "name" y "price"

        for caption in captions:
            name = caption.find("div", class_="name")
            price = caption.find("div", class_="price")

            # Imprimimos por pantalla el atributo de texto de cada elemento
            # print(name.text)
            # print(price.text)

            # Creamos el json y lo agregamos al array
            product_json = {
                "name": name.text,
                "price": price.get_text(strip=True, separator="***"),
            }

            array_json.append(product_json)

        # Mostramos el array por pantalla
        print(json.dumps(array_json, indent=2))
    except Exception as e:
        # Capturar cualquier error
        sys.stderr.write(
            str(
                f"Se ha producido un error: {e}. Es probable que esté intentando consultar una página diferente (scraping no desarrollado), y la obtención de datos no ha sido completada. Si desea agregar el soporte/funcionalidad de esta página, ¡contáctenos! "
            )
        )
        sys.exit(1)

# Si el Status Code es diferente de 200, informamos que hubo un error
else:
    sys.stderr.write(
        str(
            f"Error al realizar la petición a la web, esta intentando consultar datos de la página: {url}; si reviso y funciona en un navegador, contáctenos!"
        )
    )
    sys.exit(1)
