// Bootstrap Slider
$(function() {
  $('#bs-slider-1').slider({
    formatter: function(value) {
      return 'Value: ' + value;
    },
  });

  $('#bs-slider-2').slider();

  $('#bs-slider-3').slider({
    reversed: true,
  });

  $('#bs-slider-4').slider({
    reversed: true,
  });

  $('#bs-slider-5').slider();

  $('#bs-slider-6').slider({
    ticks:        [0, 100, 200, 300, 400],
    ticks_labels: ['$0', '$100', '$200', '$300', '$400'],
  });

  $('#bs-slider-7').slider({
    ticks:        [0, 100, 200, 300, 400],
    ticks_labels: ['$0', '$100', '$200', '$300', '$400'],
    reversed:     true,
  });

  $('.bs-slider-variant').slider();
});
