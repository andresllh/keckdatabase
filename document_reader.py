'''
Author Valentin Becerra
'''
class document_data(object):


    def __init__(self, project_name):
        self.project = project_name
        self.materal = ""
        self.model_tip = ""
        self.support_material = ""
        self.support_tip = ""
        self.rotate_x = 0
        self.rotate_y = 0
        self.rotate_z = 0
        self.scale = 0
        self.scale_x = 0
        self.scale_y = 0
        self.scale_z = 0
        self.units = 0



    def description(self):
        # this method will be used to store the data in the right format
        print ""


def filereader():
    document_data = document_data()
    filename = "file.txt"
    file = open(filename, "r")

    for line in file:
        if line[14:26] == "modelerMaterial":
            document_data.materal = line[16:]
        elif line[14:21] == "modelTip":
            document_data.model_tip = line[16:]
        elif line[14:28] == "suppportMaterial":
            document_data.support_material = line[30:]
        elif line[14:23] == "supportTip":
            document_data.support_tip = line[25:]
        elif line[14:23] == "stlRotateX":
            document_data.rotate_x = line[25:]
        elif line[14:23] == "stlRotateY":
            document_data.rotate_y = line[25:]
        elif line[14:23] == "stlRotateZ":
            document_data.rotate_z = line[25:]
        elif line[14:21] == "stlScale":
            document_data.scale = line[23:]
        elif line[14:22] == "stlScaleX":
            document_data.scale_x = line[24:]
        elif line[14:22] == "stlScaleY":
            document_data.scale_y = line[24:]
        elif line[14:22] == "stlScaleZ":
            document_data.scale_z = line[24:]
        elif line[14:21] == "stlUnits":
            document_data.units = line[26:]
