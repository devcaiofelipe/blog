from PIL import Image
import os
from django.conf import settings


#Função para redimensionar a imagem antes de salvar no banco dados
def resize_image(image_name, new_width):
    image_path = os.path.join(settings.MEDIA_ROOT, image_name)
    image = Image.open(image_path)
    width, height = image.size
    new_height = round((new_width * height) / width)

    if width <= new_width:
        image.close()
        return

    new_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    new_image.save(image_path, optimize=True, quality=60)
    new_image.close()