console.log('nowa receptura js')

const formBoxRec= document.getElementById('form-rec')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const submitBox=document.getElementById('dodajRecSubmit')
const zaDuzoRecepturModal=document.getElementById("zaDuzoRecepturModal")
function removeElementsByClass(className){
    const elements = document.getElementsByClassName(className);
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
}




function BaseFormGen(data,slownik){

         data.map(item=>{
            if(Array.isArray(item)){{
                {
                const div=document.createElement('div')
                div.setAttribute('class','input-field')
                const label=document.createElement('label');
                label.textContent=slownik[item[0]]
                const br=document.createElement('br')
                br.setAttribute('class','elFormDelete')
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown select-field");
                select.setAttribute('id',`${item[0]}`)

                div.appendChild(label)
                div.appendChild(select)
                formBoxRec.appendChild(div)
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
            div.setAttribute('class','input-field')
            const label=document.createElement('label')
            label.textContent=slownik[item]
            const input=document.createElement('input')
            input.setAttribute('id',`${item}`)
            console.log('idwimpucie',`${item}`)
            const br=document.createElement('br')
            br.setAttribute('class','elFormDelete')
            div.appendChild(label)
            div.appendChild(input)
            formBoxRec.appendChild(div)
            formBoxRec.appendChild(br)
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
            BaseFormGen(elementyForm,slownik)
//////////////////////////generoeanir fomularza do czopków/////////////////////////////////
           var rodzajBox = document.getElementById('rodzaj')
           rodzajBox.addEventListener('change',function ()  {removeElementsByClass('elFormDelete');
           var rodzaj=rodzajBox.value
           var szczegForm=response.fields[rodzaj]
           BaseFormGen(szczegForm,slownik)
            })
///////////////////////////////////////////////////////////////////////////////////////////////
            },
            error : function (response){
            console.log('error', error)}
            })
            }



function dodawanieRec(){
                console.log('wywołanie dodawanieRec()')
                ///tworzenie daty formulara i odpowiedzi do ajaxa////////////////////
                dataf={'csrfmiddlewaretoken': csrf[0].value,}

                var elements = document.getElementById("form-rec").elements;
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
                         location.href = `/receptura/(${id})`
                         }
                         else{
                         console.log('za dużo receptur')
                         $("#zaDuzoRecepturModal").modal('show');
                         }

                                        },
                error : function(error){
                         console.log(' dupa nie działa');
                                                    }
                 });
                 /////koniec ajaxa
                 removeElementsByClass('elFormDelete');



                 }


                    /////tu koniec wstawania//////

generowanieFormularzaRecepty()
submitBox.addEventListener('click', dodawanieRec)