import os
dict = {}
def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()

    # Iterate over all the entries
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
            idx_from = ''

            for idx, char in enumerate(fullPath):
                if char == "/":
                    idx_from = idx

            idx_to = len(fullPath)
            cur_file_name = fullPath[idx_from+1:idx_to]


            dict[cur_file_name] = fullPath
    return allFiles

def getDictofFiles(dirName):
    temp_list = getListOfFiles(dirName)
    return dict
#for key, value in dict.items():
#    print(key, ' : ', value)