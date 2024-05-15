function toggleDropdown(data) {
    var content = document.getElementById('content-' + data);
    if (content.style.display === 'none' || !content.style.display) {
        content.style.display = 'block';
    } else {
        content.style.display = 'none';
    }
}