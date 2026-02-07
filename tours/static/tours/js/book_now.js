$(document).ready(function() {
    flatpickr("#datePicker", {
        minDate: new Date().fp_incr(1),

        // USER sees (High-end format)
        altInput: true,
        altFormat: "F j, Y",

        //  DATABASE sees (Correct format)
        dateFormat: "Y-m-d",

        disableMobile: true,
        static: true,

        onReady: function(selectedDates, dateStr, instance) {
            instance.altInput.classList.add("form-control");
        }
    });
});