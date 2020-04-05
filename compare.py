from pathlib import Path
import time
from html.parser import HTMLParser
import re

t0 = time.time()

#ask user to ignore folders
finishInput = False
dirsToIgnore = [];
usedFiles = [];
ignoredFiles = [];
print("Want to ignore folder or files for the comparison? Y/N")
text = input("")
if text == "Y" or text == "y":
    while not finishInput:
        print("Input folder- or filename to ignore (if multiple, separate by comma)")
        text = input("")
        ignoreDirs = text.split(",")
        for dir in ignoreDirs:
            dirsToIgnore.append(dir)
        finishInput = True
    print("Ignoring following folders/fils:")
    for ignoreDir in dirsToIgnore:
        print(ignoreDir)
#find all html files
htmlFiles = list(Path(".").rglob("*.[hH][tT][mM][lL]"))

print("Found",len(htmlFiles), "HTML file(s).")

#find all css files
cssFiles = list(Path(".").rglob("*.[cC][sS][sS]"))
print("Found",len(cssFiles),"CSS File(s).")

#find all js files
jsFiles = list(Path(".").rglob("*.[jJ][sS]"))
print("Found",len(jsFiles), "JS File(s).")

divClasses = set()
cssClasses = set()
jsClasses = set()
allJsLines = []
allCssLines = []
allLines = []

#read all html files found inside the project folder 
for entry in htmlFiles:
    ignoreFile = False
    if len(dirsToIgnore) > 0:
        #check if file is inside folder we want to ignore
        for ignore in dirsToIgnore:
            if ignore in str(entry):
                ignoredFiles.append(str(entry))
                ignoreFile = True 
    if not ignoreFile:
        file = open (entry,"r")
        usedFiles.append(str(entry))
        lines =file.readlines()
        for line in lines:
            allLines.append(line)

#read all css files found inside the project folder 
print("\n Found follwing valid css class(es):\n")
cssClassCounter = 0
for entry in cssFiles:
    ignoreFile = False
    if len(dirsToIgnore)>0:
        for ignore in dirsToIgnore:
            if ignore in str(entry):
                ignoredFiles.append(str(entry))
                ignoreFile = True
    if not ignoreFile:
        file = open(entry, "r")
        usedFiles.append(str(entry))
        lines = file.readlines()
        for line in lines:
            #only find the actual css classes and remove the leading dot
            reClass = re.compile(r'[.][a-zA-Z\-\_1234567890]+')
            finds = reClass.findall(line)
            if finds:
                #now add each class without the dot to the cssClassSet
                for cssClass in finds:
                    if not cssClass[1:] in cssClasses:
                        #todo rework to regex
                        cssClasses.add(cssClass[1:])
                        print(cssClassCounter, cssClass)
                        cssClassCounter += 1

#read all js files found inside the project folder
print("\n Found following valid class(es) dynamically added  via js or used by js:")
jsClassCounter = 0
for entry in jsFiles:
    ignoreFile = False
    if len(dirsToIgnore)>0:
        for ignore in dirsToIgnore:
            if ignore in str(entry):
                ignoredFiles.append(str(entry))
                ignoreFile = True
    if not ignoreFile:
        file = open(entry, "r")
        usedFiles.append(str(entry))
        lines = file.readlines()
        for line in lines:
            #find all classes dyanmically added via js
            patternAddClass = r'.*addClass\x28[\x22\x27]*([\w\s\-]*)' 
            patternSetAttribute = r'.*setAttribute\x28[\x22\x27]class[\x22\x27],\s[\x22\x27]*([\w\s\-]*)'
            patternClassListAdd = r'.*classList.add\x28[\x22\x27]*([\w\s\-]*)'
            patternClassName = r'.*className\s*\+\=\s*[\x22\x27]*([\w\s\-]*)'
            patternVanillaJs = r'.*getElementsByClassName\x28[\x22\x27]*([\w\s\-]*)'
            patternClassSyntax = r'.*[\x22\x27]\.([\w\s\-\_\.]*)'
            patterns = [patternAddClass, patternSetAttribute, patternClassListAdd, patternClassName, patternVanillaJs, patternClassSyntax]
            for pattern in patterns:
                finds = re.search(pattern, line)
                if finds:
                    findArray = finds[1].replace("."," ").split(" ")
                    for entry in findArray:
                        if not entry in jsClasses and not entry =="":          
                            jsClasses.add(entry)
                            print(jsClassCounter, entry)
                            jsClassCounter += 1
classCounter = 0

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global classCounter 
        classCounterForDiv = 0
        if tag == "div" or tag == "select" or tag == "button" or tag == "label" or tag == "span" or tag == "img" or tag == "ul":
            #print("Checking next div.")
            #go through all attributes
            for attr in attrs:
                #find the class attribute
                if attr[0] == "class":
                    classArray = attr[1].split(" ")
                    for entry in classArray:
                    #check if the class already exists in the set
                         if not entry in divClasses:
                             #add if not existing
                             print(classCounter,":", entry)
                             divClasses.add(entry)
                             classCounter += 1

print("\n Found following div classes:\n")
parser = MyHTMLParser()
for line in allLines:
    #not working 
    #remove leading and ending whitespaces 
    #line.strip(" ")
    #ignore lines with closing div
    if not line == "</div>":
        parser.feed(line)

#now match div classes to css and vice versa
divNotInCssOrJs = set()
cssNotInDivOrJs = set()

print("\n Finding unused div classes...\n")
print("Following div classes have no related css entry or get used by js:")
notUsedCounter = 0
for divClass in divClasses:
    if not divClass in cssClasses and not divClass in jsClasses:
        divNotInCssOrJs.add(divClass)
        print(notUsedCounter,":", divClass)
        notUsedCounter += 1

print("\n Finding unused css classes...\n")
print("Following css classes have no related div classes in html or js files:")
for cssClass in cssClasses:
    if not cssClass in divClasses and not cssClass in jsClasses:
        cssNotInDivOrJs.add(cssClass)
        print(notUsedCounter, ":", cssClass)
        notUsedCounter += 1

file = open("report.txt", "w+")
file.write("Found following files: \n")
for entry in usedFiles:
    file.write(entry)
    file.write("\n")
basicCounter = 0
file.write("-------------------------------\n")
file.write("Ignored following files: \n")
file.write("\n")
file.write("-------------------------------\n")
for entry in ignoredFiles:
    file.write(str(basicCounter) + ":" + entry)
    file.write("\n")
    basicCounter += 1

basicCounter = 0
file.write("-------------------------------\n")
file.write("Found following div classes inside html files:")
file.write("\n")
file.write("-------------------------------\n")
for entry in divClasses:
       file.write(str(basicCounter) + ":" + entry)
       file.write("\n")
       basicCounter += 1

basicCounter = 0
file.write("-------------------------------\n")
file.write("Found following div classes inside css files:")
file.write("\n")
file.write("-------------------------------\n")
for entry in cssClasses:
       file.write(str(basicCounter) + ":" + entry)
       file.write("\n")
       basicCounter += 1

basicCounter = 0
file.write("-------------------------------\n")
file.write("Found following div classes inside js files:")
file.write("\n")
file.write("-------------------------------\n")
for entry in jsClasses:
       file.write(str(basicCounter) + ":" + entry)
       file.write("\n")
       basicCounter += 1

file.write("-------------------------------\n")
file.write("CSS classes not found in any html or js file: ")
file.write(str(len(cssNotInDivOrJs)))
file.write("\n")
file.write("-------------------------------\n")
file.write("\n")


basicCounter = 0
for entry in cssNotInDivOrJs:
    file.write(str(basicCounter) + ":" + entry)
    file.write("\n")
    basicCounter += 1

file.write("\n")
file.write("-------------------------------\n")
file.write("DIV classes not found in any css or js file:")
file.write(str(len(divNotInCssOrJs)))
file.write("\n")
file.write("-------------------------------\n")
file.write("\n")

basicCounter = 0
for entry in divNotInCssOrJs:
    file.write(str(basicCounter) + ":" + entry)
    file.write("\n")
    basicCounter += 1

file.close()
print()
print("Created report.txt containing the classes and files.")
t1 = time.time()
total = t1-t0
print("Finished after",round(total,2), "seconds.")

