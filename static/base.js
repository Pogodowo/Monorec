const listaSkladnikowDrop=document.getElementById("lista-dropdown" )
var ingridients=['3% roztwór kwasu borowego', 'Anestezyna', 'Balsam Peruwiański', 'Bizmutu azotan zasadowy',
'Bizmutu węglan zasadowy', 'Detreomycyna', 'Efedryna', 'Erytromycyna', 'Etanol', 'Euceryna', 'Gliceryna 86%', 'Hascobaza', 'Hydrokortyzon',
'Ichtiol', 'Kwas Borowy','Kwas Salicylowy', 'Laktoza', 'Lanolina',  'Lidokaina','Maść Cholesterolowa', 'Mentol', 'Metronidazol', 'Mocznik', 'Neomycyna', 'Nystatyna',
'Olej Rycynowy', 'Oleum Cacao', 'Oleum Menthae piperitae',
 'Papaweryna', 'Prokaina', 'Rezorcyna', 'Tlenek Cynku', 'Wazelina biała', 'Wazelina żółta', 'Witamina A', 'Witamina E', 'Woda destylowana','Woda Utleniona 3%']
const CloseXButton= document.getElementById('close-x')
const CloseXButton2= document.getElementById('close-x2')
function myFunction(){}

function listaSkladnikowDropFunc(){
          const ul=document.createElement('ul')
          ul.setAttribute('class','column-dropdown')
          ingridients.map(item=>{
          const p=document.createElement('p')
          p.setAttribute('class','drop-ingridient-item')
          const a=document.createElement('a')
          a.setAttribute('class',"dropdown-item");
          a.setAttribute('onclick',`if(getElementById('myInput')!=null){getElementById('myInput').value = '${item}'}else{myFunction()}`);
          a.innerText=item
          p.appendChild(a)
          ul.appendChild(p)
          })
          listaSkladnikowDrop.appendChild(ul)
          }




 listaSkladnikowDropFunc()

 /////////////funkcje dodaj rec///////////////////////////////

 console.log('nowa receptura js')

const formBoxRecBase= document.getElementById('dodajRecModalBody')
const csrfBase = document.getElementsByName('csrfmiddlewaretoken')
const DodajRecNavFormShow=document.getElementById('dodajRecNavButton')
const KontaktModalShow=document.getElementById('KontaktButton')
const submitBox=document.getElementById('dodajRecSubmit')
//const zaDuzoRecepturModal=document.getElementById("zaDuzoRecepturModal")
function removeElementsByClass(className){
    const elements = document.getElementsByClassName(className);
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
}




function BaseFormGen(data,slownik,deleteInputs){

         data.map(item=>{
            if(Array.isArray(item)){{
                {
                const div=document.createElement('div')
                div.setAttribute('class','input-field ')
                if(deleteInputs==true){div.setAttribute('class','elFormDelete input-field');}
                const label=document.createElement('label');
                label.textContent=slownik[item[0]]
                const br=document.createElement('br')
                br.setAttribute('class','elFormDelete')
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown select-field");
                select.setAttribute('id',`${item[0]}`)

                div.appendChild(label)
                div.appendChild(select)
                formBoxRecBase.appendChild(div)
                const optionBox= document.getElementById(`${item[0]}`)
                const slicedArray=item.slice(1)

                slicedArray.map(elem=>{
                const option=document.createElement('option')
                option.value = elem
                if(slownik.hasOwnProperty(elem)){option.textContent = slownik[elem]}else{option.textContent = elem}
                optionBox.appendChild(option)
                })}
                }
            }else{            {
            const div=document.createElement('div')
            div.setAttribute('class','input-field ')
            if(deleteInputs==true){div.setAttribute('class','elFormDelete input-field');}
            const label=document.createElement('label')
            label.textContent=slownik[item]
            const input=document.createElement('input')
            input.setAttribute('id',`${item}`)
            input.setAttribute('type','number')
            input.setAttribute("min","0")
            input.setAttribute('max',"99999")
            console.log('idwimpucie',`${item}`)
            const br=document.createElement('br')
            br.setAttribute('class','elFormDelete')
            div.appendChild(label)
            div.appendChild(input)
            formBoxRecBase.appendChild(div)
            formBoxRecBase.appendChild(br)
            }}
            })


}



function generowanieFormularzaRecepty (){


           ////////////////ajax pobieranie elementów formularza///////////////////////////////

            $.ajax({
            type: 'GET',
            url: 'dodajRecForm/',
            success : function(response){
            var elementyForm = response.fields.common
            var slownik=response.fields.slownik
            BaseFormGen(elementyForm,slownik,false)
//////////////////////////generoeanir fomularza do czopków/////////////////////////////////
           var rodzajBox = document.getElementById('rodzaj')
           rodzajBox.addEventListener('change',function ()  {removeElementsByClass('elFormDelete');
           var rodzaj=rodzajBox.value
           var szczegForm=response.fields[rodzaj]
           BaseFormGen(szczegForm,slownik,true)

           $("#dodajRecModal").modal('show');

            })
///////////////////////////////////////////////////////////////////////////////////////////////
            },
            error : function (response){
            console.log('error')}
            })
            }



function dodawanieRec(){
                console.log('wywołanie dodawanieRec()')
                ///tworzenie daty formulara i odpowiedzi do ajaxa////////////////////
                dataf={'csrfmiddlewaretoken': csrfBase[0].value,}

                var elements = document.getElementById("dodajRecModalBody").elements;
                console.log('elements',elements)
                for (var i = 0, element; element = elements[i++];) {
                if (element){
                console.log("mamy element");
                dataf[element.id]=element.value;
                 }}

                console.log('dataf',dataf)

                $.ajax({
                type: 'POST' ,
                url:'dodawanieRecJson/',
                data : dataf,
                success: function(response){
                         console.log('wygrywamy');
                         console.log('response.dodawanie recepty tabela',response.dict)
                         if (response.dict.id!= null && response.dict.res!= "przekroczona liczba")
                         {id=response.dict.id
                         //location.href = 'mojerec'
                         location.replace ( `/receptura/(${id})`)
                         }
                         else{
                         console.log('za dużo receptur')
                         $("#zaDuzoRecepturModal").modal('show');
                         }

                                        },
                error : function(error){
                         console.log(' error nie działa');
                                                    }
                 });
                 /////koniec ajaxa
                 removeElementsByClass('elFormDelete');



                 }


                    /////tu koniec wstawania//////

generowanieFormularzaRecepty()
DodajRecNavFormShow.addEventListener('click', e=>{ $("#dodajRecModal").modal('show');})
KontaktModalShow.addEventListener('click', e=>{ $("#kontaktModal").modal('show');})
submitBox.addEventListener('click', dodawanieRec)
CloseXButton.addEventListener('click', e=>{ $("#dodajRecModal").modal('hide');})
CloseXButton2.addEventListener('click', e=>{ $("#kontaktModal").modal('hide');})
