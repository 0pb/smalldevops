
/*
*   file.js  - Used for the website in the SmallDevops module
*   Author   - 0pb
*   Link     - https://github.com/0pb/smalldevops
*   LICENSE GNU V3
*/


$(document).ready(function() {
  // load toggle trigger
  load_toggling_button(data);
  load_arrow_function(data);

  // load the data and display it once the page is loaded
  current_js_file(data);

  // load the data with a set interval if the toggle is on
  refreshing_data(data);
});


function load_toggling_button(data) {
  // hide the list of errors messages
  $('.collapser2').on("click", function() {$('#test_fail').toggle("slow");});

  // hide the color grid of errors class
  $('.collapser3').on("click", function() {$('#small_color_error').toggle("slow");});

  // expand the graph on the left, put the data information at the bottom of the page
  actually_showing = false;
  $('.collapser4').on("click", function() {
    right_column_class = document.getElementById("right_column").classList;
    left_column_class = document.getElementById("left_column").classList;
    if (actually_showing) {
      actually_showing = false;
      left_column_class.add('col-xl-6');
      left_column_class.remove('col-xl-12');

      right_column_class.remove('col-xl-12');
      right_column_class.add('col-xl-6');
    }
    else {
      actually_showing = true;
      left_column_class.remove('col-xl-6');
      left_column_class.add('col-xl-12');

      right_column_class.add('col-xl-12');
      right_column_class.remove('col-xl-6');
    }
  });
}


function load_arrow_function(data) {
  function navigate_in_index_with_arrow(event, data) {
    let i = parseInt(document.getElementById('current_index').textContent, 10);
    let increment = 1;
    switch (event.keyCode) 
    {   
      case 37:
        if (i - increment < 0) {i = 0;}
        else {i = i - increment;}
        break;
      case 39:
        if (i + increment >= data.length) {i = i;}
        else {i = i + increment;}
        break;
    }
    modify_card_dom(data[i], i);
  };

  document.onkeydown = function() {
    switch (event.keyCode) 
    {   
      case 37:
        event.preventDefault();
        navigate_in_index_with_arrow(event, data);
        break;
      case 39:         
        event.preventDefault();
        navigate_in_index_with_arrow(event, data);
        break;
    }
  };
}


function current_js_file(data) {
  // get the latest point in the json file
  let current_data = data[data.length - 1];
  let current_index = data.length - 1;

  // load the entire data in the graphs in the left column
  process_data_and_graph(data);
  // add the last data information in the right column
  modify_card_dom(current_data, current_index);
}


function refreshing_data(data) {
  let auto_refresher;
  let interval_value_ms = 5000;
  let true_if_auto_refresh = false;
  // allow auto-refreshing of the data, with a jsonp call of the output.js file
  $('#toggling_auto_refresh').on("click", function() {
    current_button = document.getElementById("toggling_auto_refresh").classList;
    true_if_auto_refresh = !true_if_auto_refresh;
    if (true_if_auto_refresh) {
      current_button.remove('btn-outline-light');
      current_button.add('btn-light');
      auto_refresher = auto_refresh(interval_value_ms);
    }
    else {
      current_button.add('btn-outline-light');
      current_button.remove('btn-light');
      clearInterval(auto_refresher);
    }
  });

  // set the refresh value of the data, ie entering 3 mean an interval of 3s
  $('#button_auto_refresh').on("click", function() {
    if (true_if_auto_refresh) {
      let nameValue = document.getElementById("auto_refresh_value").value;
      if (nameValue && !isNaN(nameValue)) {
        interval_value_ms = nameValue * 1000;
        clearInterval(auto_refresher);
        auto_refresher = auto_refresh(interval_value_ms);
      }
    }
  });
}


function auto_refresh(actual_value) {
  /* 
  use ajax and jsonp in order to ignore content policy, it request the output.js file
  and return a response OK if found. If the file was found then the global "data" value 
  is refreshed.
  */

  // load once before the auto refresh, can act as a button to refresh the data only
  current_js_file(data);

  // update the latest data value from the output.js file in the current folder
  auto_refresher = setInterval(function() {
    $.ajax({
      url: 'output.js',
      dataType: 'JSONP',
      jsonpCallback: 'callbackFnc',
      type: 'GET',
      async: false,
      crossDomain: true,
      success: function (response) { },
      failure: function (response) { },
      complete: function (response) { }
    });
    current_js_file(data);
  }, actual_value);
  return auto_refresher;
}


function process_data_and_graph(data) {
  // id of the two graph, in the future a new graph will simply require to add
  // a new id and manage the new addition in the list
  line_chart_amount = "line_chart_amount";
  line_chart_timing = "line_chart_timing";

  // get the time of the data for the x axis for both graph
  // get amount of failed and success test in 2 lists for the dataset for the first graph
  // get timing test and timing of program in 2 lists for the dataset of the second graph
  var date_axis = [];
  var list_amount_fail = [];
  var list_amount_success = [];
  var list_timing_test = [];
  var list_timing_software = [];
  for (let i=0; i<data.length; i++) 
  {
    current_data = data[i];
    date = luxon.DateTime.fromFormat(current_data["date"], "y-M-d-H-m-s");
    dateobject = date.toObject();
    new_date = new Date(dateobject.year
                      , dateobject.month
                      , dateobject.day
                      , dateobject.hour
                      , dateobject.minute
                      , dateobject.second);
    date_axis.push(new_date);
    list_amount_fail.push(current_data["failed_amount"]);
    list_amount_success.push(current_data["success_amount"]);

    list_timing_test.push(current_data["timing_test"]);
    real_timing = current_data["timing_function"];
    list_timing_software.push(real_timing);
  }  
  label_for_amount = ["amount of test", "amount of fail test", "amount of successful test"];
  label_for_timing = ["timing", "seconds (tests)", "seconds (program)"];

  var chart_amount = chartjs(data
          , line_chart_amount
          , date_axis
          , list_amount_fail
          , list_amount_success
          , label_for_amount);
  var chart_timing = chartjs(data
          , line_chart_timing
          , date_axis
          , list_timing_test
          , list_timing_software
          , label_for_timing);

  // on mouse click get the current data, then display it on the right column
  document.getElementById(line_chart_amount).onclick = function() { get_current_data(event, chart_amount, data); };
  document.getElementById(line_chart_timing).onclick = function() { get_current_data(event, chart_timing, data); };
}


function chartjs(json_data, current_id, x_axis, y1_axis, y2_axis, labelling) {
  // use chartjs to create a graph
  var chart = new Chart(document.getElementById(current_id), {
    type: 'line',
    data: {
      labels: x_axis,
      datasets: 
      [{ 
        data: y1_axis,
        label: labelling[1],
        borderColor: "#00FFFF",
        fill: false
      },
      { 
        data: y2_axis,
        label: labelling[2],
        borderColor: "#3e95cd",
        fill: false
      }]
    },
    options: {
      elements: {
        point:{
          radius: 2}
      },
      animation: {
        duration: 0
      },
      title: {
        display: true,
        text: labelling[0]
      }, 
      scales: {
        xAxes: 
        [{
          ticks: {
            // display a smaller date on the x axis, if the callback isn't specified then
            // the complete date is shown (Wen 20 april 2020 00:00:00 +2Gtm etc.) which make
            // the axis unreadable
            callback: function(value) { 
              return new Date(value).toLocaleDateString('fr-FR'
                          , {month:'short', day:'numeric', hour:'numeric', minute:'numeric'}); 
                          // , {month:'short', year:'numeric'}); 
            }
          }
        }]
      }
    }
  });
  return chart;
}


function get_current_data(evt, current_chart, data) {
  // bisect function
  try {
    var activePoints = current_chart.getElementsAtEvent(evt);
    current_data_for_click = data[activePoints[0]["_index"]];
    modify_card_dom(current_data_for_click, activePoints[0]["_index"]);
  } catch (TypeError) {/* didn't click on a point in the graph */}
};


function display_error_grid(current_data) {
  var dict_of_fail_class_test = {};

  for (const [key, value] of Object.entries(current_data["success_test"])) {
      dict_of_fail_class_test[value.split(" ")[1]] = false;
  }

  for (const [key, value] of Object.entries(current_data["failed_test"])) {
      dict_of_fail_class_test[key.split(" ")[1]] = true;
  }

  $("#small_color_error").empty();
  for (const [key, value] of Object.entries(dict_of_fail_class_test)) {
    if (value) {
      text_to_add = '<div class="col border bg-danger text-white">' + key + '</div>';
      $("#small_color_error").append(text_to_add);
    }
    else {
      text_to_add = '<div class="col border bg-success text-white">' + key + '</div>';
      $("#small_color_error").append(text_to_add);
    }
  }
}

function modify_card_dom(current_data, current_index) {
  display_error_grid(current_data);

  // list message errors
  $("#test_fail").empty();
  var final_big = [];
  for (const [key, value] of Object.entries(current_data["failed_test"])) {
      var final_string = value;
      final_big.push('<li class="text-dark bg-light list-group-item"><pre><p class="mb-0">' 
                    + final_string.join('</p><p class="mb-0">') + '</p></pre></li>');
  }
  $("#test_fail").append(final_big);

  // display in the right column every informations of the current data selected by the user
  data_commit = current_data["commit"];
  total_amount = current_data["total_amount"];
  percent_amount = Math.round((1 - current_data["failed_amount"]/total_amount) * 100);
  $("#amount_test_total").text("Total test : " + total_amount);
  $("#commit_author").text(data_commit[1]);
  $("#commit_msg").text(data_commit[2]);
  $("#commit_hash").text(data_commit[0]);
  $("#commit_date").text(current_data["date"]);
  $("#current_index").text(current_index);

  $("#amount_failed").text(current_data["failed_amount"]);
  $("#pass_percent").text(percent_amount + "%");
  $("#timing_prog").text(current_data["timing_function"] + "s");

  // change the color of the right column, red for error, blue for failure and green for 100% pass
  special_card_class_list = document.getElementById("special_card").classList;
  if (current_data["error_unittest"]) {
    special_card_class_list.remove('bg-info');
    special_card_class_list.remove('bg-success');
    special_card_class_list.add('bg-danger');
  }
  else {
    special_card_class_list.remove('bg-danger');
    special_card_class_list.remove('bg-success');
    special_card_class_list.add('bg-info');
  }
  if (current_data["failed_amount"] === 0) {
    special_card_class_list.remove('bg-danger');
    special_card_class_list.remove('bg-info');
    special_card_class_list.add('bg-success');
  }
  return [current_data, current_index];
}