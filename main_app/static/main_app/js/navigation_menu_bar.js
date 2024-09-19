const ListMenu = document.querySelector('.left_bt_side') //input
const UserMenu = document.querySelector('.user_menu_ul') // input user menu

document.querySelector('body').addEventListener('click',(event)=>{
    if(event.target.id === 'menu-img-bt' & !ListMenu.classList.contains('display_block')){
        ListMenu.classList.remove('display_bar')
        ListMenu.classList.add('display_block')
        if(UserMenu){
        UserMenu.classList.add('display_none')}
   }
   else if(event.target.id === 'username-id-link'){
    if(UserMenu){
     UserMenu.classList.remove('display_none')}
     ListMenu.classList.add('display_bar')
     ListMenu.classList.remove('display_block')
   }
    else{
        ListMenu.classList.remove('display_block')
        ListMenu.classList.add('display_bar')
        if(UserMenu){
        UserMenu.classList.add('display_none')}
        //LanguageUL.classList.add('display_none')
    }
})

