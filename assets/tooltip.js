window.dccFunctions = window.dccFunctions || {};
window.dccFunctions.trafo_L = function(value) {
    if (value < Math.log10(1.25)) {
        return 0; 
    } else {
        return Math.round(Math.pow(10, value));
    }
}
window.dccFunctions.transform_log_nice = function(value) {
    let x = Math.pow(10, value);
    // same as transform_up in log_slider.py
    if (x == 0){
        return 0;
    }
    const sign = Math.sign(x);
    x = Math.abs(x);

    let step = Math.pow(10, Math.floor(Math.log10(x))) / 10;
    let nice_value = sign * Math.round(x / step) * step;
    nice_value = Number(nice_value.toFixed(4));
    return nice_value;
}

window.dccFunctions.transform_fib = function(value) {
    function fibonacci(n) {
        return n < 1 ? 0
             : n <= 2 ? 1
             : fibonacci(n - 1) + fibonacci(n - 2)
     }
     return fibonacci(value);
}

window.dccFunctions.transform_square = function(value) {
    return value * value;
}