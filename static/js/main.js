const btnDelete = document.querySelectorAll('.btn-borrar');

if(btnDelete){
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if(!confirm('¿Esta seguro de querer eliminar el registro?')){
                e.preventDefault();
            }
        });
    });
}