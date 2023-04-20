
import requests
from bs4 import BeautifulSoup

url = "https://www.ketal.com.bo/aseo-y-limpieza"

# Realizamos la petición a la web
req = requests.get(url)

# Comprobamos que la petición nos devuelve un Status Code = 200
status_code = req.status_code
if status_code == 200:

  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
  html = BeautifulSoup(req.text, "html.parser")

  # Obtenemos todos los elementos de la class "main-products"
  main_products = html.find_all("div", class_="main-products")

  # Obtenemos todos los elementos div con  class "caption"
  captions = main_products[0].find_all("div", class_="caption")

  # Construimos el array formato json
  array_json = []
  
  # Recorremos todas las captions y obtenemos los elementos con class "name" y "price"
  with open('ketal_scraping4.csv', 'w') as f:
    for caption in captions:
        name = caption.find("div", class_="name")
        price = caption.find("div", class_="price")

        # Imprimimos por pantalla el atributo de texto de cada elemento
        print(name.text)
        print(price.text)
        
        # Creamos el json y lo agregamos al array
        product_json = {
          'name_product': name.text,
          "price_product": price.get_text(strip=True, separator='***')
        }

        array_json.append(product_json)
         # Mostramos el array por pantalla
        print(array_json)
        
        # export .csv
        # f.write(name.get_text(strip=True, separator='***') + price.get_text(strip=True, separator='***') + '\n' )
        
# Si el Status Code es diferente de 200, informamos que hubo un error
else:
    print("Error al realizar la petición a la web")
    
    