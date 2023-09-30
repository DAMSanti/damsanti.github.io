const toggleButton = document.getElementById('toggle-button');
const sidebar = document.getElementById('sidebar');

toggleButton.addEventListener('click', () => {
    // Toggle the aside by changing its right position
    sidebar.style.right = sidebar.style.right === '0px' ? '-300px' : '0px';
});