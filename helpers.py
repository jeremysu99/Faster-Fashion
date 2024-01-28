import requests
from google.cloud import vision
from PIL import Image
from io import BytesIO
import base64
import psycopg2

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
    
    return object_dominant_colors

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
    
    return detect_objects_and_dominant_colors_from_bytes(image_content)

def are_rgb_values_similar(rgb1, rgb2, threshold=30):
    sum = 0
    for i in range(3):
        sum += abs(rgb1[i]-rgb2[i])
    print(sum)
    if sum > threshold: return False
    return True

def get_similar_clothes(image_url):
    colors = detect_objects_and_dominant_colors_from_url(image_url)
    connection = psycopg2.connect(
    user="jeremysu",
    password="jeremy509",
    host="169.234.107.183",
    port=5432,
    database="jeremysu"
    )
    cursor = connection.cursor()
    query = "SELECT * FROM scrapedclothes3;"
    cursor.execute(query)
    rows = cursor.fetchall()
    matches = []
    print(rows[0])
    for row in rows:
        if row[7] == list(colors.keys())[0]:
            print(row[7], list(colors.keys())[0])
            if are_rgb_values_similar(row[6],list(colors.values())[0]):
                print(row[0])
                matches.append(row)
    
    print(matches)
    print(len(matches))

    
 
# Specify the path to your image file
input()
image_file_path = 'https://lp2.hm.com/hmgoepprod?set=source[/03/36/033621a23b78d8dfe82bb478573936a467454e80.jpg],origin[dam],category[men_jeans_loose],type[DESCRIPTIVESTILLLIFE],res[m],hmver[2]&call=url[file:/product/style]'
# detect_objects_and_dominant_colors_from_url(image_file_path)
# get_labels_from_url(image_file_path)
get_similar_clothes(image_file_path)
    
#detect_objects_and_dominant_colors_from_url('https://lp2.hm.com/hmgoepprod?set=source[/d5/3b/d53bd8cf50a08abf90f4ee31ec9ad60099cab5f8.jpg],origin[dam],category[],type[DESCRIPTIVESTILLLIFE],res[m],hmver[2]&call=url[file:/product/style]')
