jQuery.fn.rating = function(options) {
	var settings = {
    increment : 1, // value to increment by
    maxvalue  : 5,   // max number of stars
    curvalue  : 0,    // number of selected stars
    change    : 0
  };
	
  if(options) {
    jQuery.extend(settings, options);
  };
   
  var container = jQuery(this), phrase=new Array("很差","一般","还行","推荐","力荐");
	
	jQuery.extend(container, {
    averageRating: settings.curvalue,
  });
  settings.increment = (settings.increment < .75) ? .5 : 1;
  var s = 1;
	for(var i= 0.5; i <= settings.maxvalue ; i++){
    var $div = $('<div class="star"></div>')
      .append('<p id="star'+i+'">'+i+'</a>')
      .appendTo(container);
    if (settings.increment == .5) {
      if (s%2) {
        $div.addClass('star-left');
      } else {
        $div.addClass('star-right');
      }
    }
    i=i-1+settings.increment;
    s++;
  }
	jQuery(container).append('<p></p>');
	var stars = jQuery(container).children('.star');
	
  stars
    .mouseover(function(){
      event.drain();
      event.fill(this);
    })
    .mouseout(function(){
      event.drain();
      event.reset();
    })
    .focus(function(){
      event.drain();
      event.fill(this);
    })
    .blur(function(){
      event.drain();
      event.reset();
    })
    .click(function(){
      if (settings.change){
        settings.curvalue=parseInt(($(this).index()+2)/2);
        $("#trinity1").attr("data-value",settings.curvalue);
        event.drain();
        event.reset();
      }
    });

	var event = {
		fill: function(el){ // fill to the current mouse position.
			var index = stars.index(el) + 1;
      if (index%2==1)
        index+=1;
			stars
				.children('p').css('width', '100%').end()
				.slice(0,index).addClass('hover').end();
      container.children('p').html(phrase[index/2-1]);
      container.children('p').attr('style',"margin-bottom:-0.5em;margin-left:90px;");
		},
		drain: function() { // drain all the stars.
			stars
				.filter('.on').removeClass('on').end()
				.filter('.hover').removeClass('hover').end();
      container.children('p').html("");
      container.children('p').attr('style',"");
		},
		reset: function(){ // Reset the stars to the default index.
			stars.slice(0,settings.curvalue / settings.increment).addClass('on').end();
		}
	};
	event.reset();
	
	return(this);	

};