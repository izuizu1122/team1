// トースト通知機能
function showToast(message,type='info'){

let container=document.querySelector('.toast-container');

if(!container){
container=document.createElement('div');
container.className='toast-container';
document.body.appendChild(container);
}

const toast=document.createElement('div');
toast.className='toast '+type;
toast.innerText=message;

container.appendChild(toast);

setTimeout(()=>{
toast.classList.add('fadeOut');

setTimeout(()=>{
toast.remove();
},300);

},4000);

}
