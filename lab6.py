#implementing an operating system in python
import json
class Folder():
    def __init__(self, name, location, children = {}):
        self.name = name
        self.location = location
        self.children=children
        self.size=self.computeSize()

    def computeSize(self):
        total=0
        for child in self.children:
            total+=child.size
        
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
    file_system[file_location].size += file_system[file_name].size
    return file_system

def mkdir(file_system, folder_name, folder_location):
    file_system[folder_name] = Folder(folder_name, folder_location, [])
    file_system[folder_location].children += [file_system[folder_name]]
    return file_system

def ls(file_system, folder_location):
    for child in file_system[folder_location].children:
        print(child.name)
    return file_system

def move(file_system, file_name, new_location):
    file_system[file_name].location.children.remove(file_system[file_name])
    file_system[file_name].location = new_location
    file_system[new_location].children += [file_system[file_name]]
    return file_system
#open file should return file object and all read write move and truncate done through this

def open_file(file_system, file_name):
    return file_system[file_name]

def read(file_object, num_bytes):
    return file_object.content[:num_bytes]

def write(file_object, content):
    file_object.content += content
    file_object.size += len(content)
    return file_object

def truncate(file_object, num_bytes):
    file_object.content = file_object.content[:num_bytes]
    file_object.size = num_bytes
    return file_object

def close(file_object):
    return file_object

def moveContentWithinFile(file_object, start, end, new_start):
    content = file_object.content[start:end]
    file_object.content = file_object.content[:start] + file_object.content[end:]
    file_object.content = file_object.content[:new_start] + content + file_object.content[new_start:]
    return file_object

def showMemoryMap(file_system):
    for key in file_system:
        print(key, file_system[key].size)
    return file_system

file_system=create_file_system()
mkdir(file_system, "folder1", "root")
mkdir(file_system, "folder2", "folder1")
create_file(file_system, "file1", "folder1", "hello")
create_file(file_system, "file2", "folder2", "hello")
create_file(file_system, "file3", "folder2", "hello")
ls(file_system, "folder1")
ls(file_system, "folder2")
file_object=open_file(file_system, "file1")
print(read(file_object, 3))
print(file_object.size)
write(file_object, "world")
print(file_object.size)
print(file_object.content)
truncate(file_object, 3)
print(file_object.size)
print(file_object.content)
close(file_object)
showMemoryMap(file_system)
