
        let products = {
            men: [],
            women: [],
            kids: []
        };

        function addProduct(category) {
            const nameInput = document.getElementById(`${category}-product-name`);
            const amountInput = document.getElementById(`${category}-product-amount`);
            const imageInput = document.getElementById(`${category}-product-image`);

            const productName = nameInput.value;
            const productAmount = amountInput.value;
            const productImage = imageInput.files[0]; // File input, requires server-side handling for image storage

            if (productName && productAmount && productImage) {
                const product = {
                    name: productName,
                    amount: productAmount,
                    image: productImage.name
                };

                products[category].push(product);
                displayProducts(category);

                // Clear the form inputs
                nameInput.value = '';
                amountInput.value = '';
                imageInput.value = '';
            }
        }

        function displayProducts(category) {
            const productTable = document.getElementById(`${category}-product-list`);

            // Clear existing rows
            while (productTable.firstChild) {
                productTable.removeChild(productTable.firstChild);
            }

            products[category].forEach(product => {
                const row = productTable.insertRow();
                row.innerHTML = `
                    <td>${product.name}</td>
                    <td>${product.amount}</td>
                    <td>${product.image}</td>
                    <td>
                        <button onclick="editProduct('${category}', ${products[category].indexOf(product)})">Edit</button>
                        <button onclick="removeProduct('${category}', ${products[category].indexOf(product)})">Remove</button>
                    </td>
                `;
            });
        }

        function editProduct(category, index) {
            // Implement edit functionality
        }

        function removeProduct(category, index) {
            products[category].splice(index, 1);
            displayProducts(category);
        }

        // Event listeners for category links
        document.getElementById('men-link').addEventListener('click', () => {
            document.querySelector('.product-form').style.display = 'none';
            document.querySelector('.product-list').style.display = 'none';
            document.getElementById('men-form').style.display = 'block';
            document.getElementById('men-list').style.display = 'block';
            displayProducts('men');
        });

        document.getElementById('women-link').addEventListener('click', () => {
            document.querySelector('.product-form').style.display = 'none';
            document.querySelector('.product-list').style.display = 'none';
            document.getElementById('women-form').style.display = 'block';
            document.getElementById('women-list').style.display = 'block';
            displayProducts('women');
        });

        document.getElementById('kids-link').addEventListener('click', () => {
            document.querySelector('.product-form').style.display = 'none';
            document.querySelector('.product-list').style.display = 'none';
            document.getElementById('kids-form').style.display = 'block';
            document.getElementById('kids-list').style.display = 'block';
            displayProducts('kids');
        });
    