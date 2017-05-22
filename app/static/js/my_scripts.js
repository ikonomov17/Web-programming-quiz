const currentLocation = location.href;
const split = currentLocation.split('/')
const currentQuestion = split[split.length - 1];
const nextQuestion = +currentQuestion + 1;
split[split.length - 1] = nextQuestion;
const pagesCount = $('.page-item').length;

let currentPage;
$('.my-page-link').each((index, element) => {
    if($(element).attr('href').indexOf(currentQuestion) != -1){
        $(element).parent().addClass('active');
        // return false to break the loop
        return false;
    }
});

current_path = window.location.pathname
current_question = $('.active').children()[0].text
$('#current_view_number').attr('value',current_question)
   


