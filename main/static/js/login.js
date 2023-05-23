let input=document.querySelector('.input')
let see = document.querySelector('.see')

see.addEventListener('click', ()=>{
    see.classList.toggle('hide')
    if(input.type === 'password'){
        input.type = 'password';
    }
    else{
        input.type = 'password';
    }
})