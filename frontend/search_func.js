const searchButton = document.getElementById("searchButton")

function updateProducts() {
    console.log("clicked")

    user_input = document.getElementById("searchInput").value
    // document.getElementById("searchInput").value = ""

    if (user_input == "") 
        return
    var queryString = '/getProducts?q=' + user_input;

    var result = getFilter();
    var filter_price = result[0];
    var filter_brands = result[1];
    var filter_shops = result[2];

    if (filter_price != '') {
      queryString += '&price=' + filter_price;
    }
    if (filter_brands != '') {
      queryString += '&brands=' + filter_brands;
    }
    if (filter_shops != '') {
      queryString += '&shops=' + filter_shops;
    }
    console.log(queryString);
    $.get(queryString)
    .then(function(data) {
        var good_products_div = document.getElementsByClassName("good-products")[0];
        var best_product_div = document.getElementsByClassName("best-product")[0] ;
        
        good_products_div.innerHTML = '';
        best_product_div.innerHTML = '';
        if (data == "") {
          return;
        }
        console.log(data)
        var good_products_div = document.getElementsByClassName("good-products")[0];
        var best_product_div = document.getElementsByClassName("best-product")[0] ;
        
        good_products_div.innerHTML = '';
        // console.log(good_products_div)
        // while (good_products_div.firstChild) {
        //   good_products_div.removeChild(good_products_div.firstChild);
        // }

        best_product_div.innerHTML = data[0];
        
        for (var i = 1; i < data.length; i++) {
            console.log(typeof data[i])
            // product_divs[i].innerHTML = data[i+1] 
            // Create a new div element for each data item
            var newDiv = document.createElement("div");
            // var doc = (new DOMParser).parseFromString(data[i], "text/html");
            newDiv.innerHTML = data[i];

            // Append the new div to the good_products_div
            good_products_div.appendChild(newDiv.firstChild);
            // good_products_div.insertAdjacentElement('beforeend', data[i])
        }
    })

}

searchButton.onclick = updateProducts;
searchInput.addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    updateProducts();
  }
});


  // ----------------
// Get slider elements
const slider1 = document.getElementById('slider1');
const slider2 = document.getElementById('slider2');

// Get slider values
value11 = document.getElementById('slider-value11');
value12 = document.getElementById('slider-value12');
value21 = document.getElementById('slider-value21');
value22 = document.getElementById('slider-value22');

// Get slider track
const track = document.querySelector('.slider-track');
const trackFill = document.querySelector('.slider-track-fill');

// Calculate track width
const trackWidth = track.offsetWidth;

// Calculate slider thumb width
const thumbWidth = slider1.offsetWidth;

// Calculate maximum left position for slider1
const maxLeftPosition = trackWidth - thumbWidth;

// Calculate maximum left position for slider2
const minLeftPosition = thumbWidth;

// Add event listeners for slider1
slider1.addEventListener('mousedown', startDragSlider1);
slider1.addEventListener('touchstart', startDragSlider1);

// Add event listeners for slider2
slider2.addEventListener('mousedown', startDragSlider2);
slider2.addEventListener('touchstart', startDragSlider2);

// Function to handle slider1 drag
function startDragSlider1(event) {
  event.preventDefault();
  document.addEventListener('mousemove', dragSlider1);
  document.addEventListener('touchmove', dragSlider1);
  document.addEventListener('mouseup', stopDragSlider1);
  document.addEventListener('touchend', stopDragSlider1);
}

// Function to handle slider2 drag
function startDragSlider2(event) {
  event.preventDefault();
  document.addEventListener('mousemove', dragSlider2);
  document.addEventListener('touchmove', dragSlider2);
  document.addEventListener('mouseup', stopDragSlider2);
  document.addEventListener('touchend', stopDragSlider2);
}

// Function to handle slider1 drag
function dragSlider1(event) {
  const clientX = event.type === 'touchmove' ? event.touches[0].clientX : event.clientX;
  const position = clientX - track.getBoundingClientRect().left;
  const leftPosition = Math.min(Math.max(position - thumbWidth / 2, 0), maxLeftPosition);

  // Update slider1 position
  slider1.style.left = `${leftPosition}px`;

  // Update slider1 value
  const value = Math.round((leftPosition / maxLeftPosition) * 150000000);
  value11.textContent = value.toLocaleString() + 'đ';
  value12.textContent = value.toLocaleString() + 'đ';
  // console.log("slider1: " + value);

  // Update slider track fill
  trackFill.style.left = `${leftPosition}px`;
  trackFill.style.width = `${slider2.getBoundingClientRect().left - slider1.getBoundingClientRect().left}px`;
}

// Function to handle slider2 drag
function dragSlider2(event) {
  const clientX = event.type === 'touchmove' ? event.touches[0].clientX : event.clientX;
  const position = clientX - track.getBoundingClientRect().left;
  const leftPosition = Math.max(Math.min(position - thumbWidth / 2, maxLeftPosition), minLeftPosition);

  // Update slider2 position
  slider2.style.left = `${leftPosition}px`;

  // Update slider2 value
  const value = Math.round((leftPosition / maxLeftPosition) * 150000000);
  value21.textContent = value.toLocaleString() + 'đ';
  value22.textContent = value.toLocaleString() + 'đ';
  // console.log("slider2: " + value);

  // Update slider track fill
  trackFill.style.width = `${slider2.getBoundingClientRect().left - slider1.getBoundingClientRect().left}px`;
}

// Function to stop dragging slider1
function stopDragSlider1() {
  document.removeEventListener('mousemove', dragSlider1);
  document.removeEventListener('touchmove', dragSlider1);
  document.removeEventListener('mouseup', stopDragSlider1);
  document.removeEventListener('touchend', stopDragSlider1);
  updateProducts();
}

// Function to stop dragging slider2
function stopDragSlider2() {
  document.removeEventListener('mousemove', dragSlider2);
  document.removeEventListener('touchmove', dragSlider2);
  document.removeEventListener('mouseup', stopDragSlider2);
  document.removeEventListener('touchend', stopDragSlider2);
  updateProducts();
}

// const checkbox = document.querySelector('.css-lc01j1');
//     checkbox.addEventListener('change', function() {
//         if (this.checked) {
//             // Checkbox is checked
//             console.log('Checkbox is checked');
//         } else {
//             // Checkbox is not checked
//             console.log('Checkbox is not checked');
//         }
//     });


// function printCheckedLabels() {
//   const checkboxes = document.querySelectorAll('.css-lc01j1'); // Select all checkboxes
//   const checkedLabels = [];

//   checkboxes.forEach(function(checkbox) {
//     if (checkbox.checked) {
//       const label = checkbox.closest('.css-1tx6f1r').querySelector('.css-1bxob8i');
//       checkedLabels.push(label.textContent);
//     }
//   });

//   console.log('Checked Labels:', checkedLabels);

//   const checkboxes2 = document.querySelectorAll('.css-lc01j1'); // Select all checkboxes
//   const checkedLabels2 = [];

//   checkboxes2.forEach(function(checkbox) {
//     if (checkbox.checked) {
//       const label = checkbox.closest('.css-1tx6f1r').querySelector('.css-1bxob8i');
//       checkedLabels2.push(label.textContent);
//     }
//   });

//   console.log('Checked Labels:', checkedLabels2);
// }


// const checkboxes = document.querySelectorAll('.css-lc01j1'); // Select all checkboxes

// checkboxes.forEach(function(checkbox) {
//   checkbox.addEventListener('change', function() {
//       printCheckedLabels();
//   });
// });

const shopUrls = {
  'Fptshop': ['fptshop.com.vn'],
  'Cellphones': ['cellphones.com.vn'],
  'Phong Vũ': ['phongvu.vn'],
  'Thế giới di động': ['thegioididong.com'],
  'Hà Nội Computer': ['hacom.vn'],
  'Tiki': [
    'tiki.vn',
    'tka.tiki.vn'
  ]
  // Add more mappings as needed...
};

function getFilter() {
  const slidervalue11_string = document.getElementById("slider-value11").textContent;
  const slidervalue21_string = document.getElementById("slider-value21").textContent;
  var slidervalue11 = parseInt(slidervalue11_string.replace(/\./g, ""), 10);
  var slidervalue21 = parseInt(slidervalue21_string.replace(/\./g, ""), 10);

  const checkboxGroups = document.querySelectorAll('.css-0'); // Select all checkbox groups

  console.log(slidervalue11 + '->' + slidervalue21);
  var filter_price = [slidervalue11, slidervalue21];
  var concatenatedPrice = filter_price.join(',');

  var groupCheckBox = 1;
  var concatenatedBrands;
  var concatenatedShops;
  checkboxGroups.forEach(function(group) {
    const checkboxes = group.querySelectorAll('.css-lc01j1'); // Select checkboxes within the group
    const checkedLabels = [];

    checkboxes.forEach(function(checkbox) {
      if (checkbox.checked) {
        const label = checkbox.closest('.css-1tx6f1r').querySelector('.css-1bxob8i');
        if (groupCheckBox == 1) 
          checkedLabels.push(label.textContent);
        else {
          var urls = shopUrls[label.textContent];
          for (var i = 0; i < urls.length; i++) {
            var url = urls[i];
            checkedLabels.push(url);
          }

        }
          
        // labels += label;
      }
    });

    console.log('Checked Labels (Group):', checkedLabels);
    if (groupCheckBox == 1) {
      concatenatedBrands = checkedLabels.join(',');
    }
    else concatenatedShops = checkedLabels.join(',');
    groupCheckBox++;
  });


  return([concatenatedPrice, concatenatedBrands, concatenatedShops])
}

const checkboxes = document.querySelectorAll('.css-lc01j1'); // Select all checkboxes

checkboxes.forEach(function(checkbox) {
  checkbox.addEventListener('change', function() {
    updateProducts();
  });
});