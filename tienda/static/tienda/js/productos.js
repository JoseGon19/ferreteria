function increment(id, maxStock) {
    let input = document.getElementById("cantidad-" + id);
    let value = parseInt(input.value);
    if (value < maxStock) {
        input.value = value + 1;
    }
}

function decrement(id) {
    let input = document.getElementById("cantidad-" + id);
    let value = parseInt(input.value);
    if (value > 1) {
        input.value = value - 1;
    }
}