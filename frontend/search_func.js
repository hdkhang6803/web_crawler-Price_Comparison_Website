const searchButton = document.getElementById("searchButton")

searchButton.onclick = function search() {
    console.log("clicked")

    user_input = document.getElementById("searchInput").value
    document.getElementById("searchInput").value = ""

    $.get('/getProducts?q=' + user_input)
    .then(function(data) {
        console.log(data)
        var product_divs = document.getElementsByClassName("css-13w7uog")
        var best_product_div = document.getElementsByClassName("best-product")[0] 
        best_product_div.innerHTML = data[0]
        for (var i = 0; i < product_divs.length; i++) {
            console.log(data[i])
            product_divs[i].innerHTML = data[i+1] 
        }
    })

}