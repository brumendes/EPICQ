$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$(document).ready(function($) {
    $(".table-row").click(function() {
        window.document.location = $(this).data("href");
    });
});