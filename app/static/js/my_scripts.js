const currentLocation = location.href;
const split = currentLocation.split('/')
const currentQuestion = split[split.length - 1];
const nextQuestion = +currentQuestion + 1;
split[split.length - 1] = nextQuestion;
const pagesCount = $('.page-item').length;

let currentPage;
$('.my-page-link').each((index, element) => {
    // if you don't want the other questions number to be disabled
    // remove the else and uncomment return false
    // WARNING! The numbers are just links and do not make a POST
    // request. This means that user answers won't be registered in DB.
    // Only Next button sends the data to the DB
    if($(element).attr('href').split('/')[2] == currentQuestion){
        $(element).parent().addClass('active');
        // return false
    } else {
        $(element).parent().addClass('disabled');
    }
});

current_path = window.location.pathname
current_question = $('.active').children()[0].text
$('#current_view_number').attr('value',current_question)
$('#qid').html(current_question)

if($('.my-page-item').last().hasClass('active')){
    $('#show-hint-button').html('End')
}
   


