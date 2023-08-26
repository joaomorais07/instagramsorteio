window.onload=()=>{
    const element = document.getElementById('btnMenu')
    element.addEventListener('click', abrir)
}

window.stop=()=>{
    const element = document.getElementById('loader')
    element.style.display='none'
}

function carregar(){
    const element = document.getElementById('loader')
    element.style.display='flex'
}

function stopLoad(){
    window.stop(); //stop loading the page
    window.location = "/principal"; //takes you somewhere
}

function abrir(){
    const element = document.getElementById('divMenu')
    element.style.display='flex'
    const btnMenu = document.getElementById('btnMenu')
    btnMenu.removeEventListener('click', abrir)
    btnMenu.addEventListener('click', fechar)
}

function fechar(){
    const element = document.getElementById('divMenu')
    element.style.display="none"
    btnMenu.removeEventListener('click', fechar)
    btnMenu.addEventListener('click', abrir)
}

function printar(dados){
    console.log(dados)
}