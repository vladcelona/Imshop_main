const sections = document.querySelectorAll('section[id]')

// The function for scrolling to the selected section on a landing page
function scrollActive(){
    const scrollY = window.pageYOffset

    sections.forEach(current=> {
        const sectionHeight = current.offsetHeight,
            sectionTop = current.offsetTop - 50,
            sectionId = current.getAttribute('id')

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight){
            document.querySelector('.nav__menu a[href*=' + sectionId + ']')
                .classList.add('active-link')
        } else {
            document.querySelector('.nav__menu a[href*=' + sectionId + ']')
                .classList.remove('active-link')
        }
    })
}
window.addEventListener('scroll', scrollActive);

/* -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-= */

// The function for changing the background header
function scrollHeader(){
    const header = document.getElementById('header')
    // When the scroll is greater than 80 viewport height, add the scroll-header class to the header tag
    if (this.scrollY >= 80) {
        header.classList.add('scroll-header');
    } else {
        header.classList.remove('scroll-header');
    }
}
window.addEventListener('scroll', scrollHeader);

/* -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-= */

// Items in a popup window
const popupWindow = document.getElementById('popupWindow');
const closeButton = document.getElementById('closeButton');
const popupImage = document.getElementById('popupImage');
const popupPrice = document.getElementById('popupPrice');
const popupDescription = document.getElementById('popupDescription');

// Properties for closeButton
closeButton.addEventListener('click', () => {
    popupWindow.style.display = 'none';
});

/* -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-= */

// Item container for items below
const itemContainerCatalog = document.getElementById('itemContainerCatalog');

// Example list of items
const items = [
    {
        image: 'https://via.placeholder.com/100',
        price: '$19.99',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        favorites: false,
        shopping_cart: false,
    },
    {
        image: 'https://via.placeholder.com/100',
        price: '$29.99',
        description: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        favorites: false,
        shopping_cart: false,
    },
    {
        image: 'https://via.placeholder.com/100',
        price: '$109.99',
        description: 'Sed do eiusmod tempor Lorem ipsum dolor sit amet',
        favorites: false,
        shopping_cart: false,
    },
    {
        image: 'https://via.placeholder.com/100',
        price: '$209.99',
        description: 'Sed do eiusmod tempor Lorem ipsum dolor sit amet',
        favorites: false,
        shopping_cart: false,
    },
    {
        image: 'https://via.placeholder.com/100',
        price: '$9.99',
        description: 'Sed do eiusmod tempor Lorem ipsum dolor sit amet',
        favorites: false,
        shopping_cart: false,
    }
  // Add more items here
];

/* -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-= */

// Function for creation of a single item
function createItem(itemData) {
    const item = document.createElement('div');
    item.className = 'list-item';
    item.innerHTML = `
        <img src="${itemData.image}" alt="Example Item Image">
        <div class="item-price">${itemData.price}</div>
        <div class="item-description">${itemData.description}</div>
        <div class="button-row">
            <button class="shopping-cart-button" id="itemShoppingCartButton">
                <span class="shopping-cart-text">Add to cart</span>
            </button>
            <button class="favorites-button" id="itemFavoritesButton">
                <img class="favorites-icon" src="https://raw.githubusercontent.com/vladcelona/Imshop_main/master/web_files/image_files/iconmonstr-heart-thin.svg" alt="Heart Icon">
            </button>
        </div>
    `;

    item.addEventListener('click', function(itemElement) {
        if (itemElement.target.id !== 'itemShoppingCartButton' && itemElement.target.id !== 'itemFavoritesButton') {
            showPopupWindow(itemData);
        }
    });
    return item;
}

// Adding item to itemContainer
items.forEach(itemData => {
    const item = createItem(itemData);
    itemContainerCatalog.appendChild(item);
});

/* -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-= */

// Function for showing the content of an item
function showPopupWindow(itemData) {
    popupWindow.style.display = 'block';
    popupImage.src = itemData.image;
    popupPrice.textContent = itemData.price;
    popupDescription.textContent = itemData.description;
}
