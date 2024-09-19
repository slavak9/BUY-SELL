let S = new FormData()
document.querySelectorAll(".sub_nav_div").forEach(e=>{
    //console.log(e.children[1].children)
    let ActionPubl = e.children[2].children[0].children[0].children[0]
    let ConfirmDelCont = e.children[1].children[0]
    let IMG = e.children[1].children[1].children[0]
    let DelBT = e.children[2].children[2].children[0]
    function ConfYes(){
        S.set('item_to_delete',e.children[2].dataset.reference)
        SendPost().then(x=>{
            if(!x){e.remove()}else{ConfirmDelCont.children[0].textContent = x}
        })
        S.delete('item_to_delete')};
    function ConfNo(){
        ConfirmDelCont.classList.remove('display_flex')
            ConfirmDelCont.classList.add('display_none')
            IMG.classList.remove('filter')
            this.removeEventListener('click',ConfNo)
    }
    DelBT.addEventListener('click',()=>{
        ConfirmDelCont.children[0].textContent = 'Are you sure you want to delete this item ?'
        IMG.classList.add('filter')
        ConfirmDelCont.classList.remove('display_none')
        ConfirmDelCont.classList.add('display_flex')
        let YES = e.children[1].children[0].children[1].children[0]
        YES.addEventListener('click',ConfYes)
        let No = e.children[1].children[0].children[1].children[1]
        No.addEventListener('click',ConfNo)
    })
    ActionPubl.addEventListener('change',()=>{
        S.set('set_publish',JsonCreate({'value':ActionPubl.name,'bool':ActionPubl.checked}))
        SendPost();
        S.delete('set_publish')
    })
    function JsonCreate(object) {
        return JSON.stringify(object)
    };
})


async function SendPost(){
const token = document.querySelector('#send_form_action input')
S.set(token.name,token.value)
let response = await fetch(window.location.href, {
    method: "POST",
    enctype:"multipart/form-data",
    body:S
    });
response = await response.json();
if(response['error']){
    console.log(response['error']);
    return response['error']
    
}else if(response['success']){
   console.log(response['success'])
}}
