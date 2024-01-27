import requests
from google.cloud import vision
from PIL import Image
from rembg import remove

def localize_objects_from_url(image_url):
    """Localize objects in an image from a URL.

    Args:
        image_url (str): The URL of the image.
    """
    client = vision.ImageAnnotatorClient()

    response = requests.get(image_url)
    image_content = response.content
    
    original_image = Image.open(BytesIO(image_content))
    
    image = vision.Image(content=image_content)


    objects = client.object_localization(image=image).localized_object_annotations

    image_dimension_dict = {}

    #print(objects)
    for object_ in objects:
        temp_image = original_image.copy()
        if object_.name == "Person":
            continue
        vertex_list = []
        for vertex in object_.bounding_poly.normalized_vertices:
            vertex_list.append((vertex.x, vertex.y))
        
        x_list = []
        y_list = []
        for vertex in vertex_list:
            x, y = vertex
            x_list.append(x)
            y_list.append(y)
        
        x_list = list(set(x_list))
        y_list = list(set(y_list))
        
        image_dimension_dict[object_.name] = (x_list, y_list)
        
    print(image_dimension_dict.keys())
    
    width = original_image.width
    height = original_image.height
    
    for object in image_dimension_dict.keys():
        x_list, y_list = image_dimension_dict[object]
        cut_box = (width * x_list[0], height * y_list[0], width * x_list[1], height * y_list[1])
        cut_image = original_image.crop(cut_box)
        cut_image.show()
    
    
  
  
 
# Specify the path to your image file
image_file_path = 'https://i.pinimg.com/564x/2e/b8/80/2eb880289f4bf98c3a0cc4a1f85923a6.jpg'
localize_objects_from_url(image_file_path)
