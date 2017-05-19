$(document).ready(function(){
    const currentLocation = location.href;
    const split = currentLocation.split('/')
    const currentQuestion = split[split.length - 1];
    const nextQuestion = +currentQuestion + 1;
    split[split.length - 1] = nextQuestion;

    $('#nextQuestion').on('click', function(){
        window.location.href = split.join('/');
    })

})