$(document).ready(function() {
    $("#scannerInput").change(function () {
        var numero = $(this).val();
        var arr = str.split("'");
        alert(numero);
        $.ajax({
            "type": "GET",
            "url": "scanner/teste/",
            "data": {'numero': numero},
            "dataType": 'json',
            "cache": false,
            "success": function (data) {
                            alert(data.messages);
                        }
        });
    });
});