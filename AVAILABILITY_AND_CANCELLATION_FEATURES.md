# Availability Checking & Appointment Cancellation Features

## ✅ Implementation Complete

Both availability checking and appointment cancellation have been successfully implemented.

---

## 🔍 Feature 1: Availability Checking

### What It Does
- **Validates appointment slots** before booking
- **Checks for conflicts** with existing appointments
- **Validates date/time** (no past dates, valid time format)
- **Suggests alternatives** if slot is unavailable
- **Prevents double bookings**

### Implementation Details

**File Created:** `database/availability.py`

**Key Functions:**
- `check_doctor_availability()` - Check if doctor is available at given date/time
- `get_available_slots()` - Get list of available time slots for a doctor
- `suggest_alternative_slots()` - Suggest alternative times if preferred slot is taken
- `validate_appointment_slot()` - Comprehensive validation with suggestions

### How It Works

1. **Before Booking:**
   - Checks if slot is already booked
   - Validates date is not in the past
   - Validates time format
   - Returns availability status

2. **If Slot Unavailable:**
   - Provides reason (e.g., "Slot already booked")
   - Suggests alternative time slots
   - Shows available times for the same date

3. **Integration:**
   - Automatically called in `process_appointment_booking()`
   - Replaces simple duplicate check
   - Provides better error messages

### Example Flow

```
User: "Book appointment with Dr. John Smith tomorrow at 10:00"
Bot: 
  ✅ Checks availability
  ✅ Slot available → Books appointment
  OR
  ❌ Slot taken → "Slot already booked. Available alternatives: 10:30, 11:00, 11:30"
```

---

## 🗑️ Feature 2: Appointment Cancellation

### What It Does
- **Cancel appointments** via chat or API
- **Find appointments** by ID or patient name
- **Update appointment status** to 'cancelled'
- **Provide confirmation** with appointment details

### Implementation Details

**API Endpoint:** `POST /api/cancel`

**Intent:** `cancel_appointment` (added to intent classifier)

**Chat Handler:** `handle_appointment_cancellation()` function

### How It Works

1. **Via Chat:**
   - User says: "Cancel my appointment"
   - Bot extracts appointment ID or patient name
   - Provides instructions or processes cancellation

2. **Via API:**
   - Send POST request to `/api/cancel`
   - Provide `appointment_id` OR `patient_name`
   - Returns cancellation confirmation

3. **Database Update:**
   - Sets appointment status to 'cancelled'
   - Preserves appointment record for history
   - Only cancels 'scheduled' or 'confirmed' appointments

### Example Queries

**Chat Interface:**
```
User: "Cancel my appointment"
Bot: "To cancel your appointment, please provide your appointment ID or name..."

User: "Cancel appointment ID 123"
Bot: "I can help you cancel appointment #123. Please confirm..."
```

**API Usage:**
```bash
# Cancel by appointment ID
curl -X POST http://localhost:8000/api/cancel \
  -H "Content-Type: application/json" \
  -d '{"appointment_id": 123}'

# Cancel by patient name
curl -X POST http://localhost:8000/api/cancel \
  -H "Content-Type: application/json" \
  -d '{"patient_name": "John Smith"}'
```

### Response Format

**Success:**
```json
{
  "status": "success",
  "message": "Appointment cancelled successfully",
  "appointment_details": {
    "id": 123,
    "doctor": "Dr. John Smith",
    "date": "2026-02-01",
    "time": "10:00"
  }
}
```

**Error:**
```json
{
  "status": "error",
  "message": "No active appointment found..."
}
```

---

## 🔧 Technical Details

### Files Created/Modified

1. **`database/availability.py`** (NEW)
   - `AvailabilityChecker` class
   - Availability validation logic
   - Alternative slot suggestions

2. **`app.py`** (MODIFIED)
   - Integrated `AvailabilityChecker`
   - Added `/api/cancel` endpoint
   - Added `handle_appointment_cancellation()` function
   - Updated `process_appointment_booking()` to use availability checking

3. **`ai/intent_model.py`** (MODIFIED)
   - Added `cancel_appointment` intent
   - Added cancellation detection patterns

### Database Schema

**Appointments Table:**
- `status` field supports: 'scheduled', 'confirmed', 'cancelled'
- Cancelled appointments are preserved for history

---

## 🎯 Usage Examples

### Availability Checking

**Example 1: Slot Available**
```
User: "Book appointment with Dr. John Smith tomorrow at 10:00"
Bot: ✅ "Appointment booked successfully!"
```

**Example 2: Slot Unavailable**
```
User: "Book appointment with Dr. John Smith tomorrow at 10:00"
Bot: ⚠️ "Slot already booked for Dr. John Smith on 2026-02-15 at 10:00.
     Available alternative times: 10:30, 11:00, 11:30"
```

**Example 3: Past Date**
```
User: "Book appointment yesterday at 10:00"
Bot: ⚠️ "Cannot book appointments in the past"
```

### Appointment Cancellation

**Example 1: Cancel by ID**
```
User: "Cancel appointment ID 123"
Bot: "I can help you cancel appointment #123..."
```

**Example 2: Cancel My Appointment**
```
User: "Cancel my appointment"
Bot: "To cancel your appointment, please provide your appointment ID..."
```

**Example 3: API Call**
```python
import requests

response = requests.post('http://localhost:8000/api/cancel', json={
    'appointment_id': 123
})
print(response.json())
```

---

## 🚀 Benefits

### Availability Checking
- ✅ Prevents double bookings
- ✅ Better user experience with alternative suggestions
- ✅ Validates dates/times before booking
- ✅ Reduces booking errors

### Appointment Cancellation
- ✅ Complete appointment lifecycle management
- ✅ User-friendly cancellation process
- ✅ Preserves appointment history
- ✅ API endpoint for programmatic access

---

## 📝 Next Steps (Optional Enhancements)

1. **Cancellation Confirmation** - Send email/SMS when appointment is cancelled
2. **Reschedule Feature** - Allow users to reschedule instead of just cancel
3. **Cancellation Window** - Prevent cancellation too close to appointment time
4. **Bulk Availability** - Show all available slots for a date
5. **Recurring Appointments** - Handle recurring appointment availability

---

## 🧪 Testing

### Test Availability Checking
1. Book an appointment
2. Try to book the same slot again → Should show unavailable
3. Try to book in the past → Should show error
4. Try invalid time → Should show error

### Test Cancellation
1. Book an appointment (note the ID)
2. Cancel via chat: "Cancel appointment ID [ID]"
3. Cancel via API: `POST /api/cancel` with appointment_id
4. Try to cancel non-existent appointment → Should show error

Both features are now fully functional! 🎉

