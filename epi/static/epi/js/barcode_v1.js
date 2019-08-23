$(document).scannerDetection({
	timeBeforeScanTest: 200, // wait for the next character for upto 200ms
	startChar: [120], // Prefix character for the cabled scanner (OPL6845R)
	endChar: [13], // be sure the scan is complete if key 13 (enter) is detected
	avgTimeByChar: 40, // it's not a barcode if a character takes longer than 40ms
	onComplete: function(barcode, qty){
	    var arr = barcode.split("'");
	    var sala = arr[0];
	    var tipo = arr[1].toLowerCase();
	    var id = arr[2];
	    var slug = tipo + "-" + id
	    $.ajax({
	        'url': '/',
	        'method': 'GET',
	        'cache': false,
	        'success': function (){
	            $('input[name=slug]').val(slug);
	            $('#scanner_form').submit();
	        }
	    });
	} // main callback function
});