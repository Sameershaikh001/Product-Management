document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        let productId = this.dataset.id;
        let newPrice = prompt("Enter new price:");
        if (newPrice) {
            fetch(`/update_price/${productId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ price: newPrice })
            }).then(response => location.reload());
        }
    });
});
