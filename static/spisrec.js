console.log('spisRec')

const Receptury = document.getElementsByClassName('pk-class')

 for (let rec of Receptury){
                            console.log('rec',rec)
                            var skl=rec.title;
                            recIng(skl)}

function recIng(skl){

        const sklId=skl
        console.log('sklId',sklId)
         var tabelaDocelowa=document.getElementById(`${sklId}-skladniki`)
            //skladnikiRecepturyBox.innerHTML='dupa'
         tabelaDocelowa.innerHTML='';

         $.ajax({
            type: 'GET',
            url:`spisSkl/${sklId}/`,
            success : function(response){


            console.log('Sukces ajaxa z tabelą', response);
            let elementyTabeli=response.tabela_zbiorcza
            console.log('elementyTabeli', response.tabela_zbiorcza)
            param=elementyTabeli.parametry.fields

            elementyTabeli=elementyTabeli.objects



            ////////////////koniec testu//////////////////////////////
            //let tabelaDocelowa=document.getElementById("tabela-docelowa");
            tabelaDocelowa.innerHTML=''
            div=document.createElement('div')
            div.innerHTML='Rp. <br><br>'
            tabelaDocelowa.appendChild(div)
            var numElem=1
            if (elementyTabeli!=null){
            elementyTabeli=elementyTabeli.sort((a, b) => a.pk- b.pk)//to dodałem
            elementyTabeli.map(item=>{
            console.log('itemTabeli',item.fields.skladnik);
            const div=document.createElement('div')

            if (item.fields.show===true){
            div.innerHTML+= numElem+') ' + item.fields.skladnik+'  '
            if (item.fields.skladnik==='Etanol'){div.innerHTML+=item.fields.pozadane_stezenie+'° '}
            if (item.fields.aa==='on'){div.innerHTML+='aa '}
            else if(item.fields.aa_ad==='on'){div.innerHTML+='aa ad '}
            else if(item.fields.ad==='on'){div.innerHTML+='ad '}
            else if(item.fields.qs==='on'){div.innerHTML+='qs '}
            if (item.fields.ilosc_na_recepcie!=='') {div.innerHTML+=+item.fields.ilosc_na_recepcie}
            if (item.fields.jednostka_z_recepty==='jednostki') {div.innerHTML+=' j.m.'}
            console.log('div',div);
            numElem+=1
            tabelaDocelowa.appendChild(div);
            }
            })

            }
            if (param['rodzaj']==='czopki_i_globulki' & param["czopki_czy_globulki"]==='czopki'){
            div=document.createElement('div');
            div.innerHTML='<br><br>M.f. supp. anal. D.t.d. No '+param['ilosc_czop_glob'];
            tabelaDocelowa.appendChild(div)
            }else if (param['rodzaj']==='czopki_i_globulki' & param["czopki_czy_globulki"]==='globulki'){
            div=document.createElement('div');
            div.innerHTML='<br><br>M.f. glob. vag. D.t.d. No '+param['ilosc_czop_glob'];
            tabelaDocelowa.appendChild(div)
            }else if (param['rodzaj']==='masc'){
            div=document.createElement('div');
            div.innerHTML='<br><br>M.f. Ung. ';
            tabelaDocelowa.appendChild(div)
            }
            else if (param['rodzaj']==='receptura_plynna_wewnetrzna' || param['rodzaj']==='receptura_plynna_zewnetrzna'){
            div=document.createElement('div');
            div.innerHTML='<br>M.f. Sol. ';
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




