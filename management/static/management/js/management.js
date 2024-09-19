const Category = document.querySelector('#list_cat_ul-c');
const SubCategory = document.querySelector('#list_cat_ul-i');
const CategoryPublished = document.querySelector('#id_is_published');
const CategorySubPublished = document.querySelector('#id_is_published_sub');
const InputCategory = document.querySelector('#id_name-category');
const InputSubCategory = document.querySelector('#id_name-sub-category');
const DropArea = document.querySelector('#drop-area-c');
const DropAreaI = document.querySelector('#drop-area-i');
const Wrap = document.querySelector('.wrapper_block_c');
let InputFileI = document.querySelector('#input-file-i');
let InputFileG = document.querySelector('#input-file-c');
let ImageSG = document.querySelector('#upload_img-c');
let ImageSI = document.querySelector('#upload_img-i');
let ImageTextG = document.querySelector('.img_text-c');
let ViewG = document.querySelector('#view_container-c');
let ImageTextI = document.querySelector('.img_text-i');
let ViewI = document.querySelector('#view_container-i');

QueriesLists = {'Category':{},'SubCategory':{}};


DropArea.addEventListener('mouseover',()=>{
   InitialImgLoad(InputFileG,ImageTextG,ImageSG,ViewG,true)
})
DropAreaI.addEventListener('mouseover',()=>{
   InitialImgLoad(InputFileI,ImageTextI,ImageSI,ViewI,false)
})


let PrivImg;
let PrivImgI;

function ChangeImg(url,Image,ImageText,View){
    Image.src = url
    ImageText.classList.add('display_none');
    View.classList.remove('background')
};

function ChangeRivImg(Image,ImageText,View,P){
    if(P){Image.src = P
    }else{
    Image.src = Image.dataset.image
    ImageText.classList.remove('display_none');
    View.classList.add('background')}
};


function InitialImgLoad(InputFile,ImageText,ImageS,View,T){
    if(InputFile){
        InputFile.addEventListener('change',UploadImg)
        // get src from InputFile and insert to the Image
    function UploadImg(){
        let ImgLink = URL.createObjectURL(InputFile.files[0]);
        ImageText.classList.add('display_none');
        View.classList.remove('background')
        ImageS.src = ImgLink;
        if(T){PrivImg = ImgLink}else{PrivImgI = ImgLink}
    };
    
    DropArea.addEventListener('dragover',(event)=>{
        event.preventDefault();
    });
    // on drop change InputFile.files
    DropArea.addEventListener('drop',(event)=>{
        event.preventDefault();
        InputFile.files = event.dataTransfer.files;
        UploadImg();
    });
    }; 
};


function FilterList(value,bool){
    let list;
    if(bool){list = Object.values(QueriesLists.Category)}else{
        list = Object.values(QueriesLists.SubCategory)
    }
    value = value.toLowerCase().trim()
    list.forEach(e=>{
        if(e.children[0].textContent.substr(0,value.length)===value){
            e.classList.remove('display_none')
            e.classList.add('display_flex')
        }else{
            e.classList.remove('display_flex')
            e.classList.add('display_none')}
    })
}


function ImgSearch(N){
    Object.values(QueriesLists.Category).forEach(e=>{
        if(e.children[1].children[0].dataset.id === N){
            ChangeImg(e.dataset.image,ImageSG,ImageTextG,ViewG)
        }
    })
};

Wrap.addEventListener('mouseover',()=>{
    Category.classList.remove('display_none')
})

Wrap.addEventListener('mouseout',()=>{
    Category.classList.add('display_none')
})

document.querySelectorAll('.name-category-type').forEach(e=>{
    let chosen = e.children[1].children[0]
    QueriesLists.Category[chosen.dataset.id] = e})


document.querySelectorAll('.name-category-type-i').forEach(e=>{
    let chosen = e.children[1].children[0]
    QueriesLists.SubCategory[chosen.dataset.id] = e})


document.querySelector('.wrapper_block_c').addEventListener('mouseenter',()=>{
    let CategorySearch = document.querySelector('#search_bar_cat')
    CategorySearch.addEventListener('keyup',()=>{
        FilterList(CategorySearch.value,true)
    })
})
   

Category.addEventListener('mouseleave',()=>{
    if(InputFileG.files[0]){
        ImageSG.src = URL.createObjectURL(InputFileG.files[0])
    }else{ChangeRivImg(ImageSG,ImageTextG,ViewG,PrivImg)}
    Category.classList.remove('display_block')
})


document.querySelector('.wrapper_block_i').addEventListener('mouseenter',()=>{
    let CategorySearch = document.querySelector('#search_bar_it')
    CategorySearch.addEventListener('keyup',()=>{
        FilterList(CategorySearch.value,false)
    })
})

// Categories bock: 
Object.values(QueriesLists.Category).forEach(e=>{
    e.children[1].children[1].children[0].addEventListener('click',()=>{
    document.querySelector('#head-h4-c').textContent=e.textContent;
    PrivImg = e.dataset.image;
    CategorySubPublished.dataset.category = e.children[1].children[0].dataset.id
    })
    e.children[1].children[0].addEventListener('click',()=>{
        InputCategory.value = e.children[1].children[0].dataset.name;
        InputCategory.name = e.children[1].children[0].dataset.id;
        CategoryPublished.checked = true ? e.children[1].children[0].dataset.published === 'True' : false;
    })
    e.addEventListener('mouseover',()=>{
        setTimeout(()=>{
        ChangeImg(e.dataset.image,ImageSG,ImageTextG,ViewG)}, 1);
        });    
})



// Sub Categories bock: 
Object.values(QueriesLists.SubCategory).forEach(e=>{
    // show image that belong to sub category on click
    e.addEventListener('click',()=>{
    ImgSearch(e.dataset.id)
    })
    // set param in Sub Category on click edit icon of the sub category
    e.children[1].children[0].addEventListener('click',()=>{
        InputSubCategory.value = e.children[1].children[0].dataset.name;
        InputSubCategory.name = e.children[1].children[0].dataset.id;
        CategorySubPublished.checked = true ? e.children[1].children[0].dataset.published === 'True' : false;
        CategorySubPublished.dataset.sub_category = e.dataset.id;
        GetModelFields({'slug': e.children[1].children[0].dataset.slug,'id':e.dataset.id},e.children[1].children[0].dataset.name)
    })
    // show previews image
    e.addEventListener('mouseover',()=>{
        setTimeout(()=>{
        ChangeImg(e.dataset.image,ImageSI,ImageTextI,ViewI)}, 1)
    })
});




SubCategory.addEventListener('mouseleave',()=>{
    if(InputFileI.files[0]){
        ImageSI.src = URL.createObjectURL(InputFileI.files[0])
    }else{
        ChangeRivImg(ImageSI,ImageTextI,ViewI,PrivImgI)
        ChangeRivImg(ImageSG,ImageTextG,ViewG,PrivImg)
    }
})

function JsonCreate(object) {
    return JSON.stringify(object)
};


let FieldList = {}
let SubChoiceF = {}
let N = new FormData()
const MesDiv = document.querySelector('#error_mess_category')
const MesSubDiv = document.querySelector('#error_mess_sub_category')

function LFields(){
    for(let name in SubChoiceF){
        FieldList[SubChoiceF[name].field] = {'type':'string','fields':[]}
    };
};

// prepare all data too be send when click Create Category button
document.querySelector('#cat_send_bt').addEventListener('click',()=>{
    if(!InputCategory.value){InputCategory.focus();return}
    if(!InputFileG.files[0]){
        InputFileG.focus();
        MesDiv.innerHTML='<ul><li>Please upload image!</li></ul>'
        return}
    N.set('create_category', JsonCreate({'name':InputCategory.value.trim(),'is_published':CategoryPublished.checked}))
    N.set('file',InputFileG.files[0],InputFileG.value)
    SendPost(true)
    N.delete('create_category')
    N.delete('file')
})
// prepare all data too be send when click Edit Category button
document.querySelector('#cat_edit_bt').addEventListener('click',()=>{
    if(!InputCategory.value){InputCategory.focus();return}
    if(!InputCategory.name){return}
    N.set('edit_category', JsonCreate({'id':InputCategory.name,'name':InputCategory.value.trim(),'is_published':CategoryPublished.checked}))
    if(InputFileG.files[0]){N.set('file',InputFileG.files[0],InputFileG.value)}
    SendPost(true)
    N.delete('edit_category')
    N.delete('file')
})
// prepare all data too be send when click Create Sub Category button
document.querySelector('#cat_item_send_bt').addEventListener('click',()=>{
    if(!InputSubCategory.value){InputSubCategory.focus();return}
    if(!CategorySubPublished.dataset.category){Category.classList.remove('display_none');window.location.href='#head-h4-c';return}
    if(!InputFileI.files[0]){
        InputFileI.focus();
        MesSubDiv.innerHTML='<ul><li>Please upload image!</li></ul>';
        return}
   // LFields()
    N.set('create_item_category', JsonCreate({'name':InputSubCategory.value.trim(),'is_published':CategorySubPublished.checked,'category_id':CategorySubPublished.dataset.category}))
    N.set('fields',JsonCreate(FieldList))
    N.set('fields_sub_choices',JsonCreate(SubChoiceF))
    N.set('file',InputFileI.files[0],InputFileI.value)
    SendPost(false)
    N.delete('create_item_category')
    N.delete('file')
})
// prepare all data too be send when click Edit Sub Category button
document.querySelector('#cat_sub_edit_bt').addEventListener('click',()=>{
    if(!InputSubCategory.name){return}
    if(!InputSubCategory.value){InputSubCategory.focus();return}
    if(!CategorySubPublished.dataset.sub_category){Category.classList.remove('display_none');window.location.href='#head-h4-c';return}
  //  LFields()
    N.set('edit_item_category', JsonCreate({'id':InputSubCategory.name,'name':InputSubCategory.value.trim(),'is_published':CategorySubPublished.checked,'category_id':CategorySubPublished.dataset.sub_category}))
    N.set('fields',JsonCreate(FieldList))
    N.set('fields_sub_choices',JsonCreate(SubChoiceF))
    if(InputFileI.files[0]){N.set('file',InputFileI.files[0],InputFileI.value)}
    SendPost(false)
    N.delete('edit_item_category')
    N.delete('file')
    
})

const Sdiv = document.querySelector('.cat_block_div-wrapper');
const Vdiv = document.querySelector('.div_s_l_o_a_i');
const TitleField = document.querySelector('.title_o_t_f');
const LIST = document.querySelector('.show_list_of_add-items');
const NameField = document.querySelector('#add_item_field');
let Fname;
let Fvalue;
//initial load sub filed from file on add button click
document.querySelector('#action_add-sub_f').addEventListener('click',()=>{
const file = document.querySelector('#file_names_select-items')
    if(Boolean(NameField.value.trim())){
        const E = document.querySelector('.Err_file-mes')
        if(file.files[0] && file.files[0].type === 'text/plain'){
            FileReaderTXT(file,GetHTMLFieldsItem,NameField,LIST)
            E.classList.add('display_none')
        }else{
          E.classList.remove('display_none')
        }
    }else{
        NameField.focus()
    }
})
 

// loads sub fields for field of the sub category if exist
function LoadSFIFE(){
    let HTML = '';
    Fname = TitleField.textContent.slice(0,TitleField.textContent.indexOf('('));
    Fvalue = TitleField.textContent.slice(TitleField.textContent.indexOf('(')).replace('(','').replace(')','')
    if (SubChoiceF[Fname]){
        let objL = SubChoiceF[Fname]
        if(objL[Fvalue]){
            objL[Fvalue].forEach(e=>{
                HTML += HTMLStrItem(LIST,e)})
            LIST.innerHTML = HTML
        }
        NameField.value = objL.field;
    }
    LoadSubField()  
};
// loads fields in list or remove from list
let ListF;
function LoadSubField(){
    ListF = [];
    document.querySelectorAll('.show_list_of_add-items li').forEach(e=>{
        ListF.push(e.children[0].children[0].textContent)
        e.children[1].children[0].addEventListener('click',()=>{
            ListF.splice(ListF.indexOf(e.children[0].children[0].textContent),1)
            e.remove()
        })
    })}
    // close window on click button close sub field for category sub field
document.querySelector('#close-sub-win').addEventListener('click',()=>{
    let objK = SubChoiceF[Fname]
    if (objK){
        if(Boolean(NameField.value.trim())){
            objK.field = NameField.value
        }else{NameField.focus()}
        if(ListF.length > 0){
            objK[Fvalue] = ListF}else{
            delete objK[Fvalue];
            if(Object.keys(objK).length < 2){
                delete SubChoiceF[Fname]
            }
        }
    }else{
        if(ListF.length > 0){
        let x = {}
        x[Fvalue] = ListF
        x['field'] = NameField.value
        SubChoiceF[Fname] = x}
    }
    Vdiv.classList.remove('display_initial')
    Vdiv.classList.add('display_none')
    Sdiv.classList.remove('display_none')
    Sdiv.classList.add('display_initial')
    LIST.innerHTML = '';
    ListF = [];
    NameField.value = '';
});


// create fields of sub choices for field of select
function GetHTMLFieldsItem(text,name,LIST){
    let HTML = '';
    text.replace('\n','').split(',').forEach(n=>{
        n = n.replace('\n','')
        n = n.trim()
        if(Boolean(n)){
            HTML += HTMLStrItem(LIST,n)
        }
    })
    LIST.innerHTML = HTML;
    LoadSubField()
}


// remove model sub category field, on list click open sub field window
function LoadFields(){
    FieldList = {}
    document.querySelectorAll('.show_list_of_add li').forEach(e=>{
        let Name = e.children[0].children[0].textContent;
        let Type = e.children[0].children[2].textContent;
        let Field;
        if(Type === 'select'){
            Field = Name.slice(Name.indexOf('(')).replace('(','').replace(')','')
            Name = Name.slice(0,Name.indexOf('('))
        } 
        if (FieldList[Name]){
            FieldList[Name].fields.push(Field);
        }else{
            FieldList[Name] = {'type':Type,'fields':[]};
            if(Field){FieldList[Name].fields.push(Field)};
        }
        e.children[1].children[1].addEventListener('click',()=>{
            if(FieldList[Name].fields.length > 1){
                FieldList[Name].fields.splice(FieldList[Name].fields.indexOf(Field),1);
            }else{
                delete FieldList[Name]
            }
            e.remove();
        })
        
        e.children[1].children[0].addEventListener('click',()=>{
            Sdiv.classList.add('display_none')
            Vdiv.classList.remove('display_none')
            Vdiv.classList.add('display_initial')
            TitleField.textContent = e.children[0].children[0].textContent
            LoadSFIFE()
        })
    })   
};


// show input file element on chose select option
const ShowFInput = document.querySelector('#display-files-select');
let SelectedRType;
document.querySelectorAll('.input_name_t li input').forEach(e=>{
    e.addEventListener('change',()=>{
        if(e.id === 'select' && e.checked){
            ShowFInput.classList.remove('display_none')
        }else{
            ShowFInput.classList.add('display_none')
        }
        SelectedRType = e
    })
});

// return LI html code field on adding sub field
function HTMLStr(name,LIST,n){
    return  `<li><div>
            <span class="spn-1">${name.value.toLowerCase()}${n ? "("+ n.toLowerCase().trim() +")" : ""}</span><b>:</b>
            <span class="spn-2">${SelectedRType.id}</span>
        </div><div class="select_del_list-img">
        <img class='img_spn_3' src="${LIST.dataset.image}" title="Add list">
        <img class='img_spn_3' src="${LIST.dataset.img}" title="Delete"></div></li>`
}
function HTMLStrItem(LIST,n){
    return  `<li><div>
            <span class="spn-1">${n.toLowerCase()}</span>
        </div><div class="select_del_list-img">
        <img class='img_spn_3' src="${LIST.dataset.img}" title="Delete"></div></li>`
}

// make from txt file sub category fields
function GetHTMLFields(text,name,LIST){
    let HTML = '';
    text.replace('\n','').split(',').forEach(n=>{
        n = n.replace('\n','')
        if(Boolean(n.trim())){
            HTML += HTMLStr(name,LIST,n)
        }
    })
    SelectedRType.checked = false;
    name.value = ''
    LIST.innerHTML += HTML;
    ShowFInput.classList.add('display_none')
    LoadFields();
};

//reading txt file loaded and initialize passed function
function FileReaderTXT(File,func,name,LIST){
    const reader = new FileReader();
    reader.onload = function () {
        result = reader.result;
        func(result,name,LIST)
        File.value = null
    };
    reader.onerror = function () {
        console.error('Error reading the file');
    };
    reader.readAsText(File.files[0], 'utf-8');
};



// creates model fields html by click plus button, to being process for creating fields
document.querySelector('#action_add-name').addEventListener('click',()=>{
    let HTMLtext;
    let name = document.querySelector('#add_type_field')
    let LIST = document.querySelector('.show_list_of_add')
    const File = document.querySelector('#file_names_select')
    const error = document.querySelector('.Err_file-mes-sel')
    error.classList.add('display_none')
    if(Boolean(name.value.trim())){
        if(File.files[0] && SelectedRType.id === 'select'){
            if(File.files[0].type === 'text/plain' ){
                FileReaderTXT(File,GetHTMLFields,name,LIST)
            }else{
                error.classList.remove('display_none')
                error.textContent = 'File error: make sure that file is .txt format'
                return
                }
        }
        else if(SelectedRType && SelectedRType.checked){
            if(SelectedRType.id === 'select' && !name.value.includes('(') && !name.value.includes(')')){
                error.classList.remove('display_none')
                error.innerHTML = 'Select error: make sure that text having right format. <b>name(value)</b>'
                name.focus()
                return
            }
            HTMLtext= HTMLStr(name,LIST,false)
            SelectedRType.checked = false
    }}else{name.focus()}

    if(HTMLtext){
        LIST.innerHTML+= HTMLtext
        name.value = ''
    }
    ShowFInput.classList.add('display_none')
    LoadFields()
});


function DisplayError(ErrorObj,bool){
    if(!ErrorObj){return};
    let text = '';
    let n = 0;
    for(let i in Object(ErrorObj)){
            n++
            text += `<li>${n}. ${i.toUpperCase()} ERROR: ${ErrorObj[i][0]}</li>`};
    text = `<ul>${text}</ul>`;
    if(bool){MesDiv.innerHTML = text}else{MesSubDiv.innerHTML = text};
   
};


function GetModelFields(obj,name){
    N.set('request_model_fields', JsonCreate(obj))
    SendPost(name)
    N.delete('request_model_fields')

};

const ExistingFields = document.querySelector('#dis-fi-s-cat')
function DisplayFields(obj,n){
    let Html = ''
    if(obj != 'None'){
    for(let i in obj){
        Html+= `<li><b>${i[0].toUpperCase() + i.slice(1)}:</b> ${obj[i]}</li>\n`
    }
    Html = `<h4> Already existing sub categories fields for ${n[0].toUpperCase() + n.slice(1)} :</h4>\n<ul>${Html}</ul>`
    }
    ExistingFields.innerHTML = Html
};


async function SendPost(bool){
    const token = document.querySelector('#input_s-1-cs').children[2]
    N.set(token.name,token.value)
    let response = await fetch(window.location.href, {
        method: "POST",
        enctype:"multipart/form-data",
        body:N
        });
    response = await response.json();
    if(response['error']){
        DisplayError(response['error'],bool)
    }else if(response['success']){
        DisplayError(false,bool)
       window.location.reload()
    }else if(response['category']){
        DisplayFields(response['category'],bool)
    }
}
