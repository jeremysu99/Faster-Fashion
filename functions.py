from google.cloud import vision

def comparelists(list1, list2)-> int:
    score = 0
    for item in list1.keys():
        if item in list2.keys():
            score += max([list1[item],list2[item]])
    return score

def detect_labels(path):
    """Detects labels in the file."""
    return_dict = dict()

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
  

    for label in labels:
        return_dict[label.description] =label.score

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    return return_dict

def are_rgb_values_similar(rgb1, rgb2, threshold=509):
    sum = 0
    for i in range(3):
        sum += abs(rgb1[i]-rgb2[i])
    if sum > threshold: return False
    return True

# # Example usage:
# rgb1 = (255, 0, 0)  # Red
# rgb2 = (250, 5, 5)  # Similar to Red with slight variation
# rgb3 = (0, 255, 0)  # Green

# print(are_rgb_values_similar(rgb1, rgb2))  # Output: True
# print(are_rgb_values_similar(rgb1, rgb3))  # Output: False

# x=detect_labels('/Users/ramajeenagala/downloads/images.jpeg')
# print(x)
# y=detect_labels('/Users/ramajeenagala/downloads/images1.jpeg')
# print(y)

# print(comparelists(x,y))