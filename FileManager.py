import openpyxl as pyxl
from pathlib import Path
import csv
import os

Fieldnames = ['DirName', 'Path']
current_Dir = []

try:
    FilePaths = open("FilePaths.csv", "x")
    writer = csv.DictWriter(FilePaths, fieldnames = Fieldnames)
    writer.writeheader()
    writer.writerow({Fieldnames[0]: "Root", Fieldnames[1]: Path().absolute()})
    FilePaths.close()
except FileExistsError:
    pass

FilePaths = open("FilePaths.csv", "r+")
reader = csv.DictReader(FilePaths, fieldnames = Fieldnames)
writer = csv.DictWriter(FilePaths, fieldnames = Fieldnames)

for n in reader:
    current_Dir.append(n)


def addtoDirs():
    newDirectory = input("Enter Folder Path: ")
    DirName = input("Enter Folder Name: ")
    DirPath = Path(newDirectory)
    if DirPath.exists():
        if len(list(filter(lambda x: x["DirName"] == DirName, current_Dir))) == 0:
            addDir(DirName, DirPath)
        else:
            print("Dupicate Dir Name")
            addtoDirs()
    elif newDirectory == "":
        return
    else:
        print("wrong directory path")
        addtoDirs()

def addDir(DirName, DirPath):
    writer.writerow({Fieldnames[0]: DirName, Fieldnames[1]: DirPath})
    print(f"Directory:\n{DirPath}\nis added with name:\n{DirName}\n")

def checkDirectory():
    DirName = input("DirName: ")
    while DirName:
        try:
            Files = GetDirectoryFiles(DirName)
            if Files == None:
                print("There are currently no files in this directory")
                break
            for File in Files:
                print(File)
        except NameError:
            print("Name does not exist")
            print("Available directories are\n")
            showDirectories()
        DirName = input("DirName: ")

def GetDirectoryFiles(DirName):
    ##could raise Name error
    path = GetDirPath(DirName)
    if DirName == n["DirName"]:
        files = [x for x in Path(path).glob('**/*') if x.is_file()]
        if len(files) == 0:
            return None
        else:
            return files

def GetDirPath(DirName):
    for entry in current_Dir:
        if DirName == entry["DirName"]:
            return entry["Path"]
    raise NameError

def showDirectories():
    for entry in current_Dir:
        entries = []
        for key, item in entry.items():
            entries.append(item)
        print('  |  '.join(entries))
        
def createNewDirectory(DirLocation):
    pass

def GetFile(DirName, FileName, GetPath=False):
    DirPath = Path(GetDirPath(DirName))
    filepath = DirPath / FileName
    if filepath.exists():
        suffix = filepath.suffix
        match suffix:
            case ".xlsx":
                file = pyxl.load_workbook(filepath)
            case ".csv":
                file = open(filepath, 'r+')
            case _n:
                file = filepath
        if GetPath:
            return file, filepath
        return file
    else:
        return None
    pass

def main():
    option = input(": ")
    while option:
        match option:
            case 'a':
                addtoDirs()
            case 'c':
                checkDirectory()
            case 's':
                showDirectories()
        option = input(": ")
        

if __name__ == "__main__":
    main()


FilePaths.close()
