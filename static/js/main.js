$(document).ready(function() {
    //Set default hint if nothing is entered
    setHints();

    //Load initial site state (countdown)
    initialize();
});
var setHints = function()
{
    $('#subscribe').attachHint('Informe-nos o seu E-mail para ser notificado em breve');
    $('.contactBackground [name=name]').attachHint('Nome');
    $('.contactBackground [name=email]').attachHint('E-mail');
    $('.contactBackground [name=subject]').attachHint('Assunto');
    $('.contactBackground [name=message]').attachHint('Mensagem');
};
var initialize = function()
{
    setInterval(function(){
        var countDownObj = calculateTimeDifference("2012/05/24");
        if(countDownObj){
            $('#days').text(countDownObj.Days);
            $('#hours').text(countDownObj.Hours);
            $('#minutes').text(countDownObj.Minutes);
            $('#seconds').text(countDownObj.Seconds);
        }
    }, 1000);
};
var getFriendlyTwitterTime = function(raw_time){
	var date = new Date((raw_time || "").replace(/-/g,"/").replace(/[TZ]/g," ")),
		diff = (((new Date()).getTime() - date.getTime()) / 1000),
		day_diff = Math.floor(diff / 86400);
			
	if ( isNaN(day_diff) || day_diff < 0 || day_diff >= 31 )
		return;
			
	return day_diff == 0 && (
			diff < 60 && "just now" ||
			diff < 120 && "1 minute ago" ||
			diff < 3600 && Math.floor( diff / 60 ) + " minutes ago" ||
			diff < 7200 && "1 hour ago" ||
			diff < 86400 && Math.floor( diff / 3600 ) + " hours ago") ||
		day_diff == 1 && "Yesterday" ||
		day_diff < 7 && day_diff + " days ago" ||
		day_diff < 31 && Math.ceil( day_diff / 7 ) + " weeks ago";
}

var resetInput = function(){
    $('input, textarea').each(function() {
        $(this).val('').text('');
    });
};

var calculateTimeDifference = function(startDate) {
    var second = 1000;
    var minute = second * 60;
    var hour = minute * 60;
    var day = hour * 24;

    var seconds = 0;
    var minutes = 0;
    var hours = 0;
    var days = 0;

    var currentDate = new Date();
    startDate = new Date(startDate);
    
    var timeCounter = startDate - currentDate;
    if (isNaN(timeCounter))
    {
        return NaN;
    }
    else
    {
        days = Math.floor(timeCounter / day);
        timeCounter = timeCounter % day;

        hours = Math.floor(timeCounter / hour);
        timeCounter = timeCounter % hour;

        minutes = Math.floor(timeCounter / minute);
        timeCounter = timeCounter % minute;
        
        seconds = Math.floor(timeCounter / second);
    }

    var tDiffObj = {
        "Days" : days,
        "Hours" : hours,
        "Minutes" : minutes,
        "Seconds" : seconds
    };

    return tDiffObj;
};

var StringFormat = function() {
    var s = arguments[0];
    for (var i = 0; i < arguments.length - 1; i++) {
        var regExpression = new RegExp("\\{" + i + "\\}", "gm");
        s = s.replace(regExpression, arguments[i + 1]);
    }
    return s;
}
var showMessage = function (msg) {
    alert(msg);
}
