(function () {
    
    var setup_checkbox_list = function(field_id) {
        var $field_label
          , $field_list;
        
        $field_label = $('#' + field_id + ' label');
        $field_list = $('#' + field_id + ' ul');
        
        $field_list.hide();
        $field_label.click(function() {
            $field_list.slideToggle();
        });
    };
    
    var init = function() {
        setup_checkbox_list('div_id_statuses');
        setup_checkbox_list('div_id_controlling_bodies');
        setup_checkbox_list('div_id_file_types');
        setup_checkbox_list('div_id_sponsors');
    };
    
    init();
})();

