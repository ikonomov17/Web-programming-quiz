 var q = [
        {'Q':'How do you write "Hello World" in an alert box?', 'A':2,'C':['msg("Hello World");','alert("Hello World");','alertBox("Hello World");'],'H':"Hint 1"},
        {'Q':'How do you create a function in JavaScript?', 'A':3,'C':['function:myFunction()','function = myFunction()','function myFunction()'],'H':"Hint 1"},
        {'Q':'How to write an IF statement in JavaScript?', 'A':1,'C':['if (i == 5)','if i = 5 then','if i == 5 then'],'H':"Hint 1"},
        {'Q':'How does a FOR loop start?', 'A':2,'C':['for (i = 0; i <= 5)','for (i = 0; i <= 5; i++)','for i = 1 to 5'],'H':"Hint 1"},
        {'Q':'What is the correct way to write a JavaScript array?', 'A':3,'C':['var colors = "red", "green", "blue"','var colors = (1:"red", 2:"green", 3:"blue")','var colors = ["red", "green", "blue"]'],'H':"Hint 1"}
    ];


$(function(){
    var loading = $('#loadbar').hide();
    $(document)
    .ajaxStart(function () {
        loading.show();
    }).ajaxStop(function () {
    	loading.hide();
    });
    

	var choicecount = 1;
    var allowchoice  = true;
    var questionNo = 0;
    
    $('#question').html(q[questionNo].Q);
	$($('#f-option').parent().find('label')).html(q[questionNo].C[0]);
	$($('#s-option').parent().find('label')).html(q[questionNo].C[1]);
	$($('#t-option').parent().find('label')).html(q[questionNo].C[2]);
		 

    $(document.body).on('click',"#show-hint-button",function (e) {
		$('.show-hint').removeClass('hidden');    	
	});

    $(document.body).on('click',"label.element-animation",function (e) {
    	var choice = $(this).parent().find('input:radio').val();
        console.log(choice);
    	var anscheck =  $(this).checking(questionNo, choice);//$( "#answer" ).html(  );      
    	var thisel = $(this);
        // q[questionNo].UC = choice;
        // console.log(anscheck);
        if(anscheck){//answer correct
            // correctCount++;
            // q[questionNo].result = "Correct";
            allowchoice = false;
        } else {//answer wrong
            // q[questionNo].result = "Incorrect";        
            $(this).addClass('cross');
            $($(this).parent().find('.check')).addClass('cross');
            $($(this).parent().find('.inputoption')).addClass('cross');
        }
        choicecount++;
    	if(choicecount > 2){//crossed limit of choosing option
    		console.log(choicecount+" greater than 2");
			allowchoice = false;
    	}	
		if(allowchoice){
			if(choicecount > 1){
				$('.show-hint').html(q[questionNo].H);
				$('#show-hint-button').prop('disabled', false);
			}
		} else {
	        setTimeout(function(){
	            $('#loadbar').show();
	            $('#quiz').fadeOut();
				
				$('.inputoption').removeClass('cross');
            	$('.check').removeClass('cross');
            	$('.inputoption').removeClass('cross');
        	
	            questionNo++;
	         	choicecount = 1;
	         	allowchoice = true;
	         	$('#show-hint-button').prop('disabled', true);
				$('.show-hint').addClass('hidden');  

				 
            //show answer and go to next question
				if((questionNo + 1) > q.length){
	                alert("Quiz completed, Now click ok to get your answer");
	                $('label.element-animation').unbind('click');
	                setTimeout(function(){
	                    var toAppend = '';
	                    $.each(q, function(i, a){
	                        toAppend += '<tr>'
	                        toAppend += '<td>'+(i+1)+'</td>';
	                        toAppend += '<td>'+a.A+'</td>';
	                        toAppend += '<td>'+a.UC+'</td>';
	                        toAppend += '<td>'+a.result+'</td>';
	                        toAppend += '</tr>'
	                    });
	                    $('#quizResult').html(toAppend);
	                    $('#totalCorrect').html("Total correct: " + correctCount);
	                    $('#quizResult').show();
	                    $('#loadbar').fadeOut();
	                    $('#result-of-question').show();
	                }, 1000);
            	} else {
					$('#qid').html(questionNo + 1);
                	$('input:radio').prop('checked', false);
		    	    setTimeout(function(){
		            	$('#quiz').show();
		            	$('#loadbar').fadeOut();
		          	}, 1000);
		            $('#question').html(q[questionNo].Q);
		            $($('#f-option').parent().find('label')).html(q[questionNo].C[0]);
		            $($('#s-option').parent().find('label')).html(q[questionNo].C[1]);
		            $($('#t-option').parent().find('label')).html(q[questionNo].C[2]);
		        }
	        }, 1000);
		}
	});


    $.fn.checking = function(qstn, ck) {
        var ans = q[questionNo].A;
        console.log(ans);
        if (ck != ans)
            return false;
        else 
            return true;
    }; 

});