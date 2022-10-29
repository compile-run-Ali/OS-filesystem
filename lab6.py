# implementing an operating system in python
from inspect import getblock
import json


class Folder():
    def __init__(self, name, location, children={}):
        self.name = name
        self.location = location
        self.children = children
        self.block_numbers = []

    def get_size(self):
        size = 0
        for child in self.children:
            size += self.children[child].get_size()
        return size
    #getter for blocks
    def get_blocks(self):
        return self.block_numbers

    def __str__(self):
        return self.name + " " + self.location + " " + str(self.get_size()) + " " + str(self.children)+ " " + str(self.block_numbers)


class File():
    def __init__(self, name, location, content):
        self.name = name
        self.location = location
        self.size = len(content)  # assuming 1 character per byte
        self.content = content
        self.block_numbers = []

    def get_size(self):
        return self.size

    def __str__(self):
        return self.name + " " + self.location + " " + str(self.size) + " " + self.content+ " " + str(self.block_numbers)

#making a disk class with blocks and random access
class Disk():
    def __init__(self, size, block_size):
        self.size = size
        self.block_size = block_size
        self.blocks = []
        self.free_blocks = []
        self.used_blocks = []
        self.block_count = int(size / block_size)
        for i in range(self.block_count):
            self.blocks.append(None)
            self.free_blocks.append(i)

    def get_free_block(self):
        if (len(self.free_blocks) == 0):
            return None
        else:
            return self.free_blocks.pop(0)

    def get_used_block(self, block_number):
        if (block_number in self.used_blocks):
            return self.blocks[block_number]
        else:
            return None

    #write in first available free block according to size of file, if file size is greater than block number, we store in multiple blocks
    def write(self, file):
        if (file.get_size() > self.block_size):
            #if file size greater, we store in multiple blocks
            #we need to check if we have enough free blocks to store the file
            if (file.get_size() > len(self.free_blocks) * self.block_size):
                return False
            else:
                block_numbers = []
                for i in range(int(file.get_size() / self.block_size)):
                    block_number = self.get_free_block()
                    block_numbers.append(block_number)
                    self.used_blocks.append(block_number)
                    self.blocks[block_number] = file
                file.block_numbers = block_numbers
                return True
        else:
            #if file size is less than block size, we store in one block
            #we need to check if we have a free block to store the file
            if (len(self.free_blocks) == 0):
                return False
            else:
                block_number = self.get_free_block()
                file.block_number = block_number
                self.used_blocks.append(block_number)
                self.blocks[block_number] = file
                return True
        #return a block number for the file
        
            

    def read(self, block_number):
        if (block_number in self.used_blocks):
            return self.blocks[block_number]
        else:
            return None


    def delete(self, file, block_number):
        print(block_number)
        #check list of block numbers in used
        i=-1
        while(block_number[i] in self.used_blocks):
            #remove from used blocks
            self.used_blocks.remove(block_number[i])
            #add to free blocks
            self.free_blocks.append(block_number[i])
            #remove from blocks
            self.blocks[block_number[i]] = None
            i+=1
        return True


    def print_blocks(self):
        for i in range(len(self.blocks)):
            print("Block " + str(i) + ": " + str(self.blocks[i]))
        

    def __str__(self):
        return "Disk size: " + str(self.size) + " Block size: " + str(self.block_size) + " Block count: " + str(self.block_count) + " Free blocks: " + str(self.free_blocks) + " Used blocks: " + str(self.used_blocks)

def create_file_system(memory):
    file_system = {}
    file_system["root"] = Folder("root", "/", {})
    #storing in memory too
    memory.write(file_system["root"])
    return file_system

# take path for folder and then go into the children and store in that directory
def mkdir(file_system, folder_name, folder_location,originalFolderLocation,memory):
    path = folder_location.split("/")
    if (len(path) == 1):
        print("creating folder in",file_system[folder_location].name)
        file_system[folder_location].children[folder_name] = Folder(folder_name, originalFolderLocation, {})
        #storing in memory too according to data
        memory.write(file_system[folder_location].children[folder_name])

    else:
        # remove index 0 from path
        temp=path.pop(0)
        new_folder_location = "/".join(path)
        mkdir(file_system[temp].children, folder_name, new_folder_location, originalFolderLocation)
    return file_system

def delete_file(file_system, file_name, file_location,memory):
    path = file_location.split("/")
    if (len(path) == 1):
        print("deleting file",file_name,"from",file_system[file_location].name)
        memory.delete(file_name,file_system[file_location].children[file_name].block_numbers)
        del file_system[file_location].children[file_name]
        #deleting from memory too according to name
    else:
        # remove index 0 from path
        temp=path.pop(0)
        temp_location = "/".join(path)
        delete_file(file_system[temp].children, file_name, temp_location,memory)
    return file_system

def create_file(file_system, file_name, file_location,originalFolderLocation, content,memory):
    path = file_location.split("/")
    if (len(path) == 1):
        print("creating file in",file_system[file_location].name)
        file_system[file_location].children[file_name] = File(file_name, originalFolderLocation, content)
        #storing in memory too according to data
        memory.write(file_system[file_location].children[file_name])
    else:
        # remove index 0 from path
        temp=path.pop(0)
        new_file_location = "/".join(path)
        create_file(file_system[temp].children, file_name, new_file_location,originalFolderLocation, content,memory)
    return file_system


def ls(file_system, folder_location):
    path = folder_location.split("/")
    if (len(path) == 1):
        print("listing folders and files in",file_system[folder_location].name)
        for child in file_system[folder_location].children:
            print(child)
    else:
        # remove index 0 from path
        temp=path.pop(0)
        new_folder_location = "/".join(path)
        ls(file_system[temp].children, new_folder_location)
    return file_system

def copy_file(file_system,originalFileSystem, file_name, file_location, new_file_location):
    path = file_location.split("/")
    if (len(path) == 1):
        #moving file to last index of path2
        print("copying file",file_name,"from",file_system[file_location].name,"to",new_file_location)
        create_file(originalFileSystem, file_name, new_file_location, new_file_location, file_system[file_location].children[file_name].content)
        #copying to another location in memory
        memory.write(originalFileSystem[new_file_location].children[file_name])
    else:
        # remove index 0 from path
        temp=path.pop(0)
        temp_location = "/".join(path)
        copy_file(file_system[temp].children,originalFileSystem, file_name, temp_location, new_file_location)
    return file_system

def move_file(file_system,original_file_system, file_name, file_location, new_file_location,memory):
    path = file_location.split("/")
    if (len(path) == 1):
        #moving file to last index of path2
        print("moving file",file_name,"from",file_system[file_location].name,"to",new_file_location)
        create_file(original_file_system, file_name, new_file_location, new_file_location, file_system[file_location].children[file_name].content,memory)
        delete_file(original_file_system, file_name, file_location,memory)
    else:
        # remove index 0 from path
        temp=path.pop(0)
        temp_location = "/".join(path)
        move_file(file_system[temp].children,original_file_system, file_name, temp_location, new_file_location)
    return file_system
# open file should return file object and all read write move and truncate done through this

def open_file(file_system, file_name, file_location):
    path = file_location.split("/")
    if (len(path) == 1):
        return file_system[file_location].children[file_name]
    else:
        # remove index 0 from path
        temp=path.pop(0)
        temp_location = "/".join(path)
        return open_file(file_system[temp].children, file_name, temp_location)
    
#read whole file
def read(file_object):
    return file_object.content

def write(file_object, start, end, content):
    file_object.content = file_object.content[:start] + content + file_object.content[end:]

    return file_object

def truncate(file_object, size):
    file_object.content = file_object.content[:size]
    return file_object

def close_file(file_object):
    return file_object

def moveContentWithinFile(file_object, start, end, new_start):
    content = file_object.content[start:end]
    file_object.content = file_object.content[:start] + file_object.content[end:]
    file_object.content = file_object.content[:new_start] + content + file_object.content[new_start:]
    return file_object

# I wanna show memory map as a tree
class customEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Folder):
            return obj.__dict__
        if isinstance(obj, File):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

def show_memory_map(file_system):
    with open('memory_map.json', 'w') as outfile:
        json.dump(file_system, outfile, cls=customEncoder, indent=4)
    return file_system

#print memory map
def print_memory_map(file_system):
    print(json.dumps(file_system, cls=customEncoder, indent=4))
    return file_system


#recursivelt printing and size
def print_file_system(file_system):
    for child in file_system:
        if isinstance(file_system[child], Folder):
            print_file_system(file_system[child].children)
        else:
            #folder size
            print(file_system[child].name, file_system[child].location, file_system[child].content)
            print(file_system[child].get_size())
    return file_system
def print_folders(file_system):
    for child in file_system:
        if isinstance(file_system[child], Folder):
            print(file_system[child].name, file_system[child].location,"Size is", file_system[child].get_size())
            print_folders(file_system[child].children)
    return file_system




#main
#disk initialization with 4gb size and 1kb block size
memory=Disk(100, 10)

file_system=create_file_system(memory)
file_system=mkdir(file_system,"folder1","root","root/folder1",memory)
 

#files
file_system=create_file(file_system,"file1","root","root","file1 is this name is",memory)
file_system=create_file(file_system,"file2","root","root","file2 is this name is",memory)
file_system=create_file(file_system,"file3","root","root","file3 is this name is",memory)
file_system=create_file(file_system,"file4","root","root","file4 is this name is",memory)
file_system=create_file(file_system,"file5","root","root","file5 is this name is",memory)


#using ls
ls(file_system, "root")
ls(file_system, "root/folder1")

memory.print_blocks()

#move
move_file(file_system,file_system, "file3", "root", "root/folder1",memory)


# print_file_system(file_system)
#printing memory map
# show_memory_map(file_system)
# print_memory_map(file_system)
#print disk blocks
memory.print_blocks()



