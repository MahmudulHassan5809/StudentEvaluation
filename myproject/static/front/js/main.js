jQuery(document).ready(function($) {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });


   if ($("#last").length == 1){
        console.log('a');
        $('#view_answer').css("display", "block");
   }

});
