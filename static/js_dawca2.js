console.log('O co tu chodzi?')
console.log('dupa?')
const modalBox=document.getElementById("exampleModal")
//const skladnikBox= document.getElementById('wybieraj');
const modalTytul=document.getElementById("exampleModalLabel")
const formBox= document.getElementById('modal-form')

const closeButton=document.getElementById('close-button')
const dodajSkladnikButton=document.getElementById("dodajsklbutton")
const prowizorycznatabelaBox=document.getElementById('prowizorycznatabela')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const tabelaDocelowa=document.getElementById('tabela-docelowa')
//console.log('tabelaDocelowa',tabelaDocelowa)
const deleteButtons=document.getElementsByClassName("btn-close")
const inputBox=document.getElementById("myInput")
const autocompleteButton=document.getElementById("submitButton")
cardBox=document.getElementById('cards')
console.log('close buttons', deleteButtons)
const mojeRecBox=document.getElementById("tabela-moje-rec")
const idBox=document.getElementById("pk-box")
console.log('id-box',idBox)
const sklId=idBox.innerText
console.log('sklId',sklId)
const elementyForm={}
const edytujSkladnikButton=document.getElementById("edytujjsklbutton")
edytujSkladnikButton.style.visibility = "hidden"
const zapiszZmianyButton=document.getElementById("zapiszzmianybutton")
zapiszZmianyButton.style.visibility = "hidden"
parametryRecBox=document.getElementById('parametry')
const delCardButton=document.getElementById('button-del')
const edCardButton=document.getElementById('button-ed')
console.log('csrf',csrf)

updateTable()

var ingridients=["witamina A","witamina E","Hydrokortyzon","Metronidazol","Wazelina","Mocznik","Woda destylowana","Etanol"
,"Oleum Cacao",'Oleum Menthae piperitae','Nystatyna','3% roztwór kwas borowy','Detreomycyna','Rezorcyna','Euceryna','Lanolina','Gliceryna 86%']
/////////////////js do autouzupełniania////////////////////////////////////////////////////////////
function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
}


autocomplete(inputBox, ingridients);
////koniec js do autouzupełmiania/////////////////////////////////////////////////////////////////

//////// ten kod pozwala na zaznaczene tylko jednegi chexboxa///////////////////////////////////////


function onlyOne(checkbox) {
    var checkboxes = document.getElementsByName('check')
    checkboxes.forEach((item) => {
        if (item !== checkbox) item.checked = false
    })
}
///////////////////////////////



/////funkcja do usuwania składnika///////////////////////////

function usuwanieSkladnika (pk){
        $.ajax({
                        type: 'GET',
                        url: `delSkl/${ pk }/`,
                        success : function(response){console.log('sukces ajaxa z del');
                        cardBox.innerHTML=''
                        tabelaDocelowa.innerHTML='';
                        updateTable()

                        },//koniec sukcesa
                        error : function (error){console.log('brak sukcesu ajaxa z del')},
                        })

}




function generowanieFormularza (){
          skl=inputBox.value;
          console.log('skladnikform',skl);
          modalTytul.innerText=inputBox.value;
           $("#exampleModal").modal('show');
           ////////////////ajax pobieranie elementów formularza///////////////////////////////

            $.ajax({
            type: 'GET',
            url: `formJson/${skl}&${sklId}/`,
            success : function(response){
            console.log('succes spobrania do forma', response);
            var elementyForm = response.formData.datadict
            var dict=response.formData.table_dict
           console.log('elementyForm z gen form',elementyForm)
           if (elementyForm!="ten składnik już został dodany"){
            elementyForm.map(item=>{
            if(Array.isArray(item)){if (item[0]==='producent' ||item[0]==='gestosc'){
                console.log('mamy tabelę');
                const label=document.createElement('label')
                label.textContent=item[0]
                label.setAttribute('class','elFormDelete');
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown");
                //select.setAttribute('id',"optionId");
                select.setAttribute('class','elFormDelete')
                select.setAttribute('id',`${skl}-${item[0]}`)
                console.log('idwimpucie',`${skl}-${item[0]}`)
                formBox.appendChild(label)
                formBox.appendChild(select)
                //const optionBox= document.getElementById('optionId')
                const optionBox= document.getElementById(`${skl}-${item[0]}`)
                const slicedArray=item.slice(1)
                console.log(item[0])
                slicedArray.map(elem=>{
                const option=document.createElement('option')
                option.textContent = elem
                optionBox.appendChild(option)
                })}else{ console.log('tutaj będzie select z imputem');
                {
                console.log('mamy tabelę');
                const label=document.createElement('label');
                label.textContent=dict[item[0]]
                label.setAttribute('class','elFormDelete');
                const br=document.createElement('br')
                br.setAttribute('class','elFormDelete')
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown");
                //select.setAttribute('id',"optionId");
                select.setAttribute('class','elFormDelete')
                select.setAttribute('id',`${skl}-${item[0]}`)
                console.log('idwimpucie',`${skl}-${item[0]}`)
                formBox.appendChild(label)
                formBox.appendChild(select)
                formBox.appendChild(br)
                //const optionBox= document.getElementById('optionId')
                const optionBox= document.getElementById(`${skl}-${item[0]}`)
                const slicedArray=item.slice(1)
                console.log(item[0])
                slicedArray.map(elem=>{
                const option=document.createElement('option')
                option.textContent = elem
                optionBox.appendChild(option)
                })}
                }
            }else{

            if (['aa','aa_ad','dodaj_wode','ad','qs','czy_zlozyc_roztwor_ze_skladnikow_prostych'].includes(item)){
            const label=document.createElement('label')
            label.textContent=item
            const check = document.createElement("input");
            check.setAttribute('type',"checkbox")
            check.setAttribute('value','off')
            check.setAttribute('id',`${skl}-${item}`)
            console.log('idwimpucie',`${skl}-${item}`)
            if (['aa','aa_ad','ad','qs'].includes(item)){check.setAttribute('name','check');
            check.setAttribute('onclick',"onlyOne(this)")}
            check.setAttribute('class','elFormDelete check-box')
            label.setAttribute('class','elFormDelete check-box-label')

            formBox.appendChild(label)
            formBox.appendChild(check)

            console.log('checkvalue',check.value)
            } else
            {
            const div=document.createElement('div')
            div.setAttribute('class','input-field')
            const label=document.createElement('label')
            const input=document.createElement('input')
            input.setAttribute('class','elFormDelete')
            label.setAttribute('class','elFormDelete')
            input.setAttribute('id',`${skl}-${item}`)
            console.log('idwimpucie',`${skl}-${item}`)
            const br=document.createElement('br')
            br.setAttribute('class','elFormDelete')
            label.textContent=dict[item]
            div.appendChild(label)
            div.appendChild(input)
            formBox.appendChild(div)

            //formBox.appendChild(br)
            }}
            })
            dodajSkladnikButton.style.visibility = "visible"
            edytujSkladnikButton.style.visibility = "hidden"
            zapiszZmianyButton.style.visibility = "hidden"


            }else{const label=document.createElement('label')
            label.textContent='Ten składnik został już dodany. Czy chcesz go edytować? '
            label.setAttribute('class','elFormDelete')
            formBox.appendChild(label)
            dodajSkladnikButton.style.visibility = "hidden"
            edytujSkladnikButton.style.visibility = "visible"

            }

            },
            error : function (response){
            console.log('error', error)}
            })
            }





function dodawanieSkl(){
            skl=inputBox.value;
            $.ajax({
            type: 'GET',
            url: `formJson/${skl}&${sklId}/`,
            success : function(response){
            console.log('succes spobrania do forma', response);
            var elementyForm = response.formData.datadict
            console.log('wczesne elementy form',elementyForm)

                const checkButtons = document.getElementsByClassName('check-box')
                console.log('checkButtons',checkButtons)
                for (let check of checkButtons){if (check.checked){ check.value='on'}else{check.value='off'}}
                /////////////////////////////////////////////////////////////////////////////
                ///tworzenie daty formulara i odpowiedzi do ajaxa////////////////////
                dataf={'csrfmiddlewaretoken': csrf[0].value,'skladnik':skl,'receptura_id':sklId}
                console.log('elementyForm1',elementyForm)
                for ( var i in elementyForm )if ( Array.isArray(elementyForm[i])){ console.log('na razie nie umiem tabeli',
                `${skl}-${elementyForm[i][0]}`);
                dataf[elementyForm[i][0]]=document.getElementById(`${skl}-${elementyForm[i][0]}`).value}
                else
                {console.log('i',i,`${skl}-${elementyForm[i]}`);
                dataf[elementyForm[i]]=document.getElementById(`${skl}-${elementyForm[i]}`).value}
                console.log('elementyForm2',elementyForm)
                console.log('dataf',dataf)

                $.ajax({
                type: 'POST' ,
                url:`dodajskl/${sklId}/`,
                data : dataf,
                success: function(response){
                         console.log('wygrywamy');
                         console.log('response.tabela',response.tabela)
                         tabelaDocelowa.innerHTML=''
                         updateTable()
                                        },
                error : function(error){
                         console.log(' dupa nie działa');
                                                    }
                 });
                 /////koniec ajaxa
                 removeElementsByClass('elFormDelete');
                 $("#exampleModal").modal('hide');
                 updateTable();


                 },
            error : function (response){
            console.log('error', error)}
            })
            }

                    /////tu koniec wstawania//////





////////////////////////////////////////////////////////////
////////funkcja z ajaxem do aktualizacji taveli///////
function updateTable(){
         tabelaDocelowa.innerHTML='';

         $.ajax({
            type: 'GET',
            url:`aktualizujTabela/${sklId}/`,
            success : function(response){
            parametryRecBox.innerHTML='';
            console.log('Sukces ajaxa z tabelą', response);
            let elementyTabeli=response.tabela_zbiorcza
            console.log('elementyTabeli', response.tabela_zbiorcza)
            param=elementyTabeli.parametry.fields
            slownik=elementyTabeli.slownik
            elementyTabeli=elementyTabeli.objects
            console.log('param',param)
            console.log('slownik',slownik)

            ////////////////test/////////////////////////////
            card=document.createElement('div')
            card.setAttribute('class','paramcard-css')
          //card.setAttribute('style','width: 36rem;')

            var ul=document.createElement('ul')
            ul.setAttribute('class','list-group list-group-flush')
            var li=document.createElement('li')
            li.setAttribute('class','flex-containerparam')
            li.innerHTML=""
            ul.appendChild(li)
            var li2=document.createElement('li')
            //li2.classList.add( 'li-inline');
             li2.setAttribute('class','flex-containerparam')
         //li2.setAttribute('class','li-inline')

        /////////wypisywanie atrybutów danego składnika/////


        for (const [key, value] of Object.entries(param)){ if ( value!=null && value!='0' && value!=''){
               const div=document.createElement('div')
                  div.setAttribute('class','flex-item-param')
                  if (key in slownik & key=='date'){console.log('jest w słowniku')
                  div.innerHTML+=' '+slownik[key]+': '
                  div.innerHTML+=value.slice(0,16).replace('T',' godz:')}
                  else if (key=='rodzaj'  & value=='czopki_i_globulki'){console.log('jest w słowniku')
                  }
                  else if (key in slownik ){console.log('jest w słowniku')
                  div.innerHTML+=' '+slownik[key]+': '
                  div.innerHTML+=value}
                  else{
                  div.innerHTML+=' '+key+': '
                  div.innerHTML+=value}
             if(div.innerHTML!='' & key!='owner'){
             if (key==='nazwa' || key==='date' ){li.appendChild(div)}else{
             li2.appendChild(div)}}
                                                    }}
        ///////////////////////////////////////////////////

        ul.appendChild(li2)
        card.appendChild(ul)
        parametryRecBox.appendChild(card)

            ////////////////koniec testu//////////////////////////////
            //let tabelaDocelowa=document.getElementById("tabela-docelowa");
            tabelaDocelowa.innerHTML=''
            cardBox.innerHTML=''
            div=document.createElement('div')
            div.innerHTML='Rp. <br><br>'
            tabelaDocelowa.appendChild(div)
            var numElem=1
            if (elementyTabeli!=null){
            elementyTabeli.map(item=>{
            console.log('itemTabeli',item.fields.skladnik);
            const div=document.createElement('div')
            ///////dodawanie przycisku do usuwania////////////////
            var deleteButton = document.createElement("button");

//          element.type = type;type="button" class="close" data-dismiss="modal" aria-label="Close"
            deleteButton.setAttribute('type','button');
            deleteButton.setAttribute('class',"btn-close");
            deleteButton.setAttribute('aria-label','Close');
            deleteButton.setAttribute('id',item.pk);
            //deleteButton.setAttribute('onclick',delItem);
            deleteButton.onclick = function() {usuwanieSkladnika(item.pk);
            }
            //////////////////////////////////////////////////////
            if (item.fields.show===true){
            div.innerHTML+= numElem+') ' + item.fields.skladnik+'  '
            if (item.fields.skladnik==='Etanol'){div.innerHTML+=item.fields.pozadane_stezenie+'° '}
            if (item.fields.aa==='on'){div.innerHTML+='aa '}
            else if(item.fields.aa_ad==='on'){div.innerHTML+='aa ad '}
            else if(item.fields.ad==='on'){div.innerHTML+='ad '}
            else if(item.fields.qs==='on'){div.innerHTML+='qs '}
            if (item.fields.ilosc_na_recepcie!=='') {div.innerHTML+=+item.fields.ilosc_na_recepcie}
            console.log('div',div);
            div.appendChild(deleteButton);
            tabelaDocelowa.appendChild(div);
            }



            //div.innerHTML+='<br>'
            ///////////////dodawanie kart/////////////////


      card=document.createElement('div')

          card.setAttribute('class','card card-css')
          //card.setAttribute('style','width: 36rem;')

   var ul=document.createElement('ul')
        ul.setAttribute('class','list-group list-group-flush')
   var li=document.createElement('li')
        li.setAttribute('class','list-group-item')
   var span=document.createElement('span')
        if (item.fields.skladnik=='3% roztwór kwas borowy' && item.fields.czy_zlozyc_roztwor_ze_skladnikow_prostych=='on')
        {span.innerHTML=numElem+')   kwas borowy'}else{
        span.innerHTML=numElem+')   '+item.fields.skladnik}

   var buttonDel=document.createElement('button')
       buttonDel.innerText='Usuń'
       buttonDel.setAttribute('class','btn btn-secondary mt-1 button-card')
       buttonDel.setAttribute('id','button-del')
   var buttonEd=document.createElement('button')
       buttonEd.innerText='Edytuj'
       buttonEd.setAttribute('class','btn btn-primary mt-1 button-card')
       buttonEd.setAttribute('id','button-ed')
       li.append(span)
       li.appendChild(buttonDel)
       li.appendChild(buttonEd)
       ul.appendChild(li)

   buttonDel.onclick = function() {usuwanieSkladnika(item.pk);
            }
   buttonEd.onclick = function() {generowanieFormularzaDoEdycji(item.fields.skladnik);
            }
   var li2=document.createElement('li')
       //li2.classList.add( 'li-inline');
       li2.setAttribute('class','flex-container')
       //li2.setAttribute('class','li-inline')

        /////////wypisywanie atrybutów danego składnika/////


        for (const [key, value] of Object.entries(item.fields)){ if ( value!=null && value!='0' && value!=''){
               const div=document.createElement('div')
                  div.setAttribute('class','flex-item')
                  if (key in slownik){console.log('jest w słowniku')
                  div.innerHTML+=' '+slownik[key]+': '
                  div.innerHTML+=value}else{
                  div.innerHTML+=' '+key+': '
                  div.innerHTML+=value}
             li2.appendChild(div)
                                                    }}
        ///////////////////////////////////////////////////

        ul.appendChild(li2)
        card.appendChild(ul)
        cardBox.appendChild(card)
        numElem+=1



            //////////////////////////////////////////////


            })
            //var skladnikiRecepturyBox=document.getElementById(`${sklId}-skladniki`)


            }
            if (param['rodzaj']==='czopki_i_globulki' & param["czopki_czy_globulki"]==='czopki'){
            div=document.createElement('div');
            div.innerHTML='<br>M.f. supp. anal. D.t.d. No '+param['ilosc_czop_glob'];
            tabelaDocelowa.appendChild(div)
            }else if (param['rodzaj']==='czopki_i_globulki' & param["czopki_czy_globulki"]==='globulki'){
            div=document.createElement('div');
            div.innerHTML='<br>M.f. glob. vag. D.t.d. No '+param['ilosc_czop_glob'];
            tabelaDocelowa.appendChild(div)
            }else if (param['rodzaj']==='masc'){
            div=document.createElement('div');
            div.innerHTML='<br>M.f. Ung. ';
            tabelaDocelowa.appendChild(div)
            }


            },
            error : function (error){console.log('error')},
            })
}
//////////koniec funkcji z ajaxem do aktualizacji tabeli//////
////funkcja do usuwania formularza z modala
function removeElementsByClass(className){
    const elements = document.getElementsByClassName(className);
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
}
////////////////////////////////////////////////////////////////////
const dodanyId=0

updateTable()


/////////////////edycja danych składnika//////////////////////////
////////////////tworzenie formularza z danymi do edycji///////////////
function generowanieFormularzaDoEdycji (item){
         console.log('item',item)
          //skl = item || inputBox.value;
//          if(item){skl=item}else{
//          skl=inputBox.value}
          skl=item || inputBox.value

          removeElementsByClass('elFormDelete')
          const div=document.createElement('div')
          div.setAttribute('class','elFormDelete');
          div.textContent='Edycja składnika'
          formBox.appendChild(div)
          const br=document.createElement('br')
          br.setAttribute('class','elFormDelete')
          formBox.appendChild(br)
          dodajSkladnikButton.style.visibility = "hidden"
          edytujSkladnikButton.style.visibility = "hidden"
          zapiszZmianyButton.style.visibility = "visible"


          console.log('skladnikform',skl);
          modalTytul.innerText=item || inputBox.value;
           $("#exampleModal").modal('show');
           ////////////////ajax pobieranie elementów formularza///////////////////////////////

            $.ajax({
            type: 'GET',
            url: `editFormJson/${skl}&${sklId}/`,
            success : function(response){
            console.log('succes spobrania do forma', response);
            var elementyForm = response.datadict.form
           console.log('elementyForm z gen form',elementyForm)

            elementyForm.map(item=>{
            if(Array.isArray(item)){if (item[0]==='producent'){
                console.log('mamy tabelę');
                const label=document.createElement('label')
                label.textContent=item[0]
                label.setAttribute('class','elFormDelete');
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown");
                //select.setAttribute('id',"optionId");
                select.setAttribute('class','elFormDelete')
                select.setAttribute('id',`${skl}-${item[0]}`)
                console.log('idwimpucie',`${skl}-${item[0]}`)
                formBox.appendChild(label)
                formBox.appendChild(select)
                //const optionBox= document.getElementById('optionId')
                const optionBox= document.getElementById(`${skl}-${item[0]}`)
                const slicedArray=item.slice(1)
                console.log(item[0])
                slicedArray.map(elem=>{
                const option=document.createElement('option')
                option.textContent = elem
                optionBox.appendChild(option)
                })}else{ console.log('tutaj będzie select z imputem');
                {
                console.log('mamy tabelę');
                const label=document.createElement('label');
                label.textContent=item[0]
                label.setAttribute('class','elFormDelete');
                const br=document.createElement('br')
                br.setAttribute('class','elFormDelete')
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown");
                //select.setAttribute('id',"optionId");
                select.setAttribute('class','elFormDelete')
                select.setAttribute('id',`${skl}-${item[0]}`)
                console.log('idwimpucie',`${skl}-${item[0]}`)
                formBox.appendChild(label)
                formBox.appendChild(select)
                formBox.appendChild(br)
                //const optionBox= document.getElementById('optionId')
                const optionBox= document.getElementById(`${skl}-${item[0]}`)
                const slicedArray=item.slice(1)
                console.log(item[0])
                slicedArray.map(elem=>{
                const option=document.createElement('option')
                option.textContent = elem
                optionBox.appendChild(option)
                })}
                }
            }else{

            if (['aa','aa_ad','dodaj_wode','ad','qs','czy_zlozyc_roztwor_ze_skladnikow_prostych'].includes(item)){
            const label=document.createElement('label')
            label.textContent=item
            const check = document.createElement("input");
            check.setAttribute('type',"checkbox")
            if (response.datadict.values[item]==='on'){check.checked = true;
            check.setAttribute('value','on')}else{
            check.setAttribute('value','off')}
            check.setAttribute('id',`${skl}-${item}`)
            console.log('idwimpucie',`${skl}-${item}`)
            if (['aa','aa_ad','ad','qs'].includes(item)){check.setAttribute('name','check');
            check.setAttribute('onclick',"onlyOne(this)")}
            check.setAttribute('class','elFormDelete check-box')

            label.setAttribute('class','elFormDelete')
            //check.setAttribute('class','checkBox')
            //check.setAttribute('name','checkBox')
            formBox.appendChild(check)
            formBox.appendChild(label)
            console.log('checkvalue',check.value)
            } else
            {
            const label=document.createElement('label')
            const input=document.createElement('input')
            input.value=response.datadict.values[item]
            input.setAttribute('class','elFormDelete')
            label.setAttribute('class','elFormDelete')
            input.setAttribute('id',`${skl}-${item}`)
            console.log('idwimpucie',`${skl}-${item}`)
            const br=document.createElement('br')
            br.setAttribute('class','elFormDelete')
            label.textContent=item
            formBox.appendChild(label)
            formBox.appendChild(input)
            formBox.appendChild(br)
            }}
            })



            },
            error : function (response){
            console.log('error', error)}
            })
            }






//////////////////////3pozycja/////////////////////////////////////////////////////

function edytowanieSkl(){
            var skladnik=document.getElementById("exampleModalLabel").innerHTML
            console.log('skladnik',skladnik)
            //skl=inputBox.value || skladnik;
            skl=skladnik
            $.ajax({
            type: 'GET',
            url: `editFormJson/${skl}&${sklId}/`,
            success : function(response){
            console.log('succes spobrania do forma', response);
            var elementyForm = response.datadict
            var dict=response.table_dict
            console.log('wczesne elementy form',elementyForm)

                const checkButtons = document.getElementsByClassName('check-box')
                console.log('checkButtons',checkButtons)
                for (let check of checkButtons){if (check.checked){ check.value='on'}else{check.value='off'}}
                /////////////////////////////////////////////////////////////////////////////
                ///tworzenie daty formulara i odpowiedzi do ajaxa////////////////////
                dataf={'csrfmiddlewaretoken': csrf[0].value,'skladnik':skl,'receptura_id':sklId}
                console.log('elementyForm.form1',elementyForm.form)
                elementyForm=elementyForm.form
                for ( var i in elementyForm )if ( Array.isArray(elementyForm[i])){ console.log('na razie nie umiem tabeli',
                `${skl}-${elementyForm[i][0]}`);
                dataf[elementyForm[i][0]]=document.getElementById(`${skl}-${elementyForm[i][0]}`).value}
                else
                {console.log('i',i,`${skl}-${elementyForm[i]}`);
                dataf[elementyForm[i]]=document.getElementById(`${skl}-${elementyForm[i]}`).value}
                console.log('elementyForm2',elementyForm)
                console.log('dataf',dataf)

                $.ajax({
                type: 'POST' ,
                url:`edytujskl/${skl}&${sklId}/`,
                data : dataf,
                success: function(response){
                         console.log('wygrywamy');
                         console.log('response.tabela',response.tabela)
                         tabelaDocelowa.innerHTML=''
                         updateTable()
                                        },
                error : function(error){
                         console.log(' dupa nie działa');
                                                    }
                 });
                 /////koniec ajaxa
                 removeElementsByClass('elFormDelete');
                 $("#exampleModal").modal('hide');


                 },
            error : function (response){
            console.log('error', error)}
            })
            }

                    /////tu koniec wstawania//////





autocompleteButton.addEventListener( 'click',generowanieFormularza );
dodajSkladnikButton.addEventListener('click',dodawanieSkl );
edytujSkladnikButton.addEventListener('click',generowanieFormularzaDoEdycji)
zapiszZmianyButton.addEventListener('click',edytowanieSkl)
closeButton.addEventListener('click',e=>{console.log('kliknąłem close ');$("#exampleModal").modal('hide');
                                           removeElementsByClass('elFormDelete'); })




////////////////////////////////////////////////////////////////////////////////////////////////












