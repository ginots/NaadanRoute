// 1. Capture the unit prices (per 1 person) from the data attributes
const baseSubtotal = parseFloat(document.getElementById("subtotal").getAttribute('data-base'));
const baseDiscount = parseFloat(document.getElementById("discount").getAttribute('data-base'));
const baseTotal = parseFloat(document.getElementById("total").getAttribute('data-base'));

function changeQuantity(delta) {
    const quantityInput = document.getElementById('quantity');
    let currentQuantity = parseInt(quantityInput.value);

    // Calculate new quantity
    let newQuantity = Math.max(1, Math.min(70, currentQuantity + delta));

    // Update input field
    quantityInput.value = newQuantity;

    // Update the bill
    updateOrderSummary(newQuantity);

    // Animation logic
    if (window.event && window.event.target) {
        const btn = window.event.target;
        btn.classList.add('pulse');
        setTimeout(() => btn.classList.remove('pulse'), 300);
    }
}

function updateOrderSummary(quantity) {
    // Calculate new values
    const newSubtotal = baseSubtotal * quantity;
    const newDiscount = baseDiscount * quantity;
    const newTotal = baseTotal * quantity;

    // Update the text in the UI
    // .toFixed(2) ensures it looks like currency (e.g., 100.00)
    document.getElementById('subtotal').textContent = newSubtotal.toFixed(2);
    document.getElementById('discount').textContent = newDiscount.toFixed(2);
    document.getElementById('total').textContent = newTotal.toFixed(2);

}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateOrderSummary(1);
});

        // Product image rotation
        function rotateImage() {
            const image = document.querySelector('.product-image');
            image.style.transform = 'scale(1.05) rotate(5deg)';
            setTimeout(() => {
                image.style.transform = 'scale(1) rotate(0deg)';
            }, 200);
        }




        $(document).ready(function(){
    $(".property-slider").owlCarousel({
      items: 1,           // Show 1 slide at a time
      loop: true,          // Infinite loop
      autoplay: true,      // Slide automatically
      autoplayTimeout: 3000,
      nav: true,           // Show arrows
      dots: true,          // Show navigation dots
      navText: ["<span class='fa fa-chevron-left'></span>", "<span class='fa fa-chevron-right'></span>"]
    });
  });