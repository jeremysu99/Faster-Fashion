import requests
from google.cloud import vision


def localize_objects_from_url(image_url):
   """Localize objects in an image from a URL.


   Args:
       image_url (str): The URL of the image.
   """
   client = vision.ImageAnnotatorClient()


   response = requests.get(image_url)
   image_content = response.content


   image = vision.Image(content=image_content)


   objects = client.object_localization(image=image).localized_object_annotations


   image_dimension_dict = {}
  
   #print(objects)
   for object_ in objects:
       if object_.name == "Person":
           continue
       vertex_list = []
       for vertex in object_.bounding_poly.normalized_vertices:
           vertex_list.append((vertex.x, vertex.y))
       image_dimension_dict[object_.name] = vertex_list
  
  
 
# Specify the path to your image file
image_file_path = 'https://i.pinimg.com/564x/2e/b8/80/2eb880289f4bf98c3a0cc4a1f85923a6.jpg'
localize_objects_from_url(image_file_path)
