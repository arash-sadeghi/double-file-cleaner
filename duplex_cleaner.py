# 937 Files, 0 Folders (3,773,885,212 bytes
import filecmp
import os
import pickle
from time import ctime,time

path="."


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    try:
        listOfFile = os.listdir(dirName)
    except Exception as E:
        print("[-] access error: {}".format(E))
        return 
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            temp=getListOfFiles(fullPath)
            if not (temp is None):
                allFiles = allFiles + temp
        else:
            allFiles.append(fullPath)
                
    return allFiles

allFiles=getListOfFiles(path)

deleted=[]
original=[]
for file1 in allFiles:
    temp=[]
    for file2 in allFiles[allFiles.index(file1):]:
        if file1 != file2 and (not(file1 in deleted)) and (not(file2 in deleted)):
            if filecmp.cmp(file1 , file2):
                temp.append(file2)

    if temp!=[]:
        deleted.append(temp)
        original.append(file1)
    deleted_len=sum(len(row) for row in deleted)
    process=allFiles.index(file1)/(len(allFiles)-deleted_len)*100
    print("[+] process: {:.2f}".format(process),end='\r')

Time=ctime(time()).replace(':','_')
open_file = open("deleted_"+Time+"_.pylist", "wb")
pickle.dump(deleted, open_file)
open_file.close()


open_file = open("original_"+Time+"_.pylist", "wb")
pickle.dump(original, open_file)
open_file.close()



ignore_input=False
for c,row_2B_deleted in enumerate(deleted):
    for element_2B_deleted in row_2B_deleted:
        if not ignore_input:
            print("gonna delete {} because {} exist? [y/n/a]".format(element_2B_deleted,original[c]))
            key=input()
        if key=='y' or key=='a' or ignore_input:
            try:
                os.remove(element_2B_deleted)
            except Exception as E:
                print("[-] file {} , duplicate of {} , could not be deleted: {}"\
                    .format(element_2B_deleted,original[c]),E)
        if key=='a':
            ignore_input=True