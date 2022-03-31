$(document).ready(function(){
    $('#owner_join').click(admin);
    $('#basic_join').click(basic);
});

function admin(){
    document.forms['admin'].submit();
}

function basic(){
    document.forms['basic'].submit();
}