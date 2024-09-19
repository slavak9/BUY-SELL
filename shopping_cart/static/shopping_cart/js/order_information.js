
const MainAddAddrButton = document.querySelector('.button_add_address')
const AddButtonInfoForm = document.querySelector('.button_send_form')
const AddressContainer = document.querySelector('.main_add_address_container')
const PhoneNumberField = document.querySelector('#id_phone_number')
//const AddressFormResponse = document.querySelector('#address_form_response')


let AddressFormObject
let CreditCartFormObject
let ProductsFileJson
let IsAddOrEdit = false


function CloseAddressWindow() { AddressContainer.style.display = 'none' };
function OpenAddressWindow() { AddressContainer.style.display = 'flex' };


//if (AddressFormResponse.value) {
  //  OpenAddressWindow()
//};

if (MainAddAddrButton) {
    MainAddAddrButton.addEventListener('click', () => { OpenAddressWindow() })
};

// phone input elaboration function (only numbers and plus permit to insert)

PhoneNumberField.addEventListener('keyup', (event) => {
    let phoneNumber = PhoneNumberField.value
    if (!phoneNumber.includes('+', 0) & !isNaN(event.key)) {
        PhoneNumberField.value = '+' + event.key.trim()
    } else if (isNaN(event.key) || event.key == ' ') {
        PhoneNumberField.value = phoneNumber.replace(event.key, '')
    }
})
// form address compile function, making json file 
function GetObjectForm() {
    const ObjectForm = {
        'country': '',
        'region': '',
        'locality_or_city': '',
        'street': '',
        'home_apartment': '',
        'postal_zip_code': '',
        'phone_number': '',
        'other_information': '',
    }
    return ObjectForm
};

function FormAddAddress() {
    const ObjectForm = GetObjectForm();
    for (let key in ObjectForm) {
        let variable = document.querySelector(`#id_${key}`)
        let TrimValue = (variable.value).trim()
        ObjectForm[key] = TrimValue
       // if (Boolean(TrimValue)) {
      //      ObjectForm[key] = TrimValue
     //   } else if (!Boolean(TrimValue) & key != 'other_information') {
     //       return false
       // };
    }
    return ObjectForm
};

function JsonCreate(object) {
    return JSON.stringify(object)
};
// send address form 
AddButtonInfoForm.addEventListener('click', () => {
    const addressForm = FormAddAddress()
    if (Boolean(IsAddOrEdit)) {
        addressForm['id'] = IsAddOrEdit
        AddButtonInfoForm.name = 'edit_form'
        AddButtonInfoForm.value = JsonCreate(addressForm)
        IsAddOrEdit = false
        CloseAddressWindow()
    } else if (!Boolean(IsAddOrEdit)) {
        AddButtonInfoForm.name = 'address_form'
        AddButtonInfoForm.value = JsonCreate(addressForm)
        CloseAddressWindow()
    } else {
        OpenAddressWindow()
    }; 
});

// send post request with a value return list of addresses
const ManageAddresses = document.getElementById('manage_addresses_button')
if(ManageAddresses){
ManageAddresses.addEventListener('click', () => {
    ManageAddresses.name = 'manage_addresses'
    ManageAddresses.value = true
});
}
   
// take each address form and modifyes it 
const ChosenAddressObject = {'chosen_address':''};
const DeleteAddressObject = {};

const divElements = document.querySelectorAll('.inner_change_address_container')
divElements.forEach(element => {
    const addresses_id = element.dataset.address_id
    const RadioChecked = document.querySelector(`#radio_${addresses_id}`)
    const DeleteButton = document.querySelector(`#delete_addresses_button_${addresses_id}`)
    const EditButton = document.querySelector(`#edit_addresses_button_${addresses_id}`)

    RadioChecked.addEventListener('click',()=>{
        ChosenAddressObject['chosen_address'] = addresses_id
    })

    // delite address
    DeleteButton.addEventListener('click', () => {
        DeleteAddressObject[`address_${addresses_id}`] = addresses_id
        element.style.display = 'none'
    })
    // compile filed in form (add address) end displays form
    EditButton.addEventListener('click', () => {
        const ListValue = GetObjectForm();
        for (let Val in ListValue) {
            let FormValue = document.querySelector(`#id_${Val}`);
            let DisplayValue = document.querySelector(`.id_${Val}_${addresses_id}`);
            FormValue.value = DisplayValue.textContent;
        };
        OpenAddressWindow();
        IsAddOrEdit = addresses_id
    })
})
const SaveModifiedAddresses = document.getElementById('save_addresses_button')
if (SaveModifiedAddresses) {
    SaveModifiedAddresses.addEventListener('click', () => {
    SaveModifiedAddresses.name = 'save_addresses'
    const ObjectToSend ={'delete_address':DeleteAddressObject,'chosen_address':ChosenAddressObject.chosen_address}
    SaveModifiedAddresses.value = JsonCreate(ObjectToSend)
    });
};

// close errors fields in address form, and adrress form it self

const ButtonCloseForm = document.querySelector('.button_send_close')
ButtonCloseForm.addEventListener('click',()=>{
    CloseAddressWindow()
    const errors = document.querySelector('.errorlist')
    if (errors){errors.style.display = 'none'}
});

const CloseAddressesModWindow = document.querySelector('.close_bt_addr_window')
if(CloseAddressesModWindow){CloseAddressesModWindow.addEventListener('click',()=>{
    document.querySelector('.outer_change_address_container').style.display = 'none'
})}

const CloseWInQuanMess = document.querySelector('.show_error_quantity_address')
if (CloseWInQuanMess){CloseWInQuanMess.addEventListener('click',()=>{
    CloseWInQuanMess.style.display = 'none'
})}