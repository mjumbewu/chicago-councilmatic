"use strict"

var searchUI = {
    /**
     * Create all the menu labels
     */
    initFullSearchMenus : function () {
        var i, label, widget;
        var labels = $('label');
        
        for (i in labels) {
            label = labels[i];
            widget = $(label).next();
            if (widget.length > 0 && widget[0].localName === 'ul') {
                widget = widget[0];
                
                $(widget).slideUp();
                searchUI.setFullSearchMenuLabelClickHandler(label, widget);
            }
        }
    },
    
    /**
     * Set the menu show/hide functionality when clicking on a menu label
     */
    setFullSearchMenuLabelClickHandler : function (label, list) {
        $(label).click(function () {
            $(list).slideToggle();
        });
    }
}

$(document).ready(function () {
//    searchUI.initFullSearchMenus();
});
