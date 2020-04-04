#find all html files
from pathlib import Path
result = list(Path(".").rglob("*.[hH][tT][mM][lL]"))
print(result)
classCounter = 0
classCounterForDiv = 0
from html.parser import HTMLParser

classes = set()
allLines = []
#read all html files in the project folder
for entry in result:
    file = open (entry,"r")
    print(file)
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
            print("found new div")
            #go through all attributes
            for attr in attrs:
                #find the class attribute
                if attr[0] == "class":
                    print ("classes of div",attr[1])
                    classArray = attr[1].split(" ")

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
            print ("Finished div and added", classCounterForDiv, "new classes.")

parser = MyHTMLParser()
for line in allLines:
    #not working 
    #remove leading and ending whitespaces 
    #line.strip(" ")
    #ignore lines with closing div
    if not line == "</div>":
        parser.feed(line)
#parser.feed('<div id= "button-nav" class = "light dark big small-go-up-button"></div>')
print("Found",classCounter,"classes.")
