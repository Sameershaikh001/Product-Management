function searchProduct() {
    let input = document.getElementById("searchBox").value.toLowerCase();
    let rows = document.querySelectorAll("#productTable tr");

    rows.forEach(row => {
        let productName = row.querySelector(".product-name").innerText.toLowerCase();
        if (productName.includes(input)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}
function confirmDelete(productId) {
    let confirmation = confirm("Are you sure you want to delete this product?");
    if (confirmation) {
        window.location.href = `/delete/${productId}`;
    }
}
