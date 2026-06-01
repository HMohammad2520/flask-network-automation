(function () {
    // Sidebar drawer functionality
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const sidebarDrawer = document.getElementById('sidebarDrawer');
    const openBtn = document.getElementById('openSidebarBtn');
    const closeBtn = document.getElementById('closeSidebarBtn');

    function openSidebar() {
        sidebarOverlay.classList.add('active');
        sidebarDrawer.classList.add('open');
        document.body.style.overflow = 'hidden'; // Prevent scrolling when sidebar is open
    }

    function closeSidebar() {
        sidebarOverlay.classList.remove('active');
        sidebarDrawer.classList.remove('open');
        document.body.style.overflow = ''; // Restore scrolling
    }

    if (openBtn) {
        openBtn.addEventListener('click', openSidebar);
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', closeSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function (e) {
            if (e.target === sidebarOverlay) {
                closeSidebar();
            }
        });
    }

    // Escape key to close sidebar
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && sidebarDrawer && sidebarDrawer.classList.contains('open')) {
            closeSidebar();
        }
    });

    // Newsletter subscription for drawer version
    const subscribeDrawerBtn = document.getElementById('subscribeDrawerBtn');
    if (subscribeDrawerBtn) {
        subscribeDrawerBtn.addEventListener('click', function () {
            const emailInput = document.getElementById('newsEmailDrawer');
            if (emailInput && emailInput.value.trim() !== '' && emailInput.value.includes('@')) {
                alert(`✨ Thanks for subscribing! (demo) We'll send updates to ${emailInput.value} – modern teal vibes only.`);
                emailInput.value = '';
                closeSidebar(); // Optional: close sidebar after subscription
            } else {
                alert('🌊 Please enter a valid email address to continue (demo interaction).');
            }
        });
    }
})();