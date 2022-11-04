function testowySlownik(){
var ret={}
$.ajax({
            type: 'GET',
            url: 'testowyslownik/',
            async: false,
            success : function(response){
            console.log('succes testowego słownika', response);
            ret=response.testowy_slownik;

            },
            error : function (response){
            console.log('error', error)}
            })

            return ret
            }

function test(){
var magma='magma';
return magma;
}

var test=test();
console.log('test',test)
