import requests
from google.cloud import vision
from PIL import Image
from io import BytesIO
import base64
    
def detect_objects_and_dominant_colors_from_bytes(image_data):
    """Localize objects in an image from a Bytes.

    Args:
        image_data (str): The image as a data
        
    Returns dictionary of {Object : (R,G,B)}
    """
    # initializes vision API
    client = vision.ImageAnnotatorClient()
    
    original_image = Image.open(BytesIO(image_data))
    
    image = vision.Image(content=image_data)
    objects = client.object_localization(image=image).localized_object_annotations

    image_dimension_dict = {}

    # takes each object detected and appends its name and area detected IF IT IS CLOTHES
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
        
    width = original_image.width
    height = original_image.height
    
    object_dominant_colors = {}
    
    # makes cropped temporary images from original image
    for object in image_dimension_dict.keys():
        x_list, y_list = image_dimension_dict[object]
        cut_box = (width * x_list[0], height * y_list[0], width * x_list[1], height * y_list[1])
        cut_image = original_image.crop(cut_box)
        with BytesIO() as byte_stream:
            cut_image.save(byte_stream, format="JPEG")
            image_bytes = byte_stream.getvalue()
            
        #color detection stuff
        image = vision.Image(content=image_bytes)
        response = client.image_properties(image=image)
        props = response.image_properties_annotation
        dominant_color = None
        for color in props.dominant_colors.colors:
            if dominant_color == None or color.pixel_fraction > dominant_color:
                object_dominant_colors[object] = (color.color.red, color.color.green, color.color.blue)
        
    print(object_dominant_colors)

def detect_objects_and_dominant_colors_from_url(image_url):
    """Localize objects in an image from a URL.

    Args:
        image_url (str): The URL of the image.
        
    Returns dictionary of {Object : (R,G,B)}
    """
    # initializes vision API
    client = vision.ImageAnnotatorClient()

    response = requests.get(image_url)
    image_content = response.content
    
    detect_objects_and_dominant_colors_from_bytes(image_content)
    
 
# Specify the path to your image file
image_file_path = 'https://img.freepik.com/premium-photo/close-up-black-t-shirt-isolated_57262-41.jpg'
#detect_objects_and_dominant_colors_from_url(image_file_path)
