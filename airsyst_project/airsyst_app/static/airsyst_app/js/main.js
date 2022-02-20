$(document).ready(function ($) {
  $('.our-team__item').on('click', function () {
    $('.modal, .team-form').addClass('active');
  });

  $('.certificates__slide img').on('click', function () {
    $('.modal, .certificates-form').addClass('active');
  });

  $('.modal .close').on('click', function () {
    $('.modal, .team-form, .certificates-form').removeClass('active');
  });

  $('#sort').on('click', function () {
    $(this).siblings('.custom-select').toggleClass('active');
  });

  $('#sort').on('change', function () {
    $(this).siblings('.custom-select').find('span').html($(this).val());
  });


  $('.feedback__checkbox').on('click', function () {
    $(this).find('.feedback__check').toggleClass('active');
  });

  $('.card__thumb').on('click', function(){
    $(this).addClass('active').siblings().removeClass('active');
    $('.card__item').removeClass('active').eq($(this).index()).addClass('active');
  });

  var cardThumbsSwiper = new Swiper(".card__slider-thumbs", {
    spaceBetween: 15,
    slidesPerView: 3,
    freeMode: true,
    watchSlidesProgress: true,
  });


  var cardSwiper = new Swiper(".card__slider-main", {
    spaceBetween: 10,
    slidesPerView: 1,
    thumbs: {
      swiper: cardThumbsSwiper,
    },
  });


  var swiper = new Swiper(".reviews__slider, .certificates__slider", {
    slidesPerView: 3,
    spaceBetween: 3,
    slidesPerGroup: 1,
    loop: true,
    loopFillGroupWithBlank: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });

  var projectSwiper = new Swiper(".project__slider", {
    slidesPerView: 2,
    spaceBetween: 0,
    slidesPerGroup: 1,
    loop: true,
    loopFillGroupWithBlank: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });





  // range-slider
  var settings = {
    visible: 0, 
    theme: {
      backgroud: "rgba(0,0,0,.9)",
    },
    CSSVarTarget: document.querySelector('.range-slider'),
    knobs: [
      "Thumb",
      {
        cssVar: ['thumb-size', 'px'],
        label: 'thumb-size',
        type: 'range',
        min: 6, max: 33 //  value: 16,
      },
      "Value",
      {
        cssVar: ['value-active-color'], // alias for the CSS variable
        label: 'value active color',
        type: 'color',
        value: 'white'
      },
      {
        cssVar: ['value-background'], // alias for the CSS variable
        label: 'value-background',
        type: 'color',
      },
      {
        cssVar: ['value-background-hover'], // alias for the CSS variable
        label: 'value-background-hover',
        type: 'color',
      },
      {
        cssVar: ['primary-color'], // alias for the CSS variable
        label: 'primary-color',
        type: 'color',
      },
      {
        cssVar: ['value-offset-y', 'px'],
        label: 'value-offset-y',
        type: 'range', value: 5, min: -10, max: 20
      },
      "Track",
      {
        cssVar: ['track-height', 'px'],
        label: 'track-height',
        type: 'range', value: 8, min: 6, max: 33
      },
      {
        cssVar: ['progress-radius', 'px'],
        label: 'progress-radius',
        type: 'range', value: 20, min: 0, max: 33
      },
      {
        cssVar: ['progress-color'], // alias for the CSS variable
        label: 'progress-color',
        type: 'color',
        value: '#EEEEEE'
      },
      {
        cssVar: ['fill-color'], // alias for the CSS variable
        label: 'fill-color',
        type: 'color',
        value: '#0366D6'
      },
      "Ticks",
      {
        cssVar: ['show-min-max'],
        label: 'hide min/max',
        type: 'checkbox',
        value: 'none'
      },
      {
        cssVar: ['ticks-thickness', 'px'],
        label: 'ticks-thickness',
        type: 'range',
        value: 1, min: 0, max: 10
      },
      {
        cssVar: ['ticks-height', 'px'],
        label: 'ticks-height',
        type: 'range',
        value: 5, min: 0, max: 15
      },
      {
        cssVar: ['ticks-gap', 'px'],
        label: 'ticks-gap',
        type: 'range',
        value: 5, min: 0, max: 15
      },
      {
        cssVar: ['min-max-x-offset', '%'],
        label: 'min-max-x-offset',
        type: 'range',
        value: 10, step: 1, min: 0, max: 100
      },
      {
        cssVar: ['min-max-opacity'],
        label: 'min-max-opacity',
        type: 'range', value: .5, step: .1, min: 0, max: 1
      },
      {
        cssVar: ['ticks-color'], // alias for the CSS variable
        label: 'ticks-color',
        type: 'color',
        value: '#AAAAAA'
      },
    ]
  }
  
  new Knobs(settings)
})