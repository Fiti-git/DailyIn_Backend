const API_URL_PRODUCTS = "http://127.0.0.1:8000/api/products/";
const API_URL_OUTLETS = "http://127.0.0.1:8000/api/outlets/";
const API_URL_STOCK = "http://127.0.0.1:8000/api/stock/";

// Fetch products and populate the select dropdown
async function fetchProducts() {
    try {
        const response = await axios.get(API_URL_PRODUCTS);
        const products = response.data;
        const productSelect = document.getElementById("product-select");

        productSelect.innerHTML = "<option value=''>Select Product</option>"; // Clear existing options

        products.forEach(product => {
            const option = document.createElement("option");
            option.value = product.id;
            option.textContent = `${product.ItDesc} (${product.Itcode})`;
            productSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Error fetching products:", error);
    }
}

// Fetch outlets and populate the select dropdown
async function fetchOutlets() {
    try {
        const response = await axios.get(API_URL_OUTLETS);
        const outlets = response.data;
        const outletSelect = document.getElementById("outlet-select");

        outletSelect.innerHTML = "<option value=''>Select Outlet</option>"; // Clear existing options

        outlets.forEach(outlet => {
            const option = document.createElement("option");
            option.value = outlet.id;
            option.textContent = outlet.outletName;
            outletSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Error fetching outlets:", error);
    }
}

// Fetch all stock data
async function fetchStock() {
    try {
        const response = await axios.get(API_URL_STOCK);
        const stock = response.data;
        const stockList = document.getElementById("stock-list");

        stockList.innerHTML = ""; // Clear previous content

        stock.forEach(stockItem => {
            const div = document.createElement("div");
            div.classList.add("stock-item");
            div.innerHTML = `
                <p><strong>Product:</strong> ${stockItem.product.ItDesc}</p>
                <p><strong>Outlet:</strong> ${stockItem.outlet.outletName}</p>
                <p><strong>Quantity:</strong> ${stockItem.quantity}</p>
            `;
            stockList.appendChild(div);
        });
    } catch (error) {
        console.error("Error fetching stock:", error);
    }
}

// Add new stock entry
async function addStock(event) {
    event.preventDefault();

    const productId = document.getElementById("product-select").value;
    const outletId = document.getElementById("outlet-select").value;
    const quantity = document.getElementById("quantity").value;

    const newStock = { product: productId, outlet: outletId, quantity };

    try {
        const response = await axios.post(API_URL_STOCK, newStock);
        alert("Stock Added Successfully!");
        fetchStock();  // Refresh the stock list
    } catch (error) {
        console.error("Error adding stock:", error);
    }
}

// Search stock
async function searchStock() {
    const searchQuery = document.getElementById("search-stock").value;

    try {
        const response = await axios.get(`${API_URL_STOCK}?search=${searchQuery}`);
        const stock = response.data;
        const stockList = document.getElementById("stock-list");

        stockList.innerHTML = ""; // Clear previous content

        stock.forEach(stockItem => {
            const div = document.createElement("div");
            div.classList.add("stock-item");
            div.innerHTML = `
                <p><strong>Product:</strong> ${stockItem.product.ItDesc}</p>
                <p><strong>Outlet:</strong> ${stockItem.outlet.outletName}</p>
                <p><strong>Quantity:</strong> ${stockItem.quantity}</p>
            `;
            stockList.appendChild(div);
        });
    } catch (error) {
        console.error("Error searching stock:", error);
    }
}

// Initialize page
document.getElementById("stock-form").addEventListener("submit", addStock);
window.onload = function() {
    fetchProducts();
    fetchOutlets();
    fetchStock();
};
