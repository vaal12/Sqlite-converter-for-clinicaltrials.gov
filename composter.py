import glob, os, datetime

#Subdirs are not working yet
#in file masks - no spaces
FILES_FOR_COMPOSTING = {
    ".": "*.sqlite3,*.log",
    # ".": "*.log",
}

COMPOST_DIR = ".compost"
CompostDirResolved = ""
curr_datetime_str = datetime.datetime.now().strftime("%d-%b-%Y %H-%M.%f")
number_of_files = 0
if not os.path.exists(COMPOST_DIR):
    os.mkdir(COMPOST_DIR)

os.mkdir(COMPOST_DIR+os.sep+curr_datetime_str+os.sep)
CompostDirResolved = os.path.abspath(COMPOST_DIR+os.sep+curr_datetime_str)+os.sep
print("CompostDir:{}".format(CompostDirResolved))

for dirName in FILES_FOR_COMPOSTING:
    os.chdir(dirName)
    fileMasksList = FILES_FOR_COMPOSTING[dirName].split(",")
    for fileMask in fileMasksList:
        for file in glob.glob(fileMask):
            print("-- {}".format(file))
            os.rename(file, CompostDirResolved+file)
            number_of_files +=1

print("{} files moved. All is OK.".format(number_of_files))



