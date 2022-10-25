#implementing an operating system in python
import json


class Folder():
    def __init__(self, name, location, children = []):
        self.name = name
        self.location = location
        self.children=children
        self.size=self.computeSize()

    def computeSize(self):
        total=0
        for child in self.children:
            print(child.size)
        return total
    def __str__(self):
        return self.name + " " + self.location + " " + str(self.size) + " " + str(self.children)
    
class File():
    def __init__(self, name, location, content):
        self.name = name
        self.location = location
        self.size = len(content) #assuming 1 character per byte
        self.content=content
    def __str__(self):
        return self.name + " " + self.location + " " + self.size + " " + self.content
    def length(self):
        return self.size
        

#using a dictionary to store pointer to files
def create_file_system():
    file_system = {}
    file_system["root"] = Folder("root", "root", [])
    return file_system

def create_file(file_system, file_name, file_location , file_content):
    file_system[file_name] = File(file_name, file_location, file_content)
    file_system[file_name].size = len(file_content)
    file_system[file_location].children += [file_system[file_name]]
    return file_system

def mkdir(file_system, folder_name, folder_location):
    file_system[folder_name] = Folder(folder_name, folder_location, [])
    file_system[folder_location].children += [folder_name]
    return file_system

file_system = create_file_system()
file_system = create_file(file_system, "file1", "root", "Hello world")
file_system = create_file(file_system, "file2", "root", "Hi")
file_system=mkdir(file_system, "folder1", "root")
file_system=create_file(file_system, "file3", "folder1", "Third file")
# json.dumps(file_system)
print (file_system['root'])
