
const modalBox=document.getElementById("exampleModal")
//const skladnikBox= document.getElementById('wybieraj');
const modalTytul=document.getElementById("exampleModalTitle")
const formBox= document.getElementById('modal-form')
const closeXMyjsButton=document.getElementById('close-x-button')
const closeButton=document.getElementById('close-button')

const oblEtButton=document.getElementById('button-obl-el')
const dodajSkladnikButton=document.getElementById("dodajsklbutton")
const prowizorycznatabelaBox=document.getElementById('prowizorycznatabela')
const csrft = document.getElementsByName('csrfmiddlewaretoken')
const tabelaDocelowa=document.getElementById('tabela-docelowa')

const deleteButtons=document.getElementsByClassName("btn-close")
const inputBox=document.getElementById("myInput")
const autocompleteButton=document.getElementById("submitButton")
cardBox=document.getElementById('cards')

const mojeRecBox=document.getElementById("tabela-moje-rec")
const idBox=document.getElementById("pk-box")

const sklId=idBox.innerText

const elementyForm={}
const edytujSkladnikButton=document.getElementById("edytujjsklbutton")
edytujSkladnikButton.style.visibility = "hidden"
const zapiszZmianyButton=document.getElementById("zapiszzmianybutton")
zapiszZmianyButton.style.visibility = "hidden"
parametryRecBox=document.getElementById('parametry')
const delCardButton=document.getElementById('button-del')
const edCardButton=document.getElementById('button-ed')
toPdfButton=document.getElementById("toPdfButton")
const wyborSkladnikowDrop=document.getElementById("wybor-skl-dropdown" )


updateTable()

var ingridients=['3% roztwór kwas borowy', 'Anestezyna', 'Balsam Peruwiański', 'Bizmutu azotan zasadowy', 'Bizmutu węglan zasadowy', 'Detreomycyna', 'Efedryna', 'Erytromycna', 'Etanol', 'Euceryna', 'Gliceryna 86%', 'Hascobaza', 'Hydrokortyzon', 'Ichtiol', 'Kwas Borowy','Kwas Salicylowy', 'Laktoza', 'Lanolina', 'Maść Cholesterolowa', 'Mentol', 'Metronidazol', 'Mocznik', 'Neomycyna', 'Nystatyna', 'Olej Rycynowy', 'Oleum Cacao', 'Oleum Menthae piperitae', 'Papaweryna', 'Prokaina', 'Rezorcyna', 'Tlenek Cynku', 'Wazelina biała', 'Wazelina żółta', 'Witamina A', 'Witamina E', 'Woda destylowana']
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
                        success : function(response){console.log('sukces');
                        cardBox.innerHTML=''
                        tabelaDocelowa.innerHTML='';
                        updateTable()

                        },//koniec sukcesa
                        error : function (error){console.log('error')},
                        })

}




function generowanieFormularza (){
          skl=inputBox.value;

          modalTytul.textContent=skl;
          if (ingridients.includes(inputBox.value)){
           $("#exampleModal").modal('show');
           ////////////////ajax pobieranie elementów formularza///////////////////////////////

            $.ajax({
            type: 'GET',
            url: `formJson/${skl}&${sklId}/`,
            success : function(response){
            var elementyForm = response.formData.datadict
            var dict=response.formData.table_dict
           if (elementyForm!="ten składnik już został dodany" & elementyForm!='receptura zakończona. Ostatni skladnik zawiera ad lub aa ad. Aby konynuować musisz usunąć bądź edytować ostatni skladnik '){
            elementyForm.map(item=>{
            if(Array.isArray(item)){
                const div=document.createElement('div')
                div.setAttribute('class', 'elFormDelete input-field-form')
                const label=document.createElement('label')
                label.textContent=dict[item[0]]
                label.setAttribute('class','elFormDelete');
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown");
                select.setAttribute('class','elFormDelete')
                select.setAttribute('id',`${skl}-${item[0]}`)
                div.appendChild(label)
                div.appendChild(select)
                formBox.appendChild(div)
                const optionBox= document.getElementById(`${skl}-${item[0]}`)
                const slicedArray=item.slice(1)
                slicedArray.map(elem=>{
                const option=document.createElement('option')
                option.value = elem
                if(dict.hasOwnProperty(elem)){option.textContent = dict[elem]}else{option.textContent = elem}
                optionBox.appendChild(option)
                })
            }else{
            if (['aa','aa_ad','dodaj_wode','ad','qs','czy_zlozyc_roztwor_ze_skladnikow_prostych','czy_powiekszyc_mase_oleum'].includes(item)){
            const label=document.createElement('label')
            label.textContent=dict[item]
            const check = document.createElement("input");
            check.setAttribute('type',"checkbox")
            check.setAttribute('value','off')
            check.setAttribute('id',`${skl}-${item}`)
            if (['aa','aa_ad','ad','qs'].includes(item)){check.setAttribute('name','check');
            check.setAttribute('onclick',"onlyOne(this)")}
            check.setAttribute('class','elFormDelete check-box')
            label.setAttribute('class','elFormDelete check-box-label')

            formBox.appendChild(label)
            formBox.appendChild(check)
            } else
            {
            const div=document.createElement('div')
            div.setAttribute('class','elFormDelete input-field-form')
            const label=document.createElement('label')
            const input=document.createElement('input')
            input.setAttribute('class','elFormDelete')
            label.setAttribute('class','elFormDelete')
            input.setAttribute('type','number')
            if (skl=='Nystatyna' && item=='UI_w_mg'){ input.value='6756';}
            input.setAttribute("min","0")
            input.setAttribute('max',"99999")
            input.setAttribute('id',`${skl}-${item}`)
            const br=document.createElement('br')
            br.setAttribute('class','elFormDelete')
            label.textContent=dict[item]
            div.appendChild(label)
            div.appendChild(input)
            formBox.appendChild(div)
            }}
            })
            dodajSkladnikButton.style.visibility = "visible"
            edytujSkladnikButton.style.visibility = "hidden"
            zapiszZmianyButton.style.visibility = "hidden"


            }else{
            if (elementyForm=="ten składnik już został dodany"){const label=document.createElement('label')
            label.textContent='Ten składnik został już dodany. '
            label.setAttribute('class','elFormDelete')
            formBox.appendChild(label)
            dodajSkladnikButton.style.visibility = "hidden"
            edytujSkladnikButton.style.visibility = "hidden"
            zapiszZmianyButton.style.visibility = "hidden"}
            else if (elementyForm=='receptura zakończona. Ostatni skladnik zawiera ad lub aa ad. Aby konynuować musisz usunąć bądź edytować ostatni skladnik ')
            {const label=document.createElement('label')
            label.textContent='receptura zakończona. Ostatni skladnik zawiera ad,qs lub aa ad. Aby konynuować musisz usunąć bądź edytować ostatni skladnik '
            label.setAttribute('class','elFormDelete')
            formBox.appendChild(label)
            dodajSkladnikButton.style.visibility = "hidden"
            edytujSkladnikButton.style.visibility = "hidden"
            zapiszZmianyButton.style.visibility = "hidden"}

            }

            },
            error : function (response){
            console.log('error')}
            })
            }else{ modalTytul.innerText="";
            const label=document.createElement('label');
            label.setAttribute('class','elFormDelete');
            label.textContent="Wpisz poprawny składnik"
            dodajSkladnikButton.style.visibility = "hidden"
            formBox.appendChild(label)

            $("#exampleModal").modal('show');}}





function dodawanieSkl(){

            skl=inputBox.value;
            $.ajax({
            type: 'GET',
            url: `formJson/${skl}&${sklId}/`,
            success : function(response){
            var elementyForm = response.formData.datadict
                const checkButtons = document.getElementsByClassName('check-box')
                for (let check of checkButtons){if (check.checked){ check.value='on'}else{check.value='off'}}
                /////////////////////////////////////////////////////////////////////////////
                ///tworzenie daty formulara i odpowiedzi do ajaxa////////////////////
                dataf={'csrfmiddlewaretoken': csrft[0].value,'skladnik':skl,'receptura_id':sklId}
                for ( var i in elementyForm )if ( Array.isArray(elementyForm[i])){
                dataf[elementyForm[i][0]]=document.getElementById(`${skl}-${elementyForm[i][0]}`).value}
                else
                {
                dataf[elementyForm[i]]=document.getElementById(`${skl}-${elementyForm[i]}`).value}
                $.ajax({
                type: 'POST' ,
                url:`dodajskl/${sklId}/`,
                data : dataf,
                success: function(response){
                         if (response.tabela['za_duzo_skladnikow']!=null && response.tabela['za_duzo_skladnikow']=='za_duzo_skladnikow')
                         {
                         $("#zaDuzoSkladnikowModal").modal('show');
                         }
                         tabelaDocelowa.innerHTML=''
                         updateTable()
                                        },
                error : function(error){
                         console.log('error');
                                                    }
                 });
                 /////koniec ajaxa
                 removeElementsByClass('elFormDelete');
                 $("#exampleModal").modal('hide');
                 //updateTable();


                 },
            error : function (response){
            console.log('error')}
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
            let elementyTabeli=response.tabela_zbiorcza
            param=elementyTabeli.parametry.fields
            slownik=elementyTabeli.slownik
            wspolczynniki_wyparcia=elementyTabeli.wspolczynniki_wyparcia

            if(elementyTabeli.objects!=null){
            elementyTabeli=elementyTabeli.objects.sort((a, b) => a.pk- b.pk);
            //elementyTabeli=elementyTabeli.sort((a, b) => a.pk- b.pk);//to dodałem
            }else{elementyTabeli=[]}
//            elementyTabeli=elementyTabeli.objects
//            elementyTabeli=elementyTabeli.sort((a, b) => a.pk- b.pk)//to dodałem
            alerty=response.tabela_zbiorcza.alerty
            display=response.tabela_zbiorcza.wyswietlane_dane

            //elementyTabeli.sort((a, b) => a.elementyTabeli.pk > b.elementyTabeli.pk)
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


        for (const [key, value] of Object.entries(param)){ if ( value!=null && value!='0' && value!=''  ){
               const div=document.createElement('div')
                  div.setAttribute('class','flex-item-param')
                  if (slownik.hasOwnProperty(key) & key=='date'){
                  div.innerHTML+=' '+slownik[key]+': '
                  div.innerHTML+=value.slice(0,16).replace('T',' godz:')}
                  else if (key=='rodzaj'  & value=='czopki_i_globulki'){
                  }
                  else if (slownik.hasOwnProperty(key)){
                  div.innerHTML+=' '+slownik[key]+': ';
                  if (slownik.hasOwnProperty(value)){div.innerHTML+=slownik[value]}else{
                  div.innerHTML+=value}
                  }
                  else if (key!='session'){
                  div.innerHTML+=' '+key+': '
                  div.innerHTML+=value}
             if(div.innerHTML!='' & key!='owner'){
             if (key==='nazwa' || key==='date' ){li.appendChild(div)}else{
             li2.appendChild(div)}}
                                                    }
             else { if (slownik.hasOwnProperty(key) && param['rodzaj']=='czopki_i_globulki' ) {const div=document.createElement('div')
                  div.setAttribute('class','flex-item-param')
                  div.innerHTML+=' '+slownik[key]+': nie podano ilości'
                  li2.appendChild(div)}}

                                                    }
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
            if(item.fields.jednostka_z_recepty==='gramy_roztworu'){div.innerHTML+='sol. '}
            if (item.fields.aa==='on'){div.innerHTML+='aa '}
            else if(item.fields.aa_ad==='on'){div.innerHTML+='aa ad '}
            else if(item.fields.ad==='on'){div.innerHTML+='ad '}
            else if(item.fields.qs==='on'){div.innerHTML+='qs '}
            else if(item.fields.jednostka_z_recepty==='krople'){div.innerHTML+='gutt. '}
            if (item.fields.ilosc_na_recepcie!=='' && parseFloat(item.fields.ilosc_na_recepcie)%1==0) {div.innerHTML+=parseFloat(item.fields.ilosc_na_recepcie).toFixed(1)}//10.toFixed(2)
            else if (item.fields.ilosc_na_recepcie!=='' && parseFloat(item.fields.ilosc_na_recepcie)%1!=0) {div.innerHTML+=item.fields.ilosc_na_recepcie}
            if (item.fields.jednostka_z_recepty==='jednostki') {div.innerHTML+=' j.m.'}

            div.appendChild(deleteButton);
            tabelaDocelowa.appendChild(div);
            }



            //div.innerHTML+='<br>'
            ///////////////dodawanie kart/////////////////


      card=document.createElement('div')

          card.setAttribute('class','card-css')
          //card.setAttribute('style','width: 36rem;')

   var ul=document.createElement('ul')
        ul.setAttribute('class','list-group-skl')
   var li=document.createElement('li')
        li.setAttribute('class','my-card-header')
        li.setAttribute('value', item.pk)

        li.setAttribute('style','padding:5px; font-size: 20px; background-color: white; height: 3.5rem; ')
   var span=document.createElement('span')
//        if (item.fields.skladnik=='3% roztwór kwas borowy' && item.fields.czy_zlozyc_roztwor_ze_skladnikow_prostych=='on')
//        {span.innerHTML=numElem+')   kwas borowy'}else{
        span.innerHTML=numElem+')   '+item.fields.skladnik//}

   var buttonDel=document.createElement('button')
       buttonDel.innerText='Usuń'
       buttonDel.setAttribute('class','btn btn-secondary mt-1 button-card')
       buttonDel.setAttribute('id','button-del')
   var buttonEd=document.createElement('button')
       buttonEd.innerText='Edytuj'
       buttonEd.setAttribute('class','btn btn-primary mt-1 button-card')
       buttonEd.setAttribute('id','button-ed')
   if (item.fields.skladnik=='Etanol'|| item.fields.skladnik=="Oleum Cacao"){
   var buttonObl=document.createElement('button')
       buttonObl.innerText='Obliczenia'
       buttonObl.setAttribute('class','btn btn-secondary mt-1 button-card')
       if (item.fields.skladnik=='Etanol'){buttonObl.setAttribute('id','button-obl-et');
        buttonObl.onclick = function() { $("#oblEtModal").modal('show');
         oblEt();}
       }
       else if  (item.fields.skladnik=="Oleum Cacao"){
       buttonObl.setAttribute('id','button-obl-ol');
       buttonObl.onclick = function() { $("#oblOlModal").modal('show');
       oblOlCacao();}
       }
       }
       li.appendChild(buttonDel)
       li.appendChild(buttonEd)
       if(buttonObl!=null){li.appendChild(buttonObl)}
//
//       }
       li.append(span)
       ul.appendChild(li)

   buttonDel.onclick = function() {usuwanieSkladnika(item.pk);
            }
   buttonEd.onclick = function() {generowanieFormularzaDoEdycji(item.fields.skladnik ,item.pk);
            }
   var li2=document.createElement('li')
       //li2.classList.add( 'li-inline');
       li2.setAttribute('class','flex-container')
       //li2.setAttribute('class','li-inline')

        /////////wypisywanie atrybutów danego składnika/////

//        for (const [key, value] of Object.entries(item.fields)){ if ( value!=null && value!='0' && value!=''  ){
//               const div=document.createElement('div')
//                  div.setAttribute('class','flex-item')
//                  if (key in slownik){console.log('jest w słowniku')
//                  div.innerHTML+=' '+slownik[key]+': '
//                  div.innerHTML+=value}else{
//                  div.innerHTML+=' '+key+': '
//                  div.innerHTML+=value}
//             li2.appendChild(div)
//                                                    }}
        ///////////////////////////////////////////////////
        /////////wypisywanie wybranych atrybutów do karty///////////////////////////////////

        for (const [key, value] of Object.entries(item.fields)){ if ( value!=null && value!='0' && value!='' && display[item.fields.skladnik].includes(key) ){
               const div=document.createElement('div')
                  div.setAttribute('class','flex-item')
                  if (key in slownik){
                  div.innerHTML+=' '+slownik[key]+': '
                  div.innerHTML+=value}else{
                  div.innerHTML+=' '+key+': '
                  div.innerHTML+=value}
             li2.appendChild(div)
                                                    }}
        if (param['rodzaj']==='czopki_i_globulki' && wspolczynniki_wyparcia.hasOwnProperty(item.fields.skladnik) && item.fields.skladnik != 'Oleum Cacao'){
               const div=document.createElement('div')
                  div.setAttribute('class','flex-item')

                  div.innerHTML='współczynnik wyparcia: '+wspolczynniki_wyparcia[item.fields.skladnik]
             li2.appendChild(div)}
        ////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
            }else if (param['rodzaj']==='receptura_plynna_wewnetrzna' || param['rodzaj']==='receptura_plynna_zewnetrzna'){
            div=document.createElement('div');
            div.innerHTML='<br>M.f. Sol. ';
            tabelaDocelowa.appendChild(div)
            }


            if (alerty!=null && alerty['alert']!=''){alert(alerty['alert'])}
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

//updateTable()


/////////////////edycja danych składnika//////////////////////////
////////////////tworzenie formularza z danymi do edycji///////////////
function generowanieFormularzaDoEdycji (item,pk){

          //skl = item || inputBox.value;
//          if(item){skl=item}else{
//          skl=inputBox.value}
          if (item!='[object MouseEvent]'){skl=item}else{skl=inputBox.value}
//          skl=item || inputBox.value


          removeElementsByClass('elFormDelete')
          const div=document.createElement('div')
          div.setAttribute('class','elFormDelete');
          div.textContent='Edycja składnika'
          div.setAttribute('id','form-header')
          formBox.appendChild(div)
          modalFormHeaderBox=document.getElementById('form-header')
          const br=document.createElement('br')
          br.setAttribute('class','elFormDelete')
          formBox.appendChild(br)
          dodajSkladnikButton.style.visibility = "hidden"
          edytujSkladnikButton.style.visibility = "hidden"
          zapiszZmianyButton.style.visibility = "visible"
          zapiszZmianyButton.setAttribute('value', pk)




          modalTytul.innerText=skl;
           $("#exampleModal").modal('show');
           ////////////////ajax pobieranie elementów formularza///////////////////////////////

            $.ajax({
            type: 'GET',
            url: `editFormJson/${pk}/`,
            success : function(response){

            var elementyForm = response.datadict.form
            var dict=response.slownik


            elementyForm.map(item=>{
            if(Array.isArray(item)){

                const div=document.createElement('div')
                div.setAttribute('class', 'elFormDelete input-field-form')
                const label=document.createElement('label')
                label.textContent=dict[item[0]]
                label.setAttribute('class','elFormDelete');
                const select=document.createElement('select');
                select.setAttribute('class',"ui dropdown");


                //select.setAttribute('id',"optionId");
                select.setAttribute('class','elFormDelete')
                select.setAttribute('id',`${skl}-${item[0]}`)

                div.appendChild(label)
                div.appendChild(select)
                formBox.appendChild(div)

                //const optionBox= document.getElementById('optionId')
                const optionBox= document.getElementById(`${skl}-${item[0]}`)
                const slicedArray=item.slice(1)

                slicedArray.map(elem=>{
                const option=document.createElement('option')
                option.textContent = elem
                option.value=elem
                if(dict.hasOwnProperty(elem)){option.textContent = dict[elem]}else{option.textContent = elem}
                optionBox.appendChild(option)
                optionBox.value=response.datadict.values[item[0]]
                })
            }else{

            if (['aa','aa_ad','dodaj_wode','ad','qs','czy_zlozyc_roztwor_ze_skladnikow_prostych','czy_zlozyc_roztwor_ze_skladnikow_prostych','czy_powiekszyc_mase_oleum'].includes(item)){
            const label=document.createElement('label')
            label.textContent=dict[item]
            const check = document.createElement("input");
            check.setAttribute('type',"checkbox")
            if (response.datadict.values[item]==='on'){check.checked = true;
            check.setAttribute('value','on')}else{
            check.setAttribute('value','off')}
            check.setAttribute('id',`${skl}-${item}`)

            if (['aa','aa_ad','ad','qs'].includes(item)){check.setAttribute('name','check');
            check.setAttribute('onclick',"onlyOne(this)")}
            check.setAttribute('class','elFormDelete check-box')
            label.setAttribute('class','elFormDelete')
            formBox.appendChild(label)
            formBox.appendChild(check)
            } else
            {

            const label=document.createElement('label')
            const input=document.createElement('input')
            input.setAttribute('class','elFormDelete')
            label.setAttribute('class','elFormDelete')
            input.setAttribute('id',`${skl}-${item}`)
            input.setAttribute('type','number')
            input.setAttribute("min","0")
            input.setAttribute('max',"99999")
            const br=document.createElement('br')
            br.setAttribute('class','elFormDelete')
            label.textContent=dict[item]
            if(response.datadict.values[item]!='' || response.datadict.values['qs']=='on'|| response.datadict.values['show']!=false){
            input.value=response.datadict.values[item]
            formBox.appendChild(label)
            formBox.appendChild(input)
            formBox.appendChild(br)}
            else{modalFormHeaderBox.textContent='brak możliwości edycji';
            zapiszZmianyButton.style.visibility = "hidden";}
            }}
            })

            },
            error : function (response){
            console.log('error')}
            })
            }






//////////////////////3pozycja/////////////////////////////////////////////////////

function edytowanieSkl(pk){
            var skladnik=modalTytul.innerText
            //skl=inputBox.value || skladnik;
            skl=skladnik
            $.ajax({
            type: 'GET',
            url: `editFormJson/${pk}/`,
            success : function(response){
            var elementyForm = response.datadict
            var dict=response.table_dict
                const checkButtons = document.getElementsByClassName('check-box')
                for (let check of checkButtons){if (check.checked){ check.value='on'}else{check.value='off'}}
                /////////////////////////////////////////////////////////////////////////////
                ///tworzenie daty formulara i odpowiedzi do ajaxa////////////////////
                dataf={'csrfmiddlewaretoken': csrft[0].value,'skladnik':skl,'receptura_id':sklId}
                elementyForm=elementyForm.form
                for ( var i in elementyForm )if ( Array.isArray(elementyForm[i])){
                dataf[elementyForm[i][0]]=document.getElementById(`${skl}-${elementyForm[i][0]}`).value}
                else
                {
                dataf[elementyForm[i]]=document.getElementById(`${skl}-${elementyForm[i]}`).value}

                if (dataf['skladnik']=="Oleum Cacao" && dataf['qs']=='on'){dataf['ilosc_na_recepcie']=''}

                $.ajax({
                type: 'POST' ,
                url:`edytujskl/${pk}/`,
                data : dataf,
                success: function(response){
                         console.log('wygrywamy');

                         tabelaDocelowa.innerHTML='';
                         updateTable();
                                        },
                error : function(error){
                         console.log('nie działa');
                                                    }
                 });
                 /////koniec ajaxa
                 removeElementsByClass('elFormDelete');
                 $("#exampleModal").modal('hide');
                 },
            error : function (response){
            console.log('error')}
            })
            }

                    /////tu koniec wstawania//////

function oblOlCacao(){ $.ajax({
            type: 'GET',
            url:`obliczeniaOlCac/${sklId}/`,
            success : function(response){
            const daneSkladnikow =document.getElementById('dane')
            const oblOlText=document.getElementById( "ol-obl-text")
            removeElementsByClass('elFormDelete');
            response.dane.map(item=> {
               const tr=document.createElement('tr');
               item.map(item2=>{
               const td=document.createElement('td');
               td.innerText=item2
               td.setAttribute('class','elFormDelete')
               tr.appendChild(td)
               })
               tr.setAttribute('class','elFormDelete oblOlSkladniki')
                daneSkladnikow.appendChild(tr)
            })
            oblOlText.innerHTML=response.obliczenia
            },
            error : function(response){},
            })
            }
function oblEt(){ $.ajax({
            type: 'GET',
            url:`obliczeniaEt/${sklId}/`,
            success : function(response){

            const oblEtText=document.getElementById( "ol-et-text")

            oblEtText.innerHTML=''
            const p=document.createElement('p')
            p.innerHTML= response.tabela['obl']+response.tabela['obl1']
            oblEtText.appendChild(p)
            MathJax.typesetPromise()
            },
            error : function(response){},
            })
            }


function wyborSkladnikowDropFunc(){

          const ul=document.createElement('ul')
          ul.setAttribute('class','column-dropdown')
          ingridients.map(item=>{
          const p=document.createElement('p')
          p.setAttribute('class','drop-ingridient-item')
          const a=document.createElement('a')
          a.setAttribute('class',"dropdown-item");
          a.setAttribute('onclick',`if(getElementById('myInput')!=null){getElementById('myInput').value = '${item}'; generowanieFormularza()}else{myFunction()}`);
          a.innerText=item
          p.appendChild(a)
          ul.appendChild(p)
          })
          wyborSkladnikowDrop.appendChild(ul)
          }

wyborSkladnikowDropFunc()
autocompleteButton.addEventListener( 'click',generowanieFormularza );
dodajSkladnikButton.addEventListener('click',dodawanieSkl );
edytujSkladnikButton.addEventListener('click',generowanieFormularzaDoEdycji)

zapiszZmianyButton.addEventListener('click',e=>{edytowanieSkl(zapiszZmianyButton.value)})
closeButton.addEventListener('click',e=>{$("#exampleModal").modal('hide');
                                           removeElementsByClass('elFormDelete'); })
closeXMyjsButton.addEventListener('click',e=>{$("#exampleModal").modal('hide');
                                           removeElementsByClass('elFormDelete'); })






modalBox.addEventListener('hidden.bs.modal', function (event) {
    removeElementsByClass('elFormDelete');

});



////////////////////////////////////////////////////////////////////////////////////////////////












