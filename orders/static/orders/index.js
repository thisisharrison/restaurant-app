document.addEventListener('DOMContentLoaded', () => {
    const toppings = document.querySelector('#toppings');
    toppings.onchange = function () {
        let chosentops = []
        const arr = toppings.selectedOptions
        for (let i = 0, len = arr.length; i < len; i++) {
            chosentops.push(arr[i].text);
        }
        const li = document.querySelector('.chosentoppings');
        li.style.visibility = "visible";
        li.innerHTML = chosentops;
    }
})