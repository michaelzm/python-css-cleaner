/**
 * This js file contains possible ways to add classes to div elements
 */
//add via jquery
$(".mock-class").addClass("test new-class jq-added-class");


var newElement = document.createElement("div");
//add class via attribute
newElement.setAttribute("class", "class-added-via-attribute and-another-class menu-size-1");

newElement.classList.add("class-added-via-classlist class-small-1 small-2");

newElement.className += "new-class-via-class-name";

newElement.innerHTML = "<div class = 'class-added-via-inner-html'></div>";