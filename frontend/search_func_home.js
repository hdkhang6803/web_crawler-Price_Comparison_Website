const searchButton = document.getElementById("searchButton");
const searchInput = document.getElementById("searchInput");


function updateProducts() {
    const userInput = searchInput.value.trim();
    if (userInput !== "") {
        window.location.href = "/displayResult?q=" + encodeURIComponent(userInput);
    }
};

searchButton.onclick = updateProducts;
searchInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
      updateProducts();
    }
  });