function toggleElement(element) {
  var style = window.getComputedStyle(element);
  if (style.display === "none") {
    element.style.display = "block";
  } else {
    element.style.display = "none";
  }
}

function toggleElements(elements) {
  elements.forEach(element => {
    toggleElement(element)
  });
}

function hideElement(element) {
  element.style.display = "none";
}
