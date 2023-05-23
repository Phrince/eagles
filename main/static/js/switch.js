let body=document.querySelector('body')
let david=document.querySelector('.david')
let icon=document.querySelector('.bi-moon-fill')

david.addEventListener('click', ()=>{
    body.classList.toggle('dark')
    if(body.classList.contains('dark')){
        icon.classList.replace('bi-moon-fill', 'bi-brightness-high-fill')
    }
    else{
        icon.classList.replace('bi-brightness-high-fill', 'bi-moon-fill')
    }
})