
const currentLocation = location.href;
const split = currentLocation.split('/')
const currentQuestion = split[split.length - 1];
const nextQuestion = +currentQuestion + 1;
split[split.length - 1] = nextQuestion;
const pages = $('.page-item').length;
$(window).on('hashchange', function(){
    console.log('eee')
    if(nextQuestion > pages){
        const end = 'end';
        split[split.length - 1] = end;
        window.location.href = split.join('/');
    }
})

$('#nextQuestion').on('click', function(){
    window.location.href = split.join('/');
})
