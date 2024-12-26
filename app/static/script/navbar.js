// Toggle Categories Dropdown
function toggleCategoriesDropdown(event) {
    event.stopPropagation(); // Prevent click from bubbling up to the document
    const categoriesMenu = document.querySelector('.categories-menu');
    categoriesMenu.classList.toggle('show'); // Toggle 'show' class to display menu
    closeOtherDropdowns('categories'); // Close other dropdowns
}

// Toggle Profile Dropdown
function toggleProfileDropdown(event) {
    event.stopPropagation(); // Prevent click from bubbling up to the document
    const profileMenu = document.querySelector('.dropdown');
    profileMenu.classList.toggle('show'); // Toggle 'show' class to display menu
    closeOtherDropdowns('profile'); // Close other dropdowns
}

// Toggle Notifications Dropdown
function toggleNotificationsDropdown(event) {
    event.stopPropagation(); // Prevent click from bubbling up to the document
    const notificationsMenu = document.querySelector('.notifications-menu');
    notificationsMenu.classList.toggle('show'); // Toggle 'show' class to display menu
    closeOtherDropdowns('notifications'); // Close other dropdowns
}

// Close all dropdowns except the one that is clicked
function closeOtherDropdowns(exclude) {
    if (exclude !== 'profile') {
        const profileDropdown = document.querySelector('.dropdown');
        if (profileDropdown) profileDropdown.classList.remove('show');
    }

    if (exclude !== 'notifications') {
        const notificationsMenu = document.querySelector('.notifications-menu');
        if (notificationsMenu) notificationsMenu.classList.remove('show');
    }

    if (exclude !== 'categories') {
        const categoriesMenu = document.querySelector('.categories-menu');
        if (categoriesMenu) categoriesMenu.classList.remove('show');
    }
}

// Close all dropdowns when clicking outside of any dropdown
document.addEventListener('click', function () {
    closeOtherDropdowns();
});

// Prevent closing dropdown when clicking inside any dropdown
document.querySelectorAll('.categories-menu, .notifications-menu, .dropdown').forEach(function(dropdown) {
    dropdown.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent click inside dropdown from closing it
    });
});