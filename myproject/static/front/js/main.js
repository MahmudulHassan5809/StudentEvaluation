jQuery(document).ready(function($) {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });


    if ($("#last").length == 1){
        console.log('a');
        $('#view_answer').css("display", "block");
    }

    if ($('#teacher_courses_count_dict').length != 0){
        var teacher_courses_count_dict = JSON.parse($('#teacher_courses_count_dict').text());

        var labels = [];
        var data = [];
        for(key in teacher_courses_count_dict) {
            labels.push(teacher_courses_count_dict[key].s_name);
            data.push(teacher_courses_count_dict[key].c_count);
        }

        console.log(labels)

        new Chart(document.getElementById("bar-chart"), {
            type: 'bar',
            data: {
              labels: labels,
              datasets: [
              {

                barThickness: 20,
                  label: "Course Per Semester",
                  backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
                  data: data
              }
              ]
          },
          options: {
                legend: { display: false },
                  title: {
                    display: true,
                    text: 'Course Per Semester'
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        });
    }







    if ($('#student_courses_count_dict').length != 0){
        var student_courses_count_dict = JSON.parse($('#student_courses_count_dict').text());

        var labels = [];
        var data = [];
        for(key in student_courses_count_dict) {
            labels.push(student_courses_count_dict[key].s_name);
            data.push(student_courses_count_dict[key].c_count);
        }

        console.log(labels,data)

        new Chart(document.getElementById("student-bar-chart"), {
            type: 'bar',
            data: {
              labels: labels,
              datasets: [
              {

                barThickness: 20,
                  label: "Course Per Semester",
                  backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
                  data: data
              }
              ]
          },
          options: {
                legend: { display: false },
                  title: {
                    display: true,
                    text: 'Course Per Semester'
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }

    $(".cool-b4-form .form-control").on("input", function() {
      if ($(this).val()) {
        $(this).addClass("hasValue");
      } else {
        $(this).removeClass("hasValue");
      }
  });


});
