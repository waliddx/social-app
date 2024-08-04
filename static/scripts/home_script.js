let dropmenu= document.getElementById('drop')
let button= document.getElementById('base')

button.onclick = ()=>{
    if (dropmenu.style.display == 'none'){
        dropmenu.style.display= 'block'
    } else {
        dropmenu.style.display= 'none'
    }
}
