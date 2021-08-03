var probar = document.getElementsByClassName('progress-bar')[0];
function myFunction() {
    if(document.getElementById("jobDescription").value != '')
    {
        var w = parseInt(probar.style.width);
        while(w!=parseInt("100")){
            w = w + parseInt("10");
            probar.style.width =  w+"%";
            probar.innerHTML = w+"%";
            if(parseInt(w)>parseInt("100")){
                w = parseInt("100");
                probar.style.width =  w+"%";
                probar.innerHTML = w+"%";
            }
            console.log(probar.style.width);
        }
        document.getElementById("fs").style.display = "none";
        document.getElementById('fd').innerHTML= 
        `<div class='text-center' style="display: flex;height: 97vh;align-items: center;justify-content: center;flex-direction: column;">
            <div class='spinner-border' role='status' style="width: 5rem;height: 5rem;border: 1.2rem solid currentColor;border-right-color: transparent;">
                <span class='sr-only'></span>
            </div>
            <h4>Proccessing...</h4>
        </div>`;
    }
}
var buttons = document.querySelectorAll('.radio');
for( i=0; i<buttons.length; i++ ) {
    buttons[i].addEventListener('change',function(){
        document.querySelector('#jobDescription').value = this.value;
    });
}