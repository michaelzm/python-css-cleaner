from pathlib import Path
from html.parser import HTMLParser
import re

#ask user to ignore folders
finishInput = False
dirsToIgnore = [];
usedFiles = [];
ignoredFiles = [];
print("Want to ignore folder or files for the comparison? Y/N")
text = input("")
if text == "Y" or text == "y":
    while not finishInput:
        print("Input folder- or filename to ignore (1)")
        text = input("")
        dirsToIgnore.append(text)
        print("Ignore another folder/file? Y/N")
        text = input("")
        if text == "N" or text == "n":
            finishInput = True

    print("Ignoring following folders/fils:")
    for ignoreDir in dirsToIgnore:
        print(ignoreDir)
#find all html files
htmlFiles = list(Path(".").rglob("*.[hH][tT][mM][lL]"))

print("Found",len(htmlFiles), "HTML file(s).")

#find all css fiels
cssFiles = list(Path(".").rglob("*.[cC][sS][sS]"))
print("Found",len(cssFiles),"CSS File(s).")

divClasses = set()
cssClasses = set()
allCssLines = []
allLines = []

#read all html files found inside the project folder 
for entry in htmlFiles:
    ignoreFile = False
    if len(dirsToIgnore) > 0:
        #check if file is inside folder we want to ignore
        for ignore in dirsToIgnore:
            if ignore in str(entry):
                print("Ignoring:", str(entry))
                ignoredFiles.append(str(entry))
                ignoreFile = True 
    if not ignoreFile:
        file = open (entry,"r")
        usedFiles.append(str(entry))
        lines =file.readlines()
        for line in lines:
            allLines.append(line)

#read all css files found inside the project folder 
print("Found follwing valid css class(es):")
cssClassCounter = 0
for entry in cssFiles:
    ignoreFile = False
    if len(dirsToIgnore)>0:
        for ignore in dirsToIgnore:
            if ignore in str(entry):
                print("ignoring", str(entry))
                ignoredFiles.append(str(entry))
                ignoreFile = True
    if not ignoreFile:
        file = open(entry, "r")
        usedFiles.append(str(entry))
        lines = file.readlines()
        for line in lines:
            #only find the actual css classes and remove the leading dot
            reClass = re.compile(r'[.][a-zA-Z-1234567890]+')
            finds = reClass.findall(line)
            if finds:
                #now add each class without the dot to the cssClassSet
                for cssClass in finds:
                    print(cssClassCounter, cssClass)
                    cssClasses.add(cssClass[1:])
                    cssClassCounter += 1

classCounter = 0

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global classCounter 
        classCounterForDiv = 0
        if tag == "div":
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

print("Found following div classes:")
parser = MyHTMLParser()
for line in allLines:
    #not working 
    #remove leading and ending whitespaces 
    #line.strip(" ")
    #ignore lines with closing div
    if not line == "</div>":
        parser.feed(line)

#now match div classes to css and vice versa
divNotInCss = set()
cssNotInDiv = set()

print()
print("Finding unused div classes...")
print("Following div classes have no related css entry:")
for divClass in divClasses:
    if not divClass in cssClasses:
        divNotInCss.add(divClass)
        print(divClass)
print()
print("Finding unused css classes...")
print("Following css classes have no related div classes in html files:")
for cssClass in cssClasses:
    if not cssClass in divClasses:
        cssNotInDiv.add(cssClass)
        print(cssClass)

file = open("report.txt", "w+")
file.write("Found following files: \n")
for entry in usedFiles:
    file.write(entry)
    file.write("\n")
file.write("-------------------------------\n")
file.write("Ignored following files: \n")
for entry in ignoredFiles:
    file.write(entry)
    file.write("\n")
file.write("-------------------------------\n")
file.write("CSS classes not found in any html file: ")
file.write(str(len(cssNotInDiv)))
file.write("\n")
file.write("-------------------------------\n")
file.write("\n")

for entry in cssNotInDiv:
    file.write(entry)
    file.write("\n")

file.write("\n")
file.write("DIV classes not found in any css file: ")
file.write(str(len(divNotInCss)))
file.write("\n")
file.write("-------------------------------\n")
file.write("\n")

for entry in divNotInCss:
    file.write(entry)
    file.write("\n")

file.close()
print()
print("Created report.txt containing the files.")
