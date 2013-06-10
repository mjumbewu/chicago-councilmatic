(function ($) {

    var init = function() {
        $('.bookmark.active button').tooltip({
            title: 'Click to unsubscribe',
            placement:'bottom'});
        $('.bookmark.inactive button').tooltip({
            title: 'Click to subscribe',
            placement:'bottom'});
        $('.bookmark.inactive.unauthenticated button').tooltip({
            title: 'Login to subscribe',
            placement:'bottom'});
    };

    $(function() {
        init();
    });
    
})(jQuery);
