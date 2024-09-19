
const TotalCartPrice = document.querySelector('.total_price_of_selected_items');
const CartTotalPricelist = {};
const CheckOut = document.querySelector('#checkout_button')
CheckOut.value = ''
// return the value 
function GetValue(Iv, Qa) {
    if (!Iv.value) { return '' }
    else if (Number(Iv.value) <= 0) { Iv.value = 1; return 1 }
    else if (!isNaN(Iv.value) & Boolean(Number(Iv.value))) {
        if (Number(Iv.value) > Number(Qa.textContent)) {
            Iv.value = Number(Qa.textContent);
            return Number(Qa.textContent);
        }
        else { return Number(Iv.value) }
    }
    else { Iv.value = 1; return 1 }
};

//manage prices 

function SetTotalCartPrice(){
    CartTotalPricelist['total'] = 0;
    for( let id in CartTotalPricelist ){
        result = (CartTotalPricelist[id].quantity * CartTotalPricelist[id].price)
        if (Boolean(result)){CartTotalPricelist['total']+= result};
    };
    TotalCartPrice.textContent = CartTotalPricelist['total'].toFixed(2);
    if((CartTotalPricelist['total'])){
        SetBtCoutRed(true)
    }else{

        SetBtCoutRed(false)
    };
};

// changing button checkout color red on if nothing in cart 
function SetBtCoutRed(value){
    if(value){
        CheckOut.classList.remove('worning_class')
    }else{
        CheckOut.classList.add('worning_class')
    };
};


function SetTpForItem(Id,Iv,Pp){
    CartTotalPricelist[Id] = {'quantity':(Number(Iv.value)),'price':Number(Pp.dataset.price)}
    
};


function GetTpForItem(Pp,Iv){
    return ((Number(Pp.dataset.price))*(Number(Iv.value)))
};

//add or substract quantity for each product 

function addRemoveProductQuantity(Id,Iv,Pp,Qa,Tp,Ck,operand) {
    let quantity = GetValue(Iv, Qa);
    const quantityAvailable = Number(Qa.textContent)
    if (operand === 'minus') { --quantity };
    if (operand === 'plus') { ++quantity };
    if (quantity > quantityAvailable) { quantity = Number(Qa.textContent)};
    if (quantity <= 0) { quantity = 1 };
    Iv.value = quantity;
    Tp.textContent = GetTpForItem(Pp,Iv).toFixed(2);
    DisplayErrorInput(Iv);
    SelectedProduct (Ck,Iv,Id,Pp)
};

// display red board of input field when is empty

function DisplayErrorInput(inputValue) {
    if (inputValue.value) {
        inputValue.classList.remove('border_style_error');
        inputValue.classList.add('border_style_default');
        return true;
    }
    else {
        inputValue.classList.remove('border_style_default');
        inputValue.classList.add('border_style_error');
        return false;
    }
}

// change quantity by input

function InitialInput(Id,Iv,Pp,Qa,Tp,Ck) {
    let quantity = GetValue(Iv, Qa);
    if (quantity){
        DisplayErrorInput(Iv);
    } else {
        DisplayErrorInput(Iv)
    };
    Tp.textContent = GetTpForItem(Pp,Iv).toFixed(2);
    SelectedProduct(Ck,Iv,Id,Pp);
};

// making total calculation of total product quantity per each item,
//and total price of the cart witch is selected when load the page

window.addEventListener('load', () => {
    const divElements = document.querySelectorAll('.detail_product_div')
    divElements.forEach(element => {
        const Pp = document.querySelector(`.product_price_${element.dataset.product_id}`);
        const Tp = document.querySelector(`.total_count_sum_${element.dataset.product_id}`);
        const Iv = document.querySelector(`#product_quantity_${element.dataset.product_id}`);
        const Ck = document.querySelector(`.check-input-${element.dataset.product_id}`);
        const Dp = document.querySelector(`#img_delete_${element.dataset.product_id}`);
        const Qa = document.querySelector(`#quantity_available_${element.dataset.product_id}`);
        const BtPlus = document.querySelector(`.plus_${element.dataset.product_id}`);
        const BtMinus = document.querySelector(`.minus_${element.dataset.product_id}`);
        //Pp.textContent = Number(Pp.textContent).toFixed(2);
        Tp.textContent = GetTpForItem(Pp,Iv).toFixed(2);
        SelectedProduct(Ck,Iv,element.dataset.product_id,Pp);
        

        Ck.addEventListener('click',()=>{
            SelectedProduct(Ck,Iv,element.dataset.product_id,Pp)
        });


        Dp.addEventListener('click',(event)=>{
            DeleteProduct(element.dataset.product_id)
            SendRequest(event,element.dataset.product_id)
            element.outerHTML = ''
        });


        BtPlus.addEventListener('click',()=>{
            addRemoveProductQuantity(element.dataset.product_id,Iv,Pp,Qa,Tp,Ck,'plus')
        });


        BtMinus.addEventListener('click',()=>{
            addRemoveProductQuantity(element.dataset.product_id,Iv,Pp,Qa,Tp,Ck,'minus')
        });


        Iv.addEventListener('keyup',()=>{
            InitialInput(element.dataset.product_id,Iv,Pp,Qa,Tp,Ck)
        });
    })
    
})

/* delete product from object */

function DeleteProduct(Id){
    if (CartTotalPricelist[Id]) {
        delete CartTotalPricelist[Id];
        SetTotalCartPrice();
    };
};

/* insert delete products from object */

function SelectedProduct (Ck,Iv,Id,Pp){
    if (Ck.checked) {
        DisplayErrorInput(Iv); SetTpForItem(Id,Iv,Pp);
    } else {DeleteProduct(Id)};
    SetTotalCartPrice();
}; 

// taking object inside of object >= return object id and quantity

function convertObject(file){
    delete file.total;
    ObjectList = {};
    for( let id in file){ObjectList[id] = file[id].quantity};
    return ObjectList;
};

function CreateJSON(file){return JSON.stringify(file);};

/*

function GetObjectToSend(file,value) {
    if(value ==='checkout'){
        return CreateJSON({'checkout':file})
    }else if(value ==='delete'){
        return CreateJSON({'delete':file})};
};
*/
// sent object when click checkout button

CheckOut.addEventListener('click', () => {
   
    if(CartTotalPricelist['total']){
        CheckOut.name = 'checkout'
        CheckOut.value = CreateJSON(convertObject(CartTotalPricelist))
    }else{
        CheckOut.name = 'delete'
        CheckOut.value = ''
    }
});


function SendRequest(event,ID) {
    event.preventDefault();
    $.ajax({
        type: 'POST',
        dataType: 'json',
        data: {
            delete:ID,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            if(response){
                console.log(response)
            }
        },
        failure: function (response) { alert('something went wrong'); }
    })
};


/*
function addProductToTheCart(event, trigger) {
    event.preventDefault();
    const data = CreateJSON(trigger);
    $.ajax({
        type: 'POST',
        dataType: 'json',
        data: {
            data:data,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            console.log(response)
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
};

BtAddProductToCart.addEventListener('click', (event) => {
    let trigger = false;
    addProductToTheCart(event, trigger)
})

BtRedirectToCart.addEventListener('click', (event) => {
    let trigger = true;
    addProductToTheCart(event, trigger)
})

*/