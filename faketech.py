
import xml.etree.ElementTree as ET
import os

AOM_PATH = "/mnt/c/Program Files (x86)/Steam/steamapps/common/Age of Mythology/"
if not os.path.exists(AOM_PATH):
    AOM_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Age of Mythology\\"
AOM_VERSION = "2.8"

class ProtoUnitDatabase:
    def __init__(self):
        proto_unit_path = AOM_PATH + os.sep + "data" + os.sep + "proto" + AOM_VERSION + ".xml"
        tree = ET.parse(proto_unit_path)
        self.tree = tree
        self.units = tree.findall("unit")
        # Language path for translating displayid
        en_lang_path = AOM_PATH + os.sep + "Language" + os.sep + "en" + os.sep + "en-language.txt"
        with open(en_lang_path, 'r', encoding="utf-16-le") as f:
            lang_lines = f.readlines()
        self.display_map = {}
        for line in lang_lines:
            tokens = line.split()
            if len(tokens) > 1:
                if tokens[0].isdigit():
                    display_id = int(tokens[0])
                    text = line[len(tokens[0]):].strip()
                    self.display_map[display_id] = text[1:-1]
                
    
    def get_name(self, id):
        for unit in self.units:
            if int(unit.attrib["id"]) == id:
                return unit.attrib["name"]

    def get_displayname(self, id):
        for unit in self.units:
            if int(unit.attrib["id"]) == id:
                display_id = int(unit.find("displaynameid").text)
                return self.display_map[display_id]
    
class Pos:

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def four(self):
        return str(self.x1) + " " + str(self.y1) +  " " + str(self.x2) + " " + str(self.y2)

database = ProtoUnitDatabase()

class Row:
    def __init__(self, archaic, classical, heroic, mythic):
        self.archaic = archaic
        self.classical = classical
        self.heroic = heroic
        self.mythic = mythic

# this should also be modified to draw onto the image at relevant pos
# in addition, do a lookup for the category via database
def gen_one(god, tech, pos):
    return '\t<gadget name="FakeTechTree-' + god + '-TechNode-' + tech + "\"" +\
        ' type="button" size1024="' + pos.four()+'">' + tech+"</gadget>" +'\n'

def gen_era(god_name, techs, x_start, x_width, x_gap, y_start, y_height):
    gadget = ""
    for tech_name in techs:
        pos = Pos(x_start, y_start, x_start + x_width, y_start + y_height)
        gadget += gen_one(god_name, tech_name, pos)
        x_start += x_gap
    return gadget
        


def get_god_gadget(god_name, gods, rows):
    gadget = ""
    gadget += '<gadget name="FakeTechTree-'+god_name+'" type="gadget" size1024="0 0 1024 768" hidden="">' + '\n'
    # First, let's align our rows.
    col1 = 24
    col2 = 244
    col3 =  557
    col4 = 845
    y1 = 255
    y_height = 34
    y_gap = 54
    x_gap = 41
    x_width = 32

    for god in gods:
        pass
    
    for row in rows:
        x_start = col1
        y_start = y1
        # y2 = 
        gadget += gen_era(god_name, row.archaic, x_start, x_width, x_gap, y_start, y_height)
        
        x_start = col2
        gadget += gen_era(god_name, row.classical, x_start, x_width, x_gap, y_start, y_height)

        x_start = col3
        gadget += gen_era(god_name, row.heroic, x_start, x_width, x_gap, y_start, y_height)

        x_start = col4
        gadget += gen_era(god_name, row.mythic, x_start, x_width, x_gap, y_start, y_height)

        gadget+= '\n'
        y_start += y_gap

    return gadget

LOKI_NAME = "Loki"
tcRow = Row(["Settlement Level 1", "Villager", "Dwarf", "Ulfsark", "Ox Cart"],
            ["Masons"],
            ["Architects", "Fortify Town Center"],
            [])


oxRow = Row(["Ox Cart", "Husbandry", "Hunting Dogs", "Hand Axe", "Pickaxe"],
            ["Plow", "Bow Saw", "Shaft Mine"], 
            ["Irrigation", "Carpenters", "Quarry"],
            ["Flood Control"])


gad = get_god_gadget(LOKI_NAME, [], [tcRow, oxRow])
print(gad)