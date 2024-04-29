window.dccFunctions = window.dccFunctions || {};
window.dccFunctions.trafo_L = function(value) {
    if (value < Math.log10(1.25)) {
        return 0; 
    } else {
        return Math.round(Math.pow(10, value));
    }
}