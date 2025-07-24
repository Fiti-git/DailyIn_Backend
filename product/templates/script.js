const API_URL = "http://127.0.0.1:8000/api/products/";

// Fetch products and display
async function fetchProducts() {
    try {
        const response = await axios.get(API_URL);
        const products = response.data;
        const productList = document.getElementById("product-list");

        productList.innerHTML = ""; // Clear previous content

        products.forEach(product => {
            const div = document.createElement("div");
            div.classList.add("product-item");
            div.innerHTML = `
                <p><strong>Itcode:</strong> ${product.Itcode}</p>
                <p><strong>Name:</strong> ${product.ItDesc}</p>
                <p><strong>Rack No:</strong> ${product.RackNo}</p>
                <p><strong>Barcode:</strong> ${product.barcode}</p>
            `;
            productList.appendChild(div);
        });
    } catch (error) {
        console.error("Error fetching products:", error);
    }
}

// Add a new product
async function addProduct(event) {
    event.preventDefault();

    const Itcode = document.getElementById("Itcode").value;
    const ItDesc = document.getElementById("ItDesc").value;
    const RackNo = document.getElementById("RackNo").value;
    const barcode = document.getElementById("barcode").value;

    const newProduct = { Itcode, ItDesc, RackNo, barcode };

    try {
        const response = await axios.post(API_URL, newProduct);
        alert("Product Added Successfully!");
        fetchProducts();  // Refresh the product list
    } catch (error) {
        console.error("Error adding product:", error);
    }
}

// Search for a product
async function searchProduct() {
    const searchQuery = document.getElementById("search").value;
    try {
        const response = await axios.get(`${API_URL}?search=${searchQuery}`);
        const products = response.data;
        const productList = document.getElementById("product-list");

        productList.innerHTML = ""; // Clear previous content

        products.forEach(product => {
            const div = document.createElement("div");
            div.classList.add("product-item");
            div.innerHTML = `
                <p><strong>Itcode:</strong> ${product.Itcode}</p>
                <p><strong>Name:</strong> ${product.ItDesc}</p>
                <p><strong>Rack No:</strong> ${product.RackNo}</p>
                <p><strong>Barcode:</strong> ${product.barcode}</p>
            `;
            productList.appendChild(div);
        });
    } catch (error) {
        console.error("Error searching products:", error);
    }
}

// Initialize page
document.getElementById("product-form").addEventListener("submit", addProduct);
window.onload = fetchProducts;
