function hideAllContents(){
    var elements = document.getElementsByClassName('content');
    for(var i = 0, length = elements.length; i < length; i++) {
        elements[i].style.display = 'none';
    }
}

function bodyLoad(){
    // hide nav on document ready
    document.getElementById('nav').style.display = 'none';
    hideAllContents();
}

function navClick(){
    // scroll up when nav is clicked and hide all contents
    document.getElementById('nav').style.display = 'none';
    hideAllContents();
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

function contentCheck(id){
    // A single method to show element "content_" + button pressed id
    if (document.getElementById('content_' + id).style.display === 'none'){
        document.getElementById('content_' + id).style.display = 'block';
        document.getElementById('nav').style.display = 'block';
    } else {
        document.getElementById('content_' + id).style.display = 'none';
        var visibleBoxes = 0;
        // if all content class divs are hidden, hide nav
        var elements = document.getElementsByClassName('content');
        for(var i = 0, length = elements.length; i < length; i++) {
            if (elements[i].style.display !== 'none'){
                visibleBoxes += 1;
            }
        }
        if (visibleBoxes == 0){
            document.getElementById('nav').style.display = 'none';
        }
    }
}
