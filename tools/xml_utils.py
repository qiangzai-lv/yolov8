import xml.etree.ElementTree as ET


class ObjectItem:
    def __init__(self):
        self.points = []
        self.possible_result = ""


class Annotation:
    def __init__(self):
        self.filename = ""
        self.objects = []


def convert_possible_result_to_index(possible_result):
    plane_class = (
        "A220", "A330", "A320/321", "Boeing737-800", "Boeing787", "ARJ21", "other", "Boeing737", "Boeing747",
        "Boeing777",
        "Boeing787", "C919", "A220", "A321", "A330", "A350", "ARJ21", "other-airplane")
    class_mapping = {class_name: index for index, class_name in enumerate(plane_class)}
    return class_mapping[possible_result]


def parse_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    annotation = Annotation()
    for child in root:
        if child.tag == 'source' or child.tag == 'research' or child.tag == 'size':
            for sub_child in child:
                if sub_child.tag == 'filename':
                    annotation.filename = sub_child.text

        elif child.tag == 'objects':
            for obj in child.findall('object'):
                obj_item = ObjectItem()
                for sub_child in obj:
                    if sub_child.tag == 'points':
                        for point in sub_child.findall('point')[:4]:
                            x, y = point.text.split(',')
                            obj_item.points.append(int(float(x)))
                            obj_item.points.append(int(float(y)))
                    elif sub_child.tag == 'possibleresult':
                        obj_item.possible_result = convert_possible_result_to_index(sub_child.find('name').text)
                annotation.objects.append(obj_item)

    return annotation
