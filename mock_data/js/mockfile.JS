/**
 * This js file contains possible ways to add or use classes to div elements
 */
//get via jquery
var element = $(".get-via-jquery sub-dir get-by-jq");

//vanilla js
var anotherElement = document.getElementsByClassName("get-via-vanilla-js navbar");


 //add via jquery
$(".mock-class").addClass("test new-class jq-added-class first");

//jQ Event Listener init
$(document).on("click", '.jQ-doc-event-syntax', function(){});

//in case of line breaks
'.just-syntax'

var newElement = document.createElement("div");
//add class via attribute
newElement.setAttribute("class", "menu-big class-added-via-attribute first and-another-class menu-size-1");

newElement.classList.add("class-added-via-classlist class-small-1 small-2 first");

newElement.className += "add-dyn";

this.someFunction($('.random-class.one-more-random-class'));

//not working
newElement.innerHTML = "<div class = 'class-added-via-inner-html'></div>";

$jQElement.find('.some-class').append(someContainer);
