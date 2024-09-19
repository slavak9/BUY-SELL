
const CategoryButton = document.querySelector('.button_ch_cat_div button')
const ContainerCategory = document.querySelector('.sub_chose_category')
const HeaderH3 = document.querySelector('.h3-chosen_cat')
const RadioInputValue = {};


// save or delete header element as old or new value, for open or close list window 
function ManageHeaderValue(element){
if(RadioInputValue['header_value']){
    if(RadioInputValue['header_value'] === element){
        CloseList(element.dataset.header);
        RadioInputValue['header_value'] = false;
    }else{
        CloseList(RadioInputValue['header_value'].dataset.header);
        OpenList(element.dataset.header);
        RadioInputValue['header_value'] = element
    };
}else{
    OpenList(element.dataset.header);
    RadioInputValue['header_value'] = element
}
};
// return object for img up and down list
function GetObjectList(id){
    return {'list':document.querySelector(`#list_${id}`),
            'img_down':document.querySelector(`.img_down_${id}`),
            'img_up':document.querySelector(`.img_up_${id}`)}
};
    // close category drop-down list window 
function CloseList(id){
    data = GetObjectList(id)
    data.list.classList.remove('display_block');
    data.img_up.classList.add('display_none');
    data.img_down.classList.remove('display_none');
};
    // open category drop-down list window 
function OpenList(id){
    data = GetObjectList(id)
    data.list.classList.add('display_block');
    data.img_down.classList.add('display_none');
    data.img_up.classList.remove('display_none');
};

// close chosen category window 
function CloseCatContainer(){
    ContainerCategory.classList.add('display_none');
    HeaderH3.classList.remove('display_none')
};
    // open chosen category window 
function OpenCatContainer(){
    ContainerCategory.classList.remove('display_none')
    HeaderH3.classList.add('display_none')
};

// take chosen item text and sets it in header container of the list column and style 
function UnsetHName(){
    let HeaderName = document.querySelector(`#header_${RadioInputValue['value_element'].name}`)
    HeaderName.textContent = RadioInputValue['name'];
    HeaderName = document.querySelector(`#header_container_${RadioInputValue['value_element'].name}`)
    HeaderName.classList.remove('header_chosen_style');
};
// close searchbar when item is selected
function CloseInputField(){
    RadioInputValue['search_value'].forEach(item =>{
        item.value = ''
    })
};

// take header container and set privies text and style  
function SetHName(element){
    let HeaderName = document.querySelector(`#header_${element.name}`);
    RadioInputValue['name'] = HeaderName.textContent;
    HeaderName.textContent = element.value;
    HeaderName = document.querySelector(`#header_container_${element.name}`);
    HeaderName.classList.add('header_chosen_style');
    if(RadioInputValue['header_value']){
    CloseList(RadioInputValue['header_value'].dataset.header)};
    CloseList(element.name);
    HeaderH3.textContent = element.value;
    CloseCatContainer();
    FilterList(element,false);
    CloseInputField();
};

// insert delete item in the object and check uncheck chosen element   

function SetElement(element){
    GetCategoryFields(element)
    if(RadioInputValue['value_element']){
        RadioInputValue['value_element'].checked = false
        UnsetHName()
        element.checked = true
        RadioInputValue['value_element'] = element
        SetHName(element)
    }else{
        element.checked = true
        RadioInputValue['value_element'] = element
        SetHName(element)
    }
    
};

// making objects of category
// making list of items for each category
// set chosen item as value_element
// listening on click to set chosen value
let OldSl
function SetSearchObject(){
    const divElements = document.querySelectorAll('.items_category_container')
    divElements.forEach(element =>{
        let Element = document.querySelectorAll(`.class-id_${element.dataset.container}`)
        RadioInputValue[element.dataset.container] = Element
        Element.forEach(e =>{
            if(e.checked){
                RadioInputValue['value_element'] = e;
                OldSl = {'slug': e.dataset.slug,'category':e.dataset.category}
                SetHName(e)
            };
            e.addEventListener('click',()=>{
                SetElement(e)
            });
        })
        
    })
};


function OpenCloseListWindow(){
    const divElements = document.querySelectorAll('.item_list_header')
    divElements.forEach(element => {
        element.addEventListener('click',()=>{
            ManageHeaderValue(element)
        })
    })
};
// filtering items for each list, and show only filtered items
function FilterList(element,bool){
    let listA = RadioInputValue[element.name];
    let value ;
    if(bool){value = element.value.toLowerCase().trim()}else{value = ''};
    if(Boolean(value)){
        listA.forEach(item =>{
            if((item.value.substr(0,value.length)===value)){
                document.querySelector(`.label_input_${item.id}`).classList.remove('display_none')
            }else{
                document.querySelector(`.label_input_${item.id}`).classList.add('display_none')
            }})
    }else{
        listA.forEach(item =>{
            document.querySelector(`.label_input_${item.id}`).classList.remove('display_none')
        })
            }
};
// takes all input fields in category items 
function InputSearch(){
    const input = document.querySelectorAll('.search_bar_input')
    let ItElement = [];
    input.forEach(element =>{
        element.addEventListener('focus',()=>{
            element.addEventListener('keyup',()=>{
                FilterList(element,true)})           
        })
        ItElement.push(element);
    })
    RadioInputValue['search_value'] = ItElement;
};
// initial function
window.addEventListener('load', () => {
    OpenCloseListWindow();
    InputSearch();
    SetSearchObject();
    GetImgListDiv();
    GetImgListDiv1();
})
// open category window 
CategoryButton.addEventListener('click',()=>{
    OpenCatContainer()
});

// close item category window
ContainerCategory.addEventListener('mouseleave',()=>{
    if(RadioInputValue['header_value']){
        CloseList(RadioInputValue['header_value'].dataset.header);};
});



// img block------------------------------------------------------------------------------

// function get list of main images elements for each image container and passes to SetImg function
function DStyle(L,I){
    const S = document.querySelector(`${I}`)
    if(L>1){
        S.classList.remove('display_flex')
        S.classList.add('display_grid')
    }else{
        S.classList.remove('display_grid')
        S.classList.add('display_flex')
    }
}


const ExCount = document.querySelector('.titles-des')
let ImgSource = document.querySelector('#add_img_files-id').dataset.img;
let count = 1;
if(Number(ExCount.dataset.count)){count = Number(ExCount.dataset.count)}
const ValuesCR = document.querySelector('.title-descrip-d')
let ExCount1 = Number(ValuesCR.dataset.count)
let Rows = Number(ValuesCR.dataset.row)-1
let count1 = 1;
if(ExCount1){count1 = ExCount1}
let selectedIMg;
function GetImgListDiv(){
    let x = document.querySelectorAll('.img-con-div')
    DStyle(x.length,'.add_img_files');
    x.forEach(element =>{
        let DropArea = document.querySelector(`#drop-area-${element.dataset.numb}`);
        let InputFile = document.querySelector(`#input-file-${element.dataset.numb}`);
        let ImageText = document.querySelector(`.img_text-${element.dataset.numb}`);
        let Image = document.querySelector(`#upload_img-${element.dataset.numb}`);
        let View = document.querySelector(`#view_container-${element.dataset.numb}`);
        let DeleteBt = document.querySelector(`#delete-img-${element.dataset.numb}`);
        let SelectedAsMain = document.querySelector(`#input_im-${element.dataset.numb}`)
        let NumCount = document.querySelector(`#span-num-${element.dataset.numb}`)
        NumCount.textContent = (Number(ExCount.dataset.limit)+1)-x.length
        SetMainImg(SelectedAsMain,InputFile);
        // delete img div container
        DeleteBt.addEventListener('click',()=>{
            DelMainImg(InputFile.id)
            element.remove();
            if(SelectedAsMain == selectedIMg){
                selectedIMg = NaN;
            }
            AddImgWindow(ImgSource,'add_img_files-id','',0);
            GetImgListDiv();
        });
        SetImg(InputFile,DropArea,ImageText,Image,View,x.length,element.dataset.numb,ImgSource,'add_img_files-id','',0);
      
});
if(!selectedIMg.checked){
    selectedIMg.checked = true;}
};

// set radio input checked for main img

function SetMainImg(SelectedAsMain){
    if(!selectedIMg){
        selectedIMg = SelectedAsMain}
    if(SelectedAsMain.checked){
        selectedIMg = SelectedAsMain
    }else if(selectedIMg.id === SelectedAsMain.id && selectedIMg.checked){
        SelectedAsMain.checked = true
    }
    SelectedAsMain.addEventListener('click',()=>{
        SelectedAsMain.checked = true
        selectedIMg = SelectedAsMain
    });
};


function SetImg(InputFile,DropArea,ImageText,Image,View,l,n,Im,I,D,L){
    if(InputFile){
        InputFile.addEventListener('change',UploadImg)
        // get src from InputFile and insert to the Image
    function UploadImg(){
        let ImgLink = URL.createObjectURL(InputFile.files[0]);
        Boolean(L) ? SetDesImgFiles(InputFile,Image.dataset.numb):SetMainImgFiles(InputFile);
        ImageText.classList.add('display_none');
        Image.classList.add('width-100');
        View.classList.remove('background')
        Image.classList.add('display_full');
        Image.src = ImgLink;
        Image.dataset.bool = 1;
        let HTMLImgCon = document.querySelector(`#action-img${D}-${n}`)
        HTMLImgCon.classList.remove('display_none')
        HTMLImgCon.classList.add('display_flex')
        let HTMLnumberLeft = document.querySelector(`#span-num${D}-${n}`)
        HTMLnumberLeft.classList.add('display_none')
        if(Boolean(L)){
            if(DelExtraImgWin() <= (Number(ValuesCR.dataset.limit)-1)){AddImgWindow(Im,I,D,L)};
        }else{
            if(l <= (Number(ExCount.dataset.limit)-1)){AddImgWindow(Im,I,D,L)};
        }
        if(InputFile.name || InputFile.dataset.value){
            InputFile.name = ''
            InputFile.dataset.value = ''
        }
        
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


// return HTML source for additional img

function GetHtmlMainSelect(C){
    let X = `<div class="make-main-img">
    <label for="input_im-${C}" class="check_box_item_container">
        <input id="input_im-${C}" class="check-input-${C}" type="radio" name="sek-main-img">
        <img id="unchecked-pic-${C}" class="unchecked" src="/static/user_personal_area/img/not-photo-gallery.png" alt="checked png" title="Set as main avatar">
        <img id="checked-pic-${C}" class="checked" src="/static/user_personal_area/img/photo-gallery.png" alt="checked png" title="Main avatar">
        </label>
    </div>`
    return X
}

function GetHtmlImg(Im,D,C,CL,L){
    C +=1;
    let text = `<div class="img-con-div${D}" id="img-file${D}-${C}" data-numb="${C}">
                    <label for="input-file${D}-${C}" id="drop-area${D}-${C}">
                        <input id="input-file${D}-${C}" class="input-f-c" type="file" accept="image/*" hidden>
                        <div id="view_container${D}-${C}" class="img_view_container${D} background">
                            <div id="dis-numb${D}-${C}" class="display_number_count"><span id="span-num${D}-${C}"></span></div>
                            <img src="${Im}" alt="upload img" id="upload_img${D}-${C}" class="${CL}" data-numb="${L}" data-bool="0">
                            <p class="img_text${D}-${C} img_text-p">Drag and drop, or click here <br>to upload image</p>
                        </div>
                    </label>

                    <div id="action-img${D}-${C}" class="action-img-div display_none">
                    ${Boolean(D) ? "": GetHtmlMainSelect(C)}
                    <div class="delete-img"><img id="delete-img${D}-${C}" src="/static/user_personal_area/img/trash.png" title="Delete image"></div>
                    </div> 
                </div>`;
    Boolean(D) ? count1 = C : count = C
return text
}
// return the last img element
function GetRecInfo(n){
    const ImageInfo = document.querySelector(`#upload_img-${n}`)
    if(!ImageInfo){
       return GetRecInfo(n-=1)
    }else{ 
        return ImageInfo
    };
};

// ADD HTML source for additional img  f-descrip-d-${L}
// ImgSource,`f-descrip-d-${e.dataset.numb}`,'-des',e.dataset.numb
function AddImgWindow(Im,I,D,L){
    const ImageCon = document.querySelector(`#${I}`); 
    let x = Boolean(D) ? count1: count
    if(Boolean(L)){
        let Y = document.querySelectorAll(`.img-count-data-${L}`)
        if(Y.length && 0 != Number(Y[Y.length-1].dataset.bool)){
            ImageCon.innerHTML += GetHtmlImg(Im,D,x,`img-count-data-${L}`,L);
            GetImgListDiv1()
        }else if(!Y.length){
            ImageCon.innerHTML += GetHtmlImg(Im,D,x,`img-count-data-${L}`,L);
            GetImgListDiv1()
        }
    }else{
        let Y = document.querySelectorAll(`.img-count-dt-${L}`)
        if(0 != Number(Y[Y.length-1].dataset.bool)){
            ImageCon.innerHTML += GetHtmlImg(Im,D,x,`img-count-dt-${L}`,L);
            GetImgListDiv()
        }}
}
//end block-----------------------------------------------------------------------------------------------

// video block --------------------------------------------------------------------------------------------
const InputFileV = document.querySelector('#input-video-file');
function SetVideo(){
    let DropAreaV = document.querySelector('#drop-video-file');
    let ImageV = document.querySelector('#view_video_container');
    let VideoContainer = document.querySelector('#dp-cat');
    let VideoSource = document.querySelector('#video-source-cat');
    let DelButton = document.querySelector('.video_del_bt_div')
    let ErrorSize = document.querySelector('.error_file_size')
    if(DelButton){
    DelButton.addEventListener('click',()=>{
        ErrorSize.classList.add('display_none')
        InputFileV.value = ''
        DelVideoFiles(InputFileV)
        InputFileV.dataset.value = 'delete'
        DelButton.classList.remove('display_flex')
        DelButton.classList.add('display_none')
        VideoContainer.classList.add('display_none');
        VideoContainer.load();
    })}
    if(InputFileV){
        InputFileV.addEventListener('change',UploadImg)
        // get src from InputFile and insert to the Image
        function UploadImg(){
        if(InputFileV.files[0].size < 500000000){
        ErrorSize.classList.add('display_none')
        let VideoLink = URL.createObjectURL(InputFileV.files[0]);
        ImageV.classList.add('display_full');
        VideoSource.src = VideoLink;
        InputFileV.dataset.value = 'delete'
        SetVideoFiles(InputFileV);
        //ImageV.classList.add('display_none')
        VideoContainer.classList.remove('display_none');
        DelButton.classList.remove('display_none')
        DelButton.classList.add('display_flex')
        VideoContainer.load();}else{
            ErrorSize.innerHTML = 'File must be less than 500Mbyte'
            ErrorSize.classList.remove('display_none')
        }
    };
    DropAreaV.addEventListener('dragover',(event)=>{
        event.preventDefault();
    });
    // on drop change InputFile.files
    DropAreaV.addEventListener('drop',(event)=>{
        event.preventDefault();
        InputFileV.files = event.dataTransfer.files;
        UploadImg();
    });
    }; 
};

SetVideo();
///////////////////////////////////////////////////////////////////////////////////////////////////
// block table elements
function GetTH(st){
    return `<th>${st.charAt(0).toUpperCase()+st.slice(1)}</th>`
}
function GetTD(st){
    return `<td>${st}</td>`
}
// clears table fields 
const ClearSpecification = document.querySelector('#bt-clear-spec')
ClearSpecification.addEventListener('click',()=>{
    let TRH = GetTRowH();
    let TRD = GetTRowD();
    if((GetTable().children.length/2) == 1){
        TRH.innerHTML = '';
        TRD.innerHTML = '';
    }else{
        TRH.outerHTML = '';
        TRD.outerHTML = '';
    }
}) 
// create table fields 
const AddSpecification = document.querySelector('#bt-add-spec')
AddSpecification.addEventListener('click',()=>{
    const inT = document.querySelector('#te-of-sp');
    const inTS = document.querySelector('#te-de-of-sp');
    !Boolean(inT.value.trim()) ? inT.focus() : !Boolean(inTS.value.trim()) ? inTS.focus() : NaN;
    if(Boolean(inT.value.trim()) && Boolean(inTS.value.trim())){
        if(GetTRowH().children.length <= 2){
            SetTRHD(inT,inTS)
        }else{
            let table = GetTable()
            table.innerHTML+= `<tr id="tr-1-sp-${(table.children.length/2)+1}"></tr><tr id="tr-2-sp-${(table.children.length/2)+1}"></tr>`;
            SetTRHD(inT,inTS);
        }}
})
function GetTable(){
    return document.querySelector('.table-style-c tbody')
};
function GetTRowH(){
    return document.querySelector(`#tr-1-sp-${GetTable().children.length/2}`)
};
function GetTRowD(){
    return document.querySelector(`#tr-2-sp-${GetTable().children.length/2}`)
};
function SetTRHD(inT,inTS){
    GetTRowH().innerHTML+= GetTH(inT.value.trim()).trim();
    GetTRowD().innerHTML+= GetTD(inTS.value.trim()).trim();
    inT.value = '';
    inT.focus();
    inTS.value = '';
}
// end block table

// function get list of description images elements for each image container and passes to SetImg function

let WinNumb = (Number(ValuesCR.dataset.limit)+1)
if(Rows){WinNumb+=Rows}
function GetImgListDiv1(){
    let x = document.querySelectorAll('.img-con-div-des');
    LF().forEach(e=>{DStyle(e.children.length,`#${e.id}`)});
    x.forEach(element =>{
        let DropArea = document.querySelector(`#drop-area-des-${element.dataset.numb}`);
        let InputFile = document.querySelector(`#input-file-des-${element.dataset.numb}`);
        let ImageText = document.querySelector(`.img_text-des-${element.dataset.numb}`);
        let Image = document.querySelector(`#upload_img-des-${element.dataset.numb}`);
        let View = document.querySelector(`#view_container-des-${element.dataset.numb}`);
        let DeleteBt = document.querySelector(`#delete-img-des-${element.dataset.numb}`);
        let NumCount = document.querySelector(`#span-num-des-${element.dataset.numb}`)
        NumCount.textContent = WinNumb-x.length
        // delete img div container
        DeleteBt.addEventListener('click',()=>{
            DelDesImg(`part-${Image.dataset.numb}:${InputFile.id}`);
            element.remove();
            AddForEachWin();
            GetImgListDiv1();
        });
        // set source img
        
        SetImg(InputFile,DropArea,ImageText,Image,View,x.length,element.dataset.numb,ImgSource,`f-descrip-d-${Image.dataset.numb}`,'-des',Image.dataset.numb);
     
});
};
// end ----------------------------------------------------------------------------------------------------

// this function return html code for new description end if it is necessary return img html code

function GetHtmlDes(L,F){
    let S = GetHtmlImg(ImgSource,'-des',count1,`img-count-data-${L}`,L)
    let X =`<div id="it-descript-di-${L}" class="it-descript-d" data-numb="${L}">
                <div id="i-descrip-d-${L}" class="i-descrip-d">
                    <label for="ta-d-i-${L}" class="descrip-label-des" >Description: ${F+1}</label>
                    <textarea id="ta-d-i-${L}" class="com-ta-d-i" name="${L}" ></textarea> 
                </div>
                <div id="f-descrip-d-${L}" class="f-descrip-d display_flex" data-numb="${L}">
                ${GetIMGParam().F <= (Number(ValuesCR.dataset.limit)-1) ? S : ""}
                </div>
                <div class="del-description-sec"><button id="del-des-sec-${L}">
                    Delete description<img src="/static/user_personal_area/img/trash.png">
                </button></div>
            </div>`
    return X
}

// initialization adding new description html container
function GetAllDes(){return document.querySelectorAll('.com-ta-d-i')};
const AllDesCon = document.querySelector('.com-descrip-d');
const AddDesSection = document.querySelector('#add-descript-c')
let countD = AllDesCon.children.length
AddDesSection.addEventListener('click',()=>{
    if(AllDesCon.children.length <= 2){
    let ObjectD = {};
    GetAllDes().forEach(e=>{ObjectD[e.id] = e.value});
    countD+=1;
    AllDesCon.innerHTML+=GetHtmlDes(countD,AllDesCon.children.length)
    GetAllDes().forEach(e=>{ObjectD[e.id] ? e.value = ObjectD[e.id]: e.value = ''});
    WinNumb+=1;
    GetImgListDiv1();
    LoadDelElem();
    }
})


function DNumb(){
    const E = document.querySelectorAll('.descrip-label-des')
    let C = 1;
    E.forEach(e=>{
        e.innerHTML = e.innerHTML.replace(e.innerHTML.slice(e.innerHTML.length-1),C)
        C+=1
    })
}

// delete description html container
function DelDes(e){
    let v = document.querySelector(`#del-des-sec-${e.dataset.numb}`)
    v.addEventListener('click',()=>{
        if(AllDesCon.children.length > 1){
            document.querySelectorAll(`.img-count-data-${e.dataset.numb}`).forEach(el=>{
                DelDesImg(`part-${e.dataset.numb}:input-file-des-${el.id.slice( el.id.lastIndexOf("-")+1)}`)
            });
            e.remove();
            WinNumb-=1;
            AddForEachWin();
            GetImgListDiv1();}
        })
}

// puts each element in delete function
function LoadDelElem(){
    for (let i = 0; i < AllDesCon.children.length; i++){DelDes(AllDesCon.children[i])}
}
if(Rows){LoadDelElem()}
// return quantity of loaded images and available to load
function GetIMGParam(){
    let Ar = [];
    let f = 0;
    document.querySelectorAll('.img_view_container-des img').forEach(e=>{
        (0 != e.dataset.bool) ? f+=1 : Ar.push(e.id.substring(e.id.lastIndexOf('-')+1))
    });
    return {'AR':Ar,'F':f};
}
// delete extra empty img load window
function DelExtraImgWin(){
    const GetPar = GetIMGParam();
    if(GetPar.F>=Number(ValuesCR.dataset.limit) && GetPar.AR.length > 0){
        GetPar.AR.forEach(i=>{document.querySelector(`#img-file-des-${i}`).remove()})
    }
    return GetPar.F
}
// adding for each description img load window 
function LF(){
    return document.querySelectorAll('.f-descrip-d')
};

function AddForEachWin(){
LF().forEach(e=>{
    AddImgWindow(ImgSource,`f-descrip-d-${e.dataset.numb}`,'-des',e.dataset.numb)
})
}

//----------------------------------------------------------------------

let ImgMainFiles = new FormData();
let VideoMainFiles = new FormData();
let ImgDesFiles = new FormData();
function SetMainImgFiles(F){
    ImgMainFiles.set(F.id,F.files[0],F.value)
}
function SetDesImgFiles(F,N){
    ImgDesFiles.set(`part-${N}:${F.id}`,F.files[0],F.value)
}

function SetVideoFiles(F){
    VideoMainFiles.set(F.id,F.files[0],F.value)
}
function DelVideoFiles(F){
    VideoMainFiles.delete(F.id)
}

function DelMainImg(I){
    ImgMainFiles.delete(I)
}
function DelDesImg(I){
    ImgDesFiles.delete(I)
}

function JsonCreate(object) {
    return JSON.stringify(object)
};

function GetStringData(){
    const ObjectForm = {};
 
    if(RadioInputValue.value_element){
        ObjectForm['product_id'] = RadioInputValue.value_element.id
        ObjectForm['name'] = RadioInputValue.value_element.dataset.slug
        ObjectForm['category'] = RadioInputValue.value_element.dataset.category
        ObjectForm['preview'] = OldSl

    }else{
        ContainerCategory.classList.remove('display_none');
        CategoryButton.focus();
        return false
    }
    const ProductName = document.querySelector('#name-product')
    if(Boolean(ProductName.value.trim())){
        ObjectForm['title'] = ProductName.value.trim()
    }else{
      ProductName.focus();
      return false
    }
    const Price = document.querySelector('#price_field')
    if(Boolean(Number(Price.value))){
        ObjectForm['price'] = Price.value
    }else{
        Price.focus();
        return false
    }

    const Quantity = document.querySelector('#quantity_field')
    if(Number(Quantity.value)>= 1){
        ObjectForm['quantity'] = Quantity.value
    }else{
        Quantity.focus();
        return false
    }
    return ObjectForm
}


function GetStringDes(){
    const DesForm = {};
    const DesTitle = document.querySelector('#t-d-i')
    if(Boolean(DesTitle.value.trim())){
        DesForm['des-title'] = DesTitle.value.trim()
    }else{
        DesTitle.focus();
        return false
    }
    
    function Control(){
        let TF = true;
        let Ct = 1;
        GetAllDes().forEach(e=>{
            if(Boolean(e.value.trim())){
                DesForm[`description-${Ct}_${e.name}`] = e.value.trim();
                Ct+=1;
            }else{
                e.focus();
                TF = false;
            }})
        return TF};

    let Des = Control();
    if(!Des){return Des};
    const Table = document.querySelector('.table-style-c tbody')
    if(Boolean(Table.children[0].children.length)){
        DesForm['table'] = Table.innerHTML.trim();
    }
    return DesForm
}

function GetMediaMString(){
    let D = {};
    document.querySelectorAll('.img-con-div .input-f-c').forEach(e=>{
        if(selectedIMg.id.slice( selectedIMg.id.lastIndexOf("-")+1) === e.id.slice(e.id.lastIndexOf("-")+1) && e.name && e.dataset.value){
            D[e.id]= {'id':e.name,'path':e.dataset.value,'selected':true}
        }
        else if(e.name && e.dataset.value){
            D[e.id]= {'id':e.name,'path':e.dataset.value}
        }else{return D['delete']= true}
    })
    return D
};

function GetMediaVString(){
    let D ={}
    if(InputFileV.name && InputFileV.dataset.value){
        D[InputFileV.id]={'id':InputFileV.name,'path':InputFileV.dataset.value}
    }
    return D
};

function GetMediaDString(){
    let D = {};
    document.querySelectorAll('.img-con-div-des .input-f-c').forEach(e=>{
        if(e.name && e.dataset.value && e.dataset.numb){
            D[`part-${e.dataset.numb}:${e.id}`]= {'id':e.name,'path':e.dataset.value}
        }
    })
    return D
};
// get additional field  model for search
function GetModelValues(){
    let D = {};
    document.querySelectorAll('#field_inform_cat li').forEach(e=>{
        if(e.children[1].type == 'checkbox' && !e.children[1].checked){
        }else if(Boolean(e.children[1].value.trim())){
            D[e.children[1].name] = e.children[1].value.trim()
    }
    })
    let TR = false
    Object.values(D).forEach(e=>{
        if(Boolean(e)){TR = true}
    })
    if(!TR){return {}}
    return D
}

function GetAllData(){
    // making json format
    let S = GetStringData();
    let M = GetStringDes(); 
    if(!S || !M){return false};
    let D = new FormData();
    D.set('name-data',JsonCreate(S));
    D.set('description-data',JsonCreate(M));
    // control errors end set images and video in D formdata
    D.set('model_fields',JsonCreate(GetModelValues()))
    function K(){
        for (const KeyValue of ImgMainFiles.entries()){
            (KeyValue [0].slice( KeyValue [0].lastIndexOf("-")+1) == selectedIMg.id.slice( selectedIMg.id.lastIndexOf("-")+1)) ?
            D.set('selected-img',KeyValue [1]) : D.set(KeyValue [0],KeyValue [1]);
        }
    };
    function V(){
        for (const KeyValue of VideoMainFiles.entries()) {D.set(KeyValue [0],KeyValue [1]);}
    };
    function U(){
        for (const KeyValue of ImgDesFiles.entries()) {D.set(KeyValue [0],KeyValue [1]);}
    };

    if(ExCount1 && Number(ExCount.dataset.count)){
        S = GetMediaMString();
        if(Object.keys(S).length !== 0 && !(ImgMainFiles.entries().next().done)){
            D.set('edit-data-main-img',JsonCreate(S));
            K()
        }else if((Object.keys(S).length === 1 && !S['delete']) || (Object.keys(S).length > 1)){
                D.set('edit-data-main-img',JsonCreate(S));
        }else if(!(ImgMainFiles.entries().next().done)){K()}else{
            document.querySelector('#img_button_error').focus();
            return false;
        }
        S = GetMediaVString()
        if(Object.keys(S).length !== 0){
            D.set('edit-data-video',JsonCreate(S));
        }
        S = GetMediaDString()
        if(Object.keys(S).length !== 0){
            D.set('edit-data-des-img',JsonCreate(S));  
        }

    }else{
    if(!(ImgMainFiles.entries().next().done)){
        K()
    }else{
        document.querySelector('#img_button_error').focus()
        return false;
    }};
    
    if(!(VideoMainFiles.entries().next().done)){V()};
    if(!(ImgDesFiles.entries().next().done)){U()};
    
    D.set('csrfmiddlewaretoken', document.querySelector('#send_form_files input').value);
    return D
};



const FGB = document.querySelector('.send-form-bt-p button')
FGB.addEventListener('click', async (e)=>{
    const LoadImg = document.querySelector('#load-anim-icon')
    e.preventDefault()
    let AllData = GetAllData();
    if(AllData){
        AllData.set('name_id',FGB.dataset.id)
        LoadImg.classList.remove('display_none')
        LoadImg.classList.add('display_flex')
        let response = await fetch(window.location.href, {
            method: "POST",
            enctype:"multipart/form-data",
            body: AllData,
          });
        response = await response.json();
        console.log(response)
        if(response['url']){
            LoadImg.classList.remove('display_flex')
            LoadImg.classList.add('display_none')
            window.location.href = response['url']
        }else{
            LoadImg.classList.remove('display_flex')
            LoadImg.classList.add('display_none')
            document.querySelector('.error-div-style').innerHTML = response['error']
        }
    }else{
        LoadImg.classList.add('display_none')
        document.querySelector('.error-div-style').innerHTML =`<strong class="str-1">ERROR: There is not enough data to processes. 
        Please compile at least all necessary fields marked with</strong><strong class="str-2"> *. </strong>`
    }
})


function LoadFields(fields){
    let G = document.querySelector('#field_inform_cat ul')
    if(fields != 'None'){
    G.innerHTML = fields 
    Object.values(G.children).forEach(e=>{
      if(e.children[0].textContent.includes('uam')){
      e.children[0].textContent = e.children[0].textContent.slice(0,e.children[0].textContent.indexOf('uam')-1) +':'
      e.children[1].placeholder ='expressed in ' + e.children[1].name.slice(e.children[1].name.lastIndexOf('uam')+4)
      if(e.children[1].children.length){
        Object.values(e.children[1].children).forEach(o=>{
            if(o.textContent.includes(' uam ')){
                o.textContent = o.textContent.slice(0, o.textContent.indexOf(' uam ')) + ' expressed in '
                 + o.textContent.slice(o.textContent.indexOf(' uam ')+5)
            }
        })
      }
       }
    })
}else{
    G.innerHTML = ''
}
};


async function GetCategoryFields(event){
    console.log(event)
        let D = new FormData();
        D.set('csrfmiddlewaretoken', document.querySelector('#send_form_files input').value);
        D.set('get_category_fields',JsonCreate({'slug': event.dataset.slug,'id': event.dataset.id,'category':event.dataset.category}));
        let response = await fetch(window.location.href, {
            method: "POST",
            enctype:"multipart/form-data",
            body: D
          });
        response = await response.json();
        if(response['fields']){
        LoadFields(response['fields'])
        }
};