$(document).ready(function() {
  $("#add_gasto").modalForm({
    formURL: "/gastos/adicionar"
  });
})


$(document).ready(function() {
  $(".delete_gasto").each(function () {
    $(this).modalForm({formURL: $(this).data('id')});
  })
  var has_at_least_one_category_limit = false

  $(".category_limit").each(function() {
    if ($(this).val().length > 0){
      has_at_least_one_category_limit = true
    }}
  );
  if ($("#value_limit_global").text() > 0) {
    $(".limite_categoria").show()
  }


  if (has_at_least_one_category_limit == true){
    $(".limites_categorias").show();
    $("hr").show();
    $(".limite_categoria").show()
    $("#limite_categoria").prop('checked', true);
    $("#value_limit_available").text()
    calculate_available_limit_for_categories();
  }

})

$(function(){
  $("#limite_categoria").click(function () {
    if ($(this).is(":checked")) {
      $(".limites_categorias").show();
      $("hr").show();
      $('#save_button').attr("disabled", true);
      $('#save_button').css('background-color', 'grey');
      calculate_available_limit_for_categories()
    } else {
      $(".limites_categorias").hide();
      $('#save_button').attr("disabled", false);
      $('#save_button').css('background-color', '#4d0270');
      $("hr").hide();
    }
  });
});

$(function(){
  var total = 0;

  $(".total_field").each(function() {
    total += parseInt($( this ).text());
  });
   $( "#total" ).text(total);
  
});


function calculate_table_limits(){

  var id_category_table = $('.id_category_table').attr("data-id");
  var id_total_category = $('.total_field').attr("data-id");

  var categories_ids = []
  $('.category_limit_id').each(function () {
    categories_ids.push($(this).data('id'))
  })

  var limit_globe = $('#limit_globe').text();
  var total_field = $('#total').text();

  var result_global_limit =  limit_globe - total_field;
  
  if (limit_globe == "None"){
    $('#limit_globe').css('color', 'black');
    $('#limit_globe').html("Não definido")

  } else {
    $('#limit_globe').html(result_global_limit.toFixed(2));
  }
  
  categories_ids.forEach((id_category_table) => {

  var value_category_limit = $('#value_category_limit_' + id_category_table).text()
  

  // Colors of Global Limit

  if (result_global_limit < 0) {
    $('#limit_globe').css('color', 'red')
  }
  if (result_global_limit == 0) {
    $('#limit_globe').css('color', 'black')
  }
  if ((result_global_limit > 0) && (result_global_limit < 0.33 * limit_globe)) {
    $('#limit_globe').css('color', 'orange')
  }
  if ((result_global_limit >= 0.33 * limit_globe) && (result_global_limit < 0.66 * limit_globe)) {
    $('#limit_globe').css('color', '#d1cc2a')
  }
  if (result_global_limit >= 0.66 * limit_globe) {
    $('#limit_globe').css('color', '#85bb65')
  }

  
    var result_category_limit = value_category_limit;
    $('.total_field[data-id="' + id_category_table + '"]').each( function () {
      
      result_category_limit -= $(this).text();
    })
    if (result_category_limit == NaN) {
      result_category_limit = 0
      $('#value_category_limit_' + id_category_table).html(result_category_limit)
    } else {
      $('#value_category_limit_' + id_category_table).html(result_category_limit)
    }
    
    // Colors of Categories Limits
    if (result_category_limit == 'None'){
      $('#value_category_limit_' + id_category_table).css('color', 'black')
      $('#value_category_limit_' + id_category_table).html("<h6> Não definido! </h6>")
    }
    if (result_category_limit < 0) {
      $('#value_category_limit_' + id_category_table).css('color', 'red')
    }
    if (result_category_limit == 0) {
      $('#value_category_limit_' + id_category_table).css('color', 'black')
    }
    if ((result_category_limit > 0) && (result_category_limit < 0.33 * value_category_limit)) {
      $('#value_category_limit_' + id_category_table).css('color', 'orange')
    }
    if ((result_category_limit >= 0.33 * value_category_limit) && (result_category_limit < 0.66 * value_category_limit)) {
      $('#value_category_limit_' + id_category_table).css('color', '#d1cc2a')
    }
    if (result_category_limit >= 0.66 * value_category_limit) {
      $('#value_category_limit_' + id_category_table).css('color', '#85bb65')
    }
  });
}
$(function(){calculate_table_limits()});


$(function() {

  $(".js-range-slider-1").ionRangeSlider({

    type: "single",
    skin: "round",
    min: 0,
    step: 50,
    max: 10000,
    from: $('#value_limit_global').text(),
    grid: true,
    prefix: "R$",
    onFinish: function(data) {
      $('.limit_global').show()
      $(".limite_categoria").show()
      $('#value_limit_global').html(data.from);
      $('#value_limit_available').html(data.from);
    }
  });




  $(".category_limit").keyup(function () {
    calculate_available_limit_for_categories()
  });


$("#save_button").click(function (event) { 
  event.preventDefault();
  $.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    } 
  });

   var value_global_limit = $('#value_limit_global').html()
   var id_category_limit = $('.category_limit').attr("data-id")

   var limit_by_category_id = {}
   $(".category_limit").each(function() {
    var id = $(this).data('id');
    limit_by_category_id[parseInt(id)] = parseInt($(this).val())
   });

   
  $.ajax({
    type: "POST",
    url: "salvar-limite/",
    dataType: 'json',
    data: {
      value_global_limit: value_global_limit,
      limit_by_category_id: JSON.stringify(limit_by_category_id)
    },
    success: function (data, textStatus, jqXHR) {
      console.log(data, textStatus, jqXHR);
    },
    complete: function (data, textStatus, jqXHR) {
      if (data.status == 200) {
        $('#successModal').modal();
      }
    }
  })
});

$(function() {
  $("#filter_month").change(function (){
    var selected_month = parseInt($(this).val())
    var selected_year = parseInt($("#filter_year").val())
    var selected_category = parseInt($("#filter_category").val())
    $.ajax({
      type: "GET",
      url: "/select_month_year_and_category/",
      dataType: 'html',
      data: {
        selected_month: selected_month,
        selected_year: selected_year,
        selected_category: selected_category
      },
      success: function(data) {
        $("tbody").empty();
        $("#gasto_table").hide()
        $("#update_table_gasto").html(data)
        calculate_table_limits()
        
      }
    })
  })
})
$(function() {
  $("#filter_year").change(function (){
    var selected_month = parseInt($("#filter_month").val())
    var selected_year = parseInt($(this).val())
    var selected_category = parseInt($("#filter_category").val())
    $.ajax({
      type: "GET",
      url: "/select_month_year_and_category/",
      dataType: 'html',
      data: {
        selected_month: selected_month,
        selected_year: selected_year,
        selected_category: selected_category
      },
      success: function(data) {
        $("tbody").empty();
        $("#gasto_table").hide()
        $("#update_table_gasto").html(data)
        calculate_table_limits()
      }
    })
  })
})

$(function() {
  $("#filter_category").change(function (){
    var selected_month = parseInt($("#filter_month").val())
    var selected_year = parseInt($("#filter_year").val())
    var selected_category = parseInt($(this).val())
    $.ajax({
      type: "GET",
      url: "/select_month_year_and_category/",
      dataType: 'html',
      data: {
        selected_month: selected_month,
        selected_year: selected_year,
        selected_category: selected_category
      },
      success: function(data) {
        $("tbody").empty();
        $("#gasto_table").hide()
        $("#update_table_gasto").html(data)
        
      }
    })
  })
})

})
function calculate_available_limit_for_categories() {
  var used_limit = 0;
  $(".category_limit").each(function() {
    value = 0  
    if ($(this).val() != "") {
      value = parseInt($(this).val())
    } 
    
    used_limit += value;
    })
    var max_limit = parseInt($('#value_limit_global').html())
    var available_limit = max_limit - used_limit
    $('#value_limit_available').html(available_limit.toFixed(2));
    if (available_limit < 0){
      $('#value_limit_available').css("color", "red")
    } 
    if (available_limit == 0){
      $('#value_limit_available').css("color", "black")
      $('#save_button').attr("disabled", false);
      $('#save_button').css('background-color', '#4d0270');
    } else {
      $('#save_button').attr("disabled", true);
      $('#save_button').css('background-color', 'gray');
    }
    if ((available_limit > 0) && (available_limit < 0.33 * max_limit)) {
      $('#value_limit_available').css("color", "orange")
    }
    if ((available_limit >= 0.33 * max_limit) && (available_limit < 0.66 * max_limit)) {
      $('#value_limit_available').css("color", "#d1cc2a")
    } 
    if (available_limit >= 0.66 * max_limit) {
      $('#value_limit_available').css("color", "#85bb65")
    }
}


