function toggleCategoriesDropdown(event) {
    event.stopPropagation();
    const categoriesMenu = document.querySelector('.categories-menu');
    categoriesMenu.style.display = categoriesMenu.style.display === 'block' ? 'none' : 'block';
    closeOtherDropdowns('categories');
}

function toggleProfileDropdown(event) {
    event.stopPropagation();
    const dropdown = document.querySelector('.dropdown');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    closeOtherDropdowns('profile');
}

function toggleNotificationsDropdown(event) {
    event.stopPropagation();
    const notificationsMenu = document.querySelector('.notifications-menu');
    notificationsMenu.style.display = notificationsMenu.style.display === 'block' ? 'none' : 'block';
    closeOtherDropdowns('notifications');
}

function closeOtherDropdowns(exclude) {
    if (exclude !== 'profile') {
        const profileDropdown = document.querySelector('.dropdown');
        if (profileDropdown) profileDropdown.style.display = 'none';
    }

    if (exclude !== 'notifications') {
        const notificationsMenu = document.querySelector('.notifications-menu');
        if (notificationsMenu) notificationsMenu.style.display = 'none';
    }

    if (exclude !== 'categories') {
        const categoriesMenu = document.querySelector('.categories-menu');
        if (categoriesMenu) categoriesMenu.style.display = 'none';
    }
}

document.addEventListener('click', function () {
    closeOtherDropdowns();
});
