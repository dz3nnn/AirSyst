$(document).ready(function ($) {
  $.cookie.raw = true;
  $.cookie.json = true;


  if ($.cookie("shopping-cart")) {
    $('.shopping-cart').attr('attr-count', Object.keys(JSON.parse($.cookie("shopping-cart"))).length);
  } else {
    $('.shopping-cart').attr('attr-count', 0);
  }

  $('.to-shopping-cart').on('click', function (e) {
    e.preventDefault();
    if ($.cookie('shopping-cart')) {
      let k = 0;
      let basketItems = $.makeArray(JSON.parse($.cookie('shopping-cart')));
      let basketItem = { id: $(this).closest('.catalog__item').attr('product-id'), count: $(this).siblings('.catalog__count').find('input').val() };
      for (let i = 0; i < basketItems.length; i++) {
        if (basketItems[i].id == $(this).closest('.catalog__item').attr('product-id')) {
          basketItems[i].count = (parseFloat(basketItems[i].count) + parseFloat($(this).siblings('.catalog__count').find('input').val()));
          k++;
        }
      } if (k == 0) {
        basketItems.push(basketItem);
        $('.shopping-cart').attr('attr-count', parseInt($('.shopping-cart').attr('attr-count')) + 1);
      }
      $.cookie('shopping-cart', basketItems, { path: '/', expires: 7 });
    } else {
      let basketItem = { id: $(this).closest('.catalog__item').attr('product-id'), count: $(this).siblings('.catalog__count').find('input').val() };
      let basketItems = [];
      basketItems.push(basketItem);
      $('.shopping-cart').attr('attr-count', parseInt($('.shopping-cart').attr('attr-count')) + 1);
      $.cookie('shopping-cart', basketItems, { path: '/', expires: 7 });
    }
  });

  $('.shop-cart__delete').on('click', function () {
    let basketItems = $.makeArray(JSON.parse($.cookie('shopping-cart')));
    let newBasketItems = [];
    for (let i = 0; i < basketItems.length; i++) {
      if (basketItems[i].id != $(this).closest('.shop-cart__item').attr('product-id')) {
        newBasketItems.push(basketItems[i]);
      }
    }
    $('.shopping-cart').attr('attr-count', parseInt($('.shopping-cart').attr('attr-count')) - 1);
    $.cookie('shopping-cart', newBasketItems, { path: '/', expires: 7 });
    location.reload();
  });

  $('.shop-cart__delete-all').on('click', function () {
    $('.shop-cart__item .filter__checkbox.active').each(function () {
      let basketItems = $.makeArray(JSON.parse($.cookie('shopping-cart')));
      let newBasketItems = [];
      for (let i = 0; i < basketItems.length; i++) {
        if (basketItems[i].id != $(this).closest('.shop-cart__item').attr('product-id')) {
          newBasketItems.push(basketItems[i]);
        }
      }
      $('.shopping-cart').attr('attr-count', parseInt($('.shopping-cart').attr('attr-count')) - 1);
      $.cookie('shopping-cart', newBasketItems, { path: '/', expires: 7 });
    });
    location.reload();
  });

  $('.filter__checkbox[name="select-all"]').on('click', function () {
    if ($(this).hasClass('active')) {
      $('.shop-cart__items .filter__checkbox').removeClass('active');
    } else {
      $('.shop-cart__items .filter__checkbox').addClass('active');
    }
  });

  var search = window.location.search.split('?')[1];
  if (search) {
    var arrFiltred = search.replace('/', '').split('&');
    for (let i = 0; i < arrFiltred.length; i++) {
      let optionId = arrFiltred[i].split('=')[0];
      let paramIdArr = arrFiltred[i].split('=')[1].split(':');
      if ($('[option-id="' + optionId + '"]').hasClass('filter__checkboxs')) {
        for (let j = 0; j < paramIdArr.length; j++) {
          $('[option-id="' + optionId + '"]').find('[option-value-id="' + paramIdArr[j] + '"]').addClass('active');
        }
      } else {
        $('[option-id="' + optionId + '"]').find('[name="min"]').val(paramIdArr[0]);
        $('[option-id="' + optionId + '"]').find('[name="max"]').val(paramIdArr[1]);
      }
    }
  }

  $('.filter .filter__checkbox').on('click', function () {
    $('.filter-apply').addClass('active');
  });

  $('.filter__inputs input').on('change', function () {
    $('.filter-apply').addClass('active');
    let pattern = new RegExp(/^[0-9]*[.,]?[0-9]+$/)
    if (pattern.test($(this).val()) == false) {
      $(this).val($(this).attr('valide-value'));
    }
    if ($(this).attr('name') == 'min') {
      if (parseFloat($(this).val()) < parseFloat($(this).attr('valide-value'))) {
        $(this).val(parseFloat($(this).attr('valide-value')));
      } else if (parseFloat($(this).val()) > parseFloat($(this).siblings().attr('valide-value'))) {
        $(this).val(parseFloat($(this).attr('valide-value')));
      }
    } else {
      if (parseFloat($(this).val()) > parseFloat($(this).attr('valide-value'))) {
        $(this).val(parseFloat($(this).attr('valide-value')));
      } else if (parseFloat($(this).val()) < parseFloat($(this).siblings().attr('valide-value'))) {
        $(this).val(parseFloat($(this).attr('valide-value')));
      }

    }
  });

  $('.filter-apply').on('click', function () {
    let filterLink = window.location.pathname + '?';
    $('[option-id]').each(function () {
      if ($(this).hasClass('filter__checkboxs') && $(this).children().hasClass('active')) {
        filterLink += $(this).attr('option-id') + '='
        $(this).find('.active').each(function () {
          filterLink += $(this).attr('option-value-id') + ':';
        })
        filterLink = filterLink.slice(0, -1);
        filterLink += '&';
      } else
        if ($(this).hasClass('filter__range') && $(this).find('input').val() != '') {
          filterLink += $(this).attr('option-id') + '=' + $(this).find('[name="min"]').val() + ':' + $(this).find('[name="max"]').val() + '&';
        }
    });
    filterLink = filterLink.slice(0, -1);
    console.log(filterLink);
    document.location.href = filterLink
  });

  if ($('.catalog .filter').length != 0) {
    $(document).on('scroll', function () {
      if ((($('.filter').offset().top + $('.filter').height()) - (window.innerHeight + window.scrollY) + 70) < 0) {
        $('.filter-apply').addClass('posAbs');
      } else {
        $('.filter-apply').removeClass('posAbs');
      }
    });
  }


  $('.armClockPage_block').css('filter', 'blur(0px)');

  $('.our-team__item').on('click', function () {
    $('.modal, .team-form').addClass('active');
  });

  $('.certificates__slide img, .reviews__slider img, .reviews-page__img, .card__slider-main img').on('click', function () {
    if ($(this).hasClass('slider-img')) {
      $('.certificates-form').addClass('w55');
    }
    $('.certificates-form .form-img').attr('src', $(this).attr('src'));
    $('.modal, .certificates-form').addClass('active');
  });

  $('.modal .close').on('click', function () {
    $('.modal, .team-form, .certificates-form, .success').removeClass('active').removeClass('w55');
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

  $('.card__thumb').on('click', function () {
    $(this).addClass('active').siblings().removeClass('active');
    $('.card__item').removeClass('active').eq($(this).index()).addClass('active');
  });

  setTimeout(function () {
    $('.bid__item').each(function () {
      $(this).find('.bid__company').css('animation-duration', ($(this).find('.bid__company').width() / 100).toFixed(1) + 's');
    })
  }, 500);

  $('.bid__item').hover(function () {
    if ($(document).width() > 600) {
      $(this).find('.bid__company').css('animation-duration', ($(this).find('.bid__company').width() / 350).toFixed(1) + 's');
    }
  });

  $('.nav__open').on('click', function () {
    $(this).toggleClass('active');
    $('.nav-mobile').toggleClass('active');
  });

  $('.filter__title').on('click', function () {
    $(this).closest('.filter').toggleClass('active');
  });


  $('.filter__checkbox').on('click', function () {
    $(this).toggleClass('active');
  });

  $('.catalog__count .catalog__minus, .catalog__count .catalog__plus').on('click', function (e) {
    e.preventDefault();
    if ($(this).hasClass('catalog__minus')) {
      if ($(this).closest('.catalog__count').find('input').val() >= 2) {
        $(this).closest('.catalog__count').find('input').val((parseFloat($(this).closest('.catalog__count').find('input').val()) - 1));
      }
    } else {
      $(this).closest('.catalog__count').find('input').val((parseFloat($(this).closest('.catalog__count').find('input').val()) + 1));
    }
    console.log($(this).closest('.catalog__count').find('input').val());
    $(this).closest('.catalog__count').find('input').change();
  });

  $('.catalog__count input').on('click', function (e) {
    e.preventDefault();
  });

  $('.feedback form').on('submit', function (e) {
    e.preventDefault();
    let emptyInputCount = 0;
    $(this).find('input[type="text"]').each(function () {
      if ($(this).val() == '') {
        $(this).addClass('form-error');
        emptyInputCount++;
        let errorInput = $(this);
        setTimeout(function () {
          $(errorInput).removeClass('form-error');
        }, 1500);
      }
    });
    if ($(this).find('.feedback__check').hasClass('active')) {
      if (emptyInputCount == 0) {
        $.ajax({
          data: {
            name: $(this).find('input[name="name"]').val(),
            email: $(this).find('input[name="mail"]').val(),
            msg: $(this).find('textarea[name="message"]').val(),
            csrfmiddlewaretoken: $(this).find('input[name="csrfmiddlewaretoken"]').val()
          },
          method: 'post',
          url: "/send_feedback/",
          dataType: 'json',
          complete: function (response) {
            $('.modal').addClass('active');
            $('.success').addClass('active');
          }
        });
      }
    }
    else {
      $(this).find('span').addClass('form-error');
      $(this).find('.feedback__check').addClass('form-error');
      setTimeout(function () {
        $('.feedback form').find('span').removeClass('form-error');
        $('.feedback form').find('.feedback__check').removeClass('form-error');
      }, 1500);
    }
  });

  $('.order .btn').on('click', function () {
    let emptyInputCount = 0;
    $(this).closest('.order').find('input').each(function () {
      if ($(this).val() == '') {
        $(this).addClass('form-error');
        emptyInputCount++;
        let errorInput = $(this);
        setTimeout(function () {
          $(errorInput).removeClass('form-error');
        }, 1500);
      }
    });
    if ($.cookie("shopping-cart")) {
      if (emptyInputCount == 0) {
        $.ajax({
          data: {
            name: $(this).closest('.order').find('input[name="name"]').val(),
            phone: $(this).closest('.order').find('input[name="phone"]').val(),
            email: $(this).closest('.order').find('input[name="mail"]').val(),
            csrfmiddlewaretoken: $(this).closest('.order').find('input[name="csrfmiddlewaretoken"]').val()
          },
          method: 'post',
          url: "/send_basket/",
          dataType: 'json',
          complete: function (response) {
            $('.modal').addClass('active');
            $('.success').addClass('active');
            $.removeCookie('shopping-cart', { path: '/' });
            $('.shopping-cart').attr('attr-count', 0);
          }
        });
      }
    } else {
      $(this).addClass('form-error').html('Корзина пуста');
      setTimeout(function(){
        $('.order .btn').removeClass('form-error').html('Продолжить')
      },1500)
    }
  });


  $('.catalog__count input').change(function () {
    let pattern = new RegExp(/^[0-9]*[.,]?[0-9]+$/)
    if (pattern.test($(this).val()) == false) {
      $(this).val(1);
    }
    if (parseFloat($(this).val()) <= parseFloat(1)) {
      $(this).val(1);
    }
    /* $(this).closest('.product-card__calc').find('.product-card__total span').html((parseFloat($(this).val()) * parseFloat($(this).closest('.card__top__info, .product-card, .cart__item').find('.product-card__price span, .card__price span, .cart__price span').html())).toFixed(2));
    cartItemsCount = 0;
    cartItemsKg = 0;
    cartTotalPrice = 0;
    let basketItems = [];
    $('.cart__item').each(function (index) {
        if ($(this).find('.cart__price').text().includes('кг')) {
            cartItemsKg = (parseFloat(cartItemsKg) + parseFloat($(this).find('input').val())).toFixed(2);
        } else {
            cartItemsInt = (parseFloat(cartItemsKg) + parseFloat($(this).find('input').val())).toFixed(0);
        }
        cartItemsCount = cartItemsCount + 1;
        cartTotalPrice = (parseFloat(cartTotalPrice) + parseFloat($(this).find('.product-card__total span').html().trim())).toFixed(2);
        let basketItem = { id: $(this).find('.cart__delete').attr('prod_id'), count: $(this).find('input').val() };
        basketItems.push(basketItem);
        $.cookie('basket', basketItems, { path: '/', expires: 7 });
    });
  
  
  
    $('.cart__you-order-info').html(cartItemsCount + ' товар(а) / ' + cartItemsKg + ' кг / ' + cartItemsInt + ' шт');
    $('.cart__total span').html(cartTotalPrice); */
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
    }, breakpoints: {
      300: {
        slidesPerView: 1,
      },
      640: {
        slidesPerView: 3,
      }
    }
  });

  var projectSwiper = new Swiper(".project__slider", {
    slidesPerView: 2,
    spaceBetween: 100,
    slidesPerGroup: 1,
    loop: true,
    loopFillGroupWithBlank: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    }, breakpoints: {
      300: {
        slidesPerView: 1,
      },
      640: {
        slidesPerView: 3,
      }
    }
  });





  // range-slider
  /*   var settings = {
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
  
    new Knobs(settings) */
})