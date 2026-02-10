document.addEventListener('DOMContentLoaded', function() {
    // --- Filter buttons for appointment list ---
    const filterBtns = document.querySelectorAll('.filter-btn');
    const tableRows = document.querySelectorAll('.appointments-table tbody tr');
    const cards = document.querySelectorAll('.appointment-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Update active state
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            const filter = this.dataset.filter;

            // Filter table rows (desktop)
            tableRows.forEach(row => {
                if (!row.dataset.type) return; // Skip empty state rows
                if (filter === 'all') {
                    row.style.display = '';
                } else if (['formation', 'livrables'].includes(filter)) {
                    row.style.display = row.dataset.type === filter ? '' : 'none';
                } else {
                    row.style.display = row.dataset.status === filter ? '' : 'none';
                }
            });

            // Filter cards (mobile)
            cards.forEach(card => {
                if (filter === 'all') {
                    card.style.display = '';
                } else if (['formation', 'livrables'].includes(filter)) {
                    card.style.display = card.dataset.type === filter ? '' : 'none';
                } else {
                    card.style.display = card.dataset.status === filter ? '' : 'none';
                }
            });
        });
    });

    // --- Confirm before status change ---
    const statusSelects = document.querySelectorAll('.status-select');
    statusSelects.forEach(select => {
        select.addEventListener('change', function(e) {
            if (!this.value) return;

            const statusLabels = {
                'confirmed': 'confirmer',
                'cancelled': 'annuler',
                'completed': 'terminer'
            };
            const label = statusLabels[this.value] || this.value;

            if (confirm('Voulez-vous vraiment ' + label + ' ce rendez-vous ?')) {
                this.closest('form').submit();
            } else {
                this.value = '';
            }
        });
    });

    // --- Auto-dismiss success/error messages after 5 seconds ---
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});
