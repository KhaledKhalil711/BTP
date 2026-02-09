# Booking System Implementation Guide

## Overview

A complete booking/appointment system has been implemented for both **Formations** and **Livrables** pages, allowing users to schedule consultations without conflicts.

---

## 🎯 Features Implemented

### 1. **Appointment Booking System**
- ✅ Separate calendars for Formations and Livrables (no conflicts)
- ✅ Monday to Friday only (9:00 - 16:00)
- ✅ 1-hour appointment slots
- ✅ Real-time availability checking via API
- ✅ Interactive time slot selection
- ✅ Email and phone contact collection
- ✅ Admin dashboard for managing appointments

### 2. **Comprehensive Content**
#### Formation Page:
- 4 training programs (Beginner, Intermediate, Advanced, Specialization)
- Detailed course features and pricing
- "Why choose us" section
- Professional hero section with CTA
- Booking modal integrated

#### Livrables Page:
- 4 consulting services (Project Study, Plans & Metrics, Project Management, Technical Assistance)
- Deliverables documentation section
- Work process timeline
- Benefits section
- Booking modal integrated

---

## 📁 Files Created/Modified

### **New Files:**
1. `core/static/core/js/calendar.js` - Calendar and booking JavaScript
2. `BOOKING_SYSTEM_GUIDE.md` - This documentation

### **Modified Files:**
1. `core/models.py` - Added `Appointment` model
2. `core/forms.py` - Added `AppointmentForm`
3. `core/views.py` - Added booking logic and API endpoint
4. `core/urls.py` - Added API route
5. `core/admin.py` - Added Appointment admin interface
6. `core/templates/core/formation.html` - Complete redesign with booking
7. `core/templates/core/livrables.html` - Complete redesign with booking
8. `core/static/core/css/style.css` - Added 500+ lines of styling
9. `core/migrations/0002_*.py` - Database migration for Appointment model

---

## 🗓️ How the Booking System Works

### User Flow:
1. **User clicks "Réserver un rendez-vous" button**
2. **Modal opens with booking form**
3. **User selects a date** (Monday-Friday only)
4. **System fetches available time slots** via API
5. **User clicks on an available time slot**
6. **User fills in contact details and notes**
7. **User submits the form**
8. **Appointment is saved to database**
9. **Success message displayed**

### Technical Flow:
```
User selects date
    ↓
JavaScript: calendar.js
    ↓
Fetch API: /api/available-slots/?date=YYYY-MM-DD&type=formation|livrables
    ↓
Django View: get_available_slots()
    ↓
Query Database: Check booked appointments
    ↓
Return: Available time slots (9:00-16:00, excluding booked)
    ↓
JavaScript: Display time slots
    ↓
User selects time & submits
    ↓
Django View: formation() or livrables()
    ↓
Validate & Save Appointment
    ↓
Redirect with success message
```

---

## 🔧 Database Schema

### **Appointment Model**
```python
{
    'user': ForeignKey(User) # Optional - if user is logged in
    'name': CharField(100)
    'email': EmailField()
    'phone': CharField(20)
    'appointment_type': 'formation' | 'livrables'
    'appointment_date': DateField()
    'appointment_time': TimeField()
    'duration_hours': IntegerField(default=1)
    'subject': CharField(200)
    'notes': TextField()
    'status': 'pending' | 'confirmed' | 'cancelled' | 'completed'
    'created_at': DateTimeField(auto_now_add=True)
    'updated_at': DateTimeField(auto_now=True)
}
```

**Unique Constraint:** (`appointment_type`, `appointment_date`, `appointment_time`)
- Ensures no double-booking for the same time slot and type

---

## 🎨 New UI Components

### 1. **Hero Section**
- Gradient background
- Call-to-action button
- Professional header for each page

### 2. **Formation/Service Cards**
- 4-column responsive grid
- Hover animations
- Ribbons for featured items
- Price tags
- Feature lists
- Action buttons

### 3. **Booking Modal**
- Centered overlay
- Smooth animations
- Responsive design
- Form validation
- Time slots grid
- Close button

### 4. **Time Slots Display**
- Grid layout
- Interactive buttons
- Active state indication
- Loading and error states
- Real-time availability

### 5. **Features Grid**
- Icon-based features
- Hover effects
- Responsive 4-column layout

### 6. **Process Timeline**
- 4-step process
- Numbered steps
- Clear progression

---

## 🔐 API Endpoint

### **GET /api/available-slots/**

**Query Parameters:**
- `date` (required): YYYY-MM-DD format
- `type` (required): "formation" or "livrables"

**Response:**
```json
{
    "date": "2026-02-15",
    "type": "formation",
    "available_slots": [
        {
            "time": "09:00",
            "display": "9:00 - 10:00"
        },
        {
            "time": "10:00",
            "display": "10:00 - 11:00"
        },
        ...
    ]
}
```

**Error Response:**
```json
{
    "error": "Les rendez-vous ne sont disponibles que du lundi au vendredi."
}
```

---

## 👨‍💼 Admin Interface

Access at: `/admin/core/appointment/`

**Features:**
- List view with filters (type, status, date)
- Search by name, email, phone, subject
- Date hierarchy navigation
- Bulk actions
- Detailed appointment view with:
  - Client information
  - Appointment details
  - Status management
  - Creation/update timestamps

**List Filters:**
- Appointment Type (formation/livrables)
- Status (pending/confirmed/cancelled/completed)
- Date
- Creation date

---

## 📱 Responsive Design

### Breakpoints:
- **Desktop:** Full grid layout (4 columns)
- **Tablet (768px):** 2 columns, stacked form rows
- **Mobile (480px):** Single column, compact buttons

### Mobile Optimizations:
- Touch-friendly time slot buttons
- Full-width modal
- Simplified navigation
- Adjusted font sizes

---

## 🎯 Key Features

### 1. **No Conflicts**
- Formation and livrables appointments are tracked separately
- Unique constraint prevents double-booking
- Real-time availability checking

### 2. **Business Hours Validation**
- Monday-Friday only
- 9:00 AM to 4:00 PM (last slot at 3:00 PM)
- Weekend dates automatically rejected
- Past dates cannot be selected

### 3. **User-Friendly**
- Visual time slot selection (no manual time entry)
- Inline form validation
- Success/error messages
- Auto-open modal on form errors

### 4. **Flexible**
- Works for both authenticated and anonymous users
- Optional phone number
- Custom notes/subject for each appointment

---

## 🧪 Testing the System

### Test Scenarios:

1. **Book a Formation Appointment:**
   - Navigate to `/formation/`
   - Click "Réserver un rendez-vous"
   - Select a future weekday date
   - Click on an available time slot
   - Fill in contact details
   - Submit

2. **Book a Livrables Appointment:**
   - Navigate to `/livrables/`
   - Click "Prendre rendez-vous"
   - Select same date as formation
   - Verify different availability (no conflicts)
   - Complete booking

3. **Test Conflict Prevention:**
   - Book a formation appointment for Monday 10:00
   - Try to book another formation for Monday 10:00
   - Verify that 10:00 slot is no longer available
   - Verify that livrables Monday 10:00 is still available

4. **Test Validation:**
   - Try selecting a Saturday (should be blocked)
   - Try selecting a past date (should be blocked)
   - Try submitting without required fields (should show errors)

---

## 🚀 Usage Instructions

### For Users:
1. Visit Formation or Livrables page
2. Click any "Réserver" button
3. Select date from calendar
4. Click available time slot
5. Fill contact information
6. Submit booking

### For Admins:
1. Login to `/admin/`
2. Navigate to Core → Rendez-vous
3. View all appointments
4. Filter by type, status, date
5. Update appointment status
6. Confirm or cancel appointments

---

## 💡 Future Enhancements (Optional)

1. **Email Notifications:**
   - Send confirmation emails to users
   - Send reminders 24h before appointment
   - Notify admin of new bookings

2. **Calendar Integration:**
   - iCal export
   - Google Calendar sync

3. **Payment Integration:**
   - Online payment for formations
   - Deposit system

4. **User Dashboard:**
   - View my appointments
   - Reschedule appointments
   - Cancel appointments

5. **Multi-day Appointments:**
   - Support for longer consultations
   - Recurring appointments

---

## 📊 Statistics

### Lines of Code Added:
- **Python:** ~250 lines (models, forms, views, admin)
- **JavaScript:** ~180 lines (calendar.js)
- **CSS:** ~600 lines (styling)
- **HTML:** ~600 lines (templates)
- **Total:** ~1,630 lines

### Components Created:
- 1 Model (Appointment)
- 1 Form (AppointmentForm)
- 3 Views (formation, livrables, get_available_slots)
- 1 API Endpoint
- 2 Complete Pages
- 1 Modal Component
- 10+ CSS Components

---

## ✅ Checklist

- ✅ Appointment model created with validation
- ✅ Booking forms implemented
- ✅ Calendar JavaScript with time slot selection
- ✅ API endpoint for availability checking
- ✅ Formation page filled with content
- ✅ Livrables page filled with content
- ✅ Responsive design implemented
- ✅ Admin interface configured
- ✅ Migrations applied
- ✅ No conflicts between formation/livrables bookings
- ✅ Business hours validation (Mon-Fri, 9-16)
- ✅ 1-hour appointment slots
- ✅ Professional styling and animations

---

## 🎓 Training Content Summary

### Formation Page (4 Programs):
1. **Fondamentaux du BTP** - 1,500€ - 2 weeks (70h)
2. **Perfectionnement BTP** - 2,500€ - 4 weeks (140h)
3. **Chef de Chantier** - 4,000€ - 6 weeks (210h)
4. **Spécialisation Technique** - 1,800€ - 3 weeks (105h)

### Livrables Page (4 Services):
1. **Étude de Projet** - Sur devis - Feasibility analysis
2. **Plans & Métrés** - From 800€ - Technical drawings
3. **Gestion de Projet** - Sur mesure - Project management
4. **Assistance Technique** - 150€/hour - Technical support

---

## 📞 Support

For questions about the booking system:
1. Check this documentation
2. Review the code comments in:
   - `core/models.py`
   - `core/views.py`
   - `core/static/core/js/calendar.js`
3. Test the admin interface at `/admin/`

---

**Implementation Date:** 2026-02-09
**Django Version:** 4.2.28
**Status:** ✅ Fully Functional
