var buyform = document.querySelector('.buyform')
var buy = document.querySelector('.buy')
var formbuy = document.querySelector('.formbuy')

buy.addEventListener('click', () => {
    setTimeout(() =>{
        buyform.style.display = 'block'
    }, 2000)
})


formbuy.addEventListener('click', () => {
        buyform.style.display = 'none'
})