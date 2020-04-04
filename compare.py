from pathlib import Path
#find all html files
htmlFiles = list(Path(".").rglob("*.[hH][tT][mM][lL]"))
print("Found",len(htmlFiles), "HTML file(s).")

#find all css fiels
cssFiles = list(Path(".").rglob("*.[cC][sS][sS]"))
print("Found",len(cssFiles),"CSS File(s).")

classCounter = 0
classCounterForDiv = 0
from html.parser import HTMLParser

classes = set()
allLines = []
#read all html files in the project folder
for entry in htmlFiles:
    file = open (entry,"r")
    lines =file.readlines()
    for line in lines:
        allLines.append(line)
print("ALL LINES FOUND INSIDE THE FILES:",allLines)
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global classCounter 
        global classCounterForDiv
	
        classCounterForDiv = 0
        if tag == "div":
            print("Checking next div.")
            #go through all attributes
            for attr in attrs:
                #find the class attribute
                if attr[0] == "class":
                    classArray = attr[1].split(" ")
                    print("Found", len(classArray), "class(es) inside the div.")
                    for entry in classArray:

                     #check if the class already exists in the set
                         if not entry in classes:
                             #add if not
                             print("Adding class",entry)
                             classes.add(entry)
                             classCounter += 1
                             classCounterForDiv += 1
                         else:
                            print("Dup class", entry)
    def handle_endtag(self, tag):
        if tag == "div":
            print ("Finished div and added", classCounterForDiv, "new class(es).")

parser = MyHTMLParser()
for line in allLines:
    #not working 
    #remove leading and ending whitespaces 
    #line.strip(" ")
    #ignore lines with closing div
    if not line == "</div>":
        parser.feed(line)

#print the classes
print("Found",classCounter,"classes.")
iteratorCounter = 0
for cssClass in classes:
    print(iteratorCounter,": ", cssClass)
    iteratorCounter += 1
