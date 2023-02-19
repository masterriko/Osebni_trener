// Define variables
var column = document.getElementById("column");
var select = document.getElementById("select");

// Add event listeners
select.addEventListener("change", addItem);
column.addEventListener("dragstart", dragStart);
column.addEventListener("dragover", dragOver);
column.addEventListener("drop", drop);

// Function to add a new item to the column
function addItem() {
  var value = select.value;
  if (value !== "") {
    var row = document.createElement("div");
    row.className = "row";
    row.draggable = true;
    row.innerHTML = "<span>" + value + "</span><button onclick='deleteItem(this.parentNode)'>x</button>";
    column.appendChild(row);
    select.value = "";
  }
}

// Function to delete an item from the column
function deleteItem(item) {
  column.removeChild(item);
}

// Function to handle drag start event
function dragStart(event) {
  var item = event.target;
  item.classList.add("dragging");
}

// Function to handle drag over event
function dragOver(event) {
  event.preventDefault();
}

// Function to handle drop event
function drop(event) {
  var item = event.target;
  if (item.className === "row") {
    var draggingItem = document.querySelector(".dragging");
    var nextItem = item.nextElementSibling;
    if (nextItem === draggingItem) {
      nextItem = nextItem.nextElementSibling;
    }
    column.insertBefore(draggingItem, nextItem);
    draggingItem.classList.remove("dragging");
  }
}