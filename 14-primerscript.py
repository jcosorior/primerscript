import os
import requests
import random
import string

# Generar una cadena aleatoria para agregar a los nombres de archivo
def random_string(length=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# URL de la API
url = 'https://api.waifu.im/search'

# Carpeta de destino para guardar las imágenes
folder_path = '/home/kuma/Desktop/curso-python/scriptimagenes'
os.makedirs(folder_path, exist_ok=True)

# Número mínimo de imágenes que deseas descargar
min_images = 10

# Realizar solicitudes a la API hasta obtener al menos 10 imágenes
downloaded_images = 0
while downloaded_images < min_images:
    # Parámetros para obtener hasta 10 imágenes aleatorias por solicitud
    params = {
        'limit': min_images - downloaded_images
    }

    # Realizar la solicitud a la API
    response = requests.get(url, params=params)

    # Verificar el estado de la solicitud
    if response.status_code == 200:
        # Convertir la respuesta a formato JSON
        data = response.json()
        
        # Descargar y guardar las imágenes
        for index, image_info in enumerate(data['images']):
            image_url = image_info['url']
            random_name = random_string()
            image_name = f'image_{random_name}.jpg'  # Nombre de la imagen
            image_path = os.path.join(folder_path, image_name)  # Ruta completa de la imagen
            
            # Descargar la imagen
            image_response = requests.get(image_url)
            
            # Guardar la imagen en la carpeta especificada
            with open(image_path, 'wb') as f:
                f.write(image_response.content)
            
            print(f'Imagen {downloaded_images + 1} descargada y guardada como {image_name}')
            print(f'URL de la imagen: {image_url}')  # Imprimir la URL de la imagen
            
            downloaded_images += 1
            if downloaded_images >= min_images:
                break
    else:
        print('La solicitud falló con el código de estado:', response.status_code)
        break
