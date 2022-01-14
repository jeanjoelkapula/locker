
jQuery( document ).ready(function() {
		
    //get settings
    settings = window.themeSettings.settings;

    //get theme primary color
    primary = settings.theme.colors.primary;

    //set root color elements

    var styleElem = document.head.appendChild(document.createElement("style"));

    styleElem.innerHTML = `:root { --primary: ${primary}; }`;

})