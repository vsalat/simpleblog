var amountScrolled = 1;
var scrollpos = 0
var scrollock = false
$(window).scroll(function() {
	console.log('scroll',amountScrolled)
	if ( $(window).scrollTop() > amountScrolled ) {
		$('.hor-nav').show();
		$('.hor-nav .up-arr').show();
		$('.hor-nav .down-arr').hide()
	} else {
		if (scrollock){
			scrollock = false
		}
		else{
			$('.hor-nav').hide();	
		}
		
	}
});
$(document).ready(function(){
	$('.hor-nav .up-arr').bind('click',function(){
		scrollpos = $(window).scrollTop();
		$('html, body').animate({
			scrollTop: 0
		}, 300,function(){
			$('.hor-nav').show()
			$('.hor-nav .up-arr').hide()
			$('.hor-nav .down-arr').show()		
			scrollock = true
		})

	})
	$('.hor-nav .down-arr').bind('click',function(){
		$('html, body').animate({
			scrollTop: scrollpos
		}, 300);
		$('.hor-nav .down-arr').hide()
		$('.hor-nav .up-arr').show()
	})
})
