var probar = document.getElementsByClassName('progress-bar')[0];
function myFunction() {
    if(document.getElementById("myFile").value != '')
    {
        var w = parseInt(probar.style.width);
        while(w!=parseInt("50")){
            w = w + parseInt("10");
            probar.style.width =  w+"%";
            probar.innerHTML = w+"%";
            if(parseInt(w)>parseInt("50")){
                w = parseInt("50");
                probar.style.width =  w+"%";
                probar.innerHTML = w+"%";
            }
            console.log(probar.style.width);
        }
        document.getElementById("fs").style.display = "none";
        document.getElementById('fd').innerHTML= 
        `<div class='text-center' style="display: flex;height: 97vh;align-items: center;justify-content: center;flex-direction: column;">
            <div class='spinner-border' role='status' style="
            width: 5rem;
            height: 5rem;
            border: 1.2rem solid currentColor;
            border-right-color: transparent;">
                <span class='sr-only'></span>
            </div>
            <h4>Proccessing...</h4>
            </div>`;
    }
}