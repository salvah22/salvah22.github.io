let nav
function hideAllContents(){
    var elements = document.getElementsByClassName('content');
    for(e of elements) {
        e.style.display = 'none';
    }
}
function bodyLoad(){
    nav = document.getElementById('nav')
}
function navClick(){
    // hide all contents
    nav.style.display = 'none';
    hideAllContents();
    // scroll up 
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
function contentCheck(id){
    // A single method to show element "content_" + button pressed id
    const content = document.getElementById('content_' + id)
    if (content.style.display === 'none'){
        content.style.display = 'block';
        nav.style.display = 'block';
    } else {
        content.style.display = 'none';
        var visibleBoxes = 0;
        // if all content class divs are hidden, hide nav
        var elements = document.getElementsByClassName('content');
        for(e of elements) {
            if (e.style.display !== 'none'){
                visibleBoxes += 1;
            }
        }
        if (visibleBoxes == 0){
            nav.style.display = 'none';
        }
    }
}
function enlargeMe(img) {
  img.style.width = "700px";
}
function enlargeMe2(img) {
  img.style.height = "600px";
}
