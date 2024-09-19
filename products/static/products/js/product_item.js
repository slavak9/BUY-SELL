// replace images from sub window to main window //
const mainImgWindow = document.querySelector('.main-product-img-cont');
let VideoIsMain = false;
const mainImg = document.querySelector('.main-product-img-cont img');
const UlContainer = document.querySelector('.product_img_grid');
const GalleryUrl = document.querySelector('#gallery__url');
const BtAddProductToCart = document.querySelector('#id_add_cart')
const BtRedirectToCart = document.querySelector('#id_cart_redirect')
const ProductPrice = document.querySelector('.price-h3-style')

function changeIMG(id) {
    const subImg = document.getElementById(id);
    if (!VideoIsMain) {
        mainImgWindow.innerHTML = subImg.outerHTML;
    } else {
        subImg.addEventListener('click', () => {
            VideoIsMain = false;
            mainImgWindow.innerHTML = subImg.outerHTML;
            UlContainer.style.cursor = 'default'
            GalleryUrl.style.cursor = 'zoom-in'
        })
    };
}

UlContainer.addEventListener('mouseleave', () => {
    if (!VideoIsMain) { mainImgWindow.innerHTML = mainImg.outerHTML }
})

// change value of input quantity on button click  //

function ShowPrise(N){
    let price = Number(N*ProductPrice.dataset.price).toFixed(2)
    if(price < 0){price = (0).toFixed(2)}
    ProductPrice.innerHTML=`<strong>${price.slice(0,length-3)}</strong>,${price.slice(price.length-2)}`
};

const plusQuantBt = document.querySelector('#plus__bt');
const minusQuantBt = document.querySelector('#minus__bt');
const inputValue = document.querySelector('.input_Product_Quantity');
const errorQuantity = document.querySelector('.display_error_quantity span')
let productQuantity;
if(inputValue){productQuantity = inputValue.value};


function addRemoveProductQuantity(operand) {
    if (Math.abs(inputValue.value)) {
        const quantityAvailable = Number(errorQuantity.textContent);
        productQuantity = Math.abs(inputValue.value);
        if (operand === 'minus') { --productQuantity };
        if (operand === 'plus') { ++productQuantity };
        if (productQuantity > quantityAvailable) { productQuantity = quantityAvailable };
        if (productQuantity <= 0) { productQuantity = 1 };
    } else {
        productQuantity = 1
    }
    inputValue.value = productQuantity;
    valueInputControl();
    ShowPrise(productQuantity);
};

plusQuantBt.addEventListener('click', () => { addRemoveProductQuantity('plus') });
minusQuantBt.addEventListener('click', () => { addRemoveProductQuantity('minus') });

// input quantity field error message //
function valueInputControl() {
    const QuantityError = document.querySelector('.display_error_quantity');
    const InputOutlinestyle = document.querySelector('.minus_plus input')
    if (Math.abs(inputValue.value) && Math.abs(inputValue.value) <= Number(errorQuantity.textContent)) {
        QuantityError.style.display = 'none'; 
        InputOutlinestyle.classList.remove('input_outline_stile')
    } else {
        QuantityError.style.display = 'initial';
        InputOutlinestyle.classList.add('input_outline_stile')
    };
};
valueInputControl();

inputValue.addEventListener('keyup', () => {
    valueInputControl();
    productQuantity = inputValue.value;
    ShowPrise(productQuantity)
})

// activate-deactivate sub-video
function replaceSubContent(id) {
    const SubVideoImgContainer = document.getElementById(`sub_video_container_${id}`)
    const imgSubPlayer = document.getElementById(`play_sub_img_${id}`);
    const videoSubPlayer = document.getElementById(`video_${id}`);
    imgSubPlayer.style.display = 'none';
    videoSubPlayer.muted = true;
    if (videoSubPlayer.paused || videoSubPlayer.ended) {
        videoSubPlayer.play()
    };
    SubVideoImgContainer.addEventListener('mouseleave', () => {
        videoSubPlayer.pause();
        imgSubPlayer.style.display = 'initial';
    });
    SubVideoImgContainer.addEventListener('click', () => {
        const videoSrc = document.getElementById(`video_src_${id}`);
        mainImgWindow.innerHTML = `<video width="100%" controls><source src="${videoSrc.src}"></video>`;
        VideoIsMain = true;
        UlContainer.style.cursor = 'pointer'
        GalleryUrl.style.cursor = 'default'
    });
};

//show message about cart changes
function CartChangesMessage(message, param) {
    const cartMessage = document.querySelector('.buy_form_message')
    if (param) {
        cartMessage.style.color = 'rgb(64, 162, 49)'
        cartMessage.textContent = message
        setTimeout(() => {
            cartMessage.textContent = ''
        }, 4000);
    } else {
        cartMessage.style.color = 'red'
        cartMessage.textContent = message
        setTimeout(() => {
            cartMessage.textContent = ''
        }, 5000);
    }
}

// change quantity of the cart
function changeCartQuantity() {
    const cartValue = document.querySelector('#cart_quantity');
    const num = Number(cartValue.textContent) + 1;
    cartValue.textContent = num;
};


// add a product to the cart
function CreateJSON(trigger){
    const ObjectData = {
        'product_id': inputValue.dataset.product,
        'trigger':trigger
    };
    if(Math.abs(productQuantity)){ObjectData['quantity'] = Math.abs(productQuantity)}
    if(ObjectData.product_id && ObjectData.quantity){
        return JSON.stringify(ObjectData);
    }else{return false}
    
};


function addProductToTheCart(event, trigger) {
    event.preventDefault();
    const data = CreateJSON(trigger);
    if(data){
    $.ajax({
        type: 'POST',
        dataType: 'json',
        data: {
            data:data,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            if (response['saved']) {
                changeCartQuantity()
                CartChangesMessage(response['saved'], true)
                if (response['url']) {
                    window.location.href = response['url']
                }
            }
            else if (response['quantity']) {
                CartChangesMessage(response['quantity'], true)
                if (response['url']) {
                    window.location.href = response['url']
                }
            }
            else if (response['error']) {
                CartChangesMessage(response['error'], false)
            }
        },
        failure: function (response) { alert('something went wrong'); }
    })
}
};

BtAddProductToCart.addEventListener('click', (event) => {
    let trigger = false;
    addProductToTheCart(event, trigger)
});

BtRedirectToCart.addEventListener('click', (event) => {
    let trigger = true;
    addProductToTheCart(event, trigger)
});

const ShowAddInfoPr = document.querySelector("#more-info-item");
let Switch = false;
ShowAddInfoPr.addEventListener('click',()=>{
    const I = document.querySelectorAll('.var-block-des')
    I.forEach(e=>{
        if(Switch){
            e.classList.remove('display_flex')
            e.classList.add('display_none')
        }else{
            e.classList.remove('display_none')
            e.classList.add('display_flex')
        }
    })
    if(Switch){
        ShowAddInfoPr.textContent = 'more information';
        Switch = false;
    }
    else{
        ShowAddInfoPr.textContent = 'less information';
        Switch = true;
    }
});
