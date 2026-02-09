/**
 * Calendar and Booking System
 * Handles appointment booking for formations and livrables
 */

document.addEventListener('DOMContentLoaded', function() {
    const bookingModal = document.getElementById('booking-modal');
    const bookingBtns = document.querySelectorAll('.book-appointment-btn');
    const closeModalBtn = document.querySelector('.close-modal');
    const dateInput = document.getElementById('id_appointment_date');
    const timeInput = document.getElementById('id_appointment_time');
    const timeSlotsContainer = document.getElementById('time-slots-container');
    const selectedTimeDisplay = document.getElementById('selected-time-display');

    let currentAppointmentType = null;

    // Open booking modal
    bookingBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            currentAppointmentType = this.dataset.type || getAppointmentTypeFromPage();
            if (bookingModal) {
                bookingModal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            }
        });
    });

    // Close modal
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function() {
            bookingModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });
    }

    // Close modal when clicking outside
    if (bookingModal) {
        bookingModal.addEventListener('click', function(e) {
            if (e.target === bookingModal) {
                bookingModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }

    // Handle date selection
    if (dateInput) {
        dateInput.addEventListener('change', function() {
            const selectedDate = this.value;
            if (selectedDate) {
                fetchAvailableSlots(selectedDate, currentAppointmentType);
            }
        });

        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);

        // Set maximum date to 3 months from now
        const maxDate = new Date();
        maxDate.setMonth(maxDate.getMonth() + 3);
        dateInput.setAttribute('max', maxDate.toISOString().split('T')[0]);
    }

    /**
     * Fetch available time slots for a given date and type
     */
    function fetchAvailableSlots(date, type) {
        if (!timeSlotsContainer) return;

        // Show loading state
        timeSlotsContainer.innerHTML = '<p class="loading-text">Chargement des créneaux disponibles...</p>';

        // Build API URL
        const url = `/api/available-slots/?date=${date}&type=${type}`;

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'Erreur lors du chargement des créneaux');
                    });
                }
                return response.json();
            })
            .then(data => {
                displayTimeSlots(data.available_slots);
            })
            .catch(error => {
                console.error('Error fetching slots:', error);
                timeSlotsContainer.innerHTML = `<p class="error-text">${error.message}</p>`;
            });
    }

    /**
     * Display available time slots
     */
    function displayTimeSlots(slots) {
        if (!timeSlotsContainer) return;

        if (slots.length === 0) {
            timeSlotsContainer.innerHTML = '<p class="no-slots-text">Aucun créneau disponible pour cette date. Veuillez choisir une autre date.</p>';
            return;
        }

        timeSlotsContainer.innerHTML = '<h4>Créneaux disponibles:</h4><div class="time-slots-grid"></div>';
        const grid = timeSlotsContainer.querySelector('.time-slots-grid');

        slots.forEach(slot => {
            const slotBtn = document.createElement('button');
            slotBtn.type = 'button';
            slotBtn.className = 'time-slot-btn';
            slotBtn.textContent = slot.display;
            slotBtn.dataset.time = slot.time;

            slotBtn.addEventListener('click', function() {
                // Remove active class from all slots
                document.querySelectorAll('.time-slot-btn').forEach(btn => {
                    btn.classList.remove('active');
                });

                // Add active class to selected slot
                this.classList.add('active');

                // Set the time input value
                if (timeInput) {
                    timeInput.value = slot.time;
                }

                // Update display
                if (selectedTimeDisplay) {
                    selectedTimeDisplay.textContent = `Heure sélectionnée: ${slot.display}`;
                    selectedTimeDisplay.style.display = 'block';
                }
            });

            grid.appendChild(slotBtn);
        });
    }

    /**
     * Get appointment type from current page URL
     */
    function getAppointmentTypeFromPage() {
        const path = window.location.pathname;
        if (path.includes('formation')) {
            return 'formation';
        } else if (path.includes('livrables')) {
            return 'livrables';
        }
        return 'formation'; // default
    }

    /**
     * Disable weekends in date picker
     */
    if (dateInput) {
        dateInput.addEventListener('input', function() {
            const selectedDate = new Date(this.value);
            const dayOfWeek = selectedDate.getDay();

            // If Saturday (6) or Sunday (0), clear the input
            if (dayOfWeek === 0 || dayOfWeek === 6) {
                this.value = '';
                alert('Les rendez-vous ne sont disponibles que du lundi au vendredi.');
            }
        });
    }

    // Auto-open modal if there are form errors
    const formErrors = document.querySelector('.booking-form .errorlist, .booking-form .error-text');
    if (formErrors && bookingModal) {
        bookingModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        currentAppointmentType = getAppointmentTypeFromPage();
    }
});
