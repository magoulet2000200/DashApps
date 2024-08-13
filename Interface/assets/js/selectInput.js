window.onload = function () {
    setTimeout(function () {
        var input = document.getElementById('input_host_id');
        if (input != null) {
            input.focus();
            input.select();
            console.log(input);
        }
    }, 500); // Delay of 500 miliseconds
}
