async function loadInventory() {

    try {

        const response =
            await fetch(
                `${API_URL}/reports/inventory`,
                {
                    headers: getHeaders()
                }
            );


        const data =
            await response.json();


        if (!response.ok) {
            throw new Error("Failed to load inventory report");
        }

        const table = document.getElementById("inventoryTableBody");


        table.innerHTML = "";


        data.report.forEach(
            product => {

                const row =
                    document.createElement(
                        "tr"
                    );


                row.innerHTML = `

                    <td>
                        ${product.product_id}
                    </td>

                    <td>
                        ${product.product_name}
                    </td>

                    <td>
                        ${product.available_stock}
                    </td>

                    <td>
                        ${product.reserved_stock}
                    </td>

                `;


                table.appendChild(row);

            }
        );

    }
    catch (error) {

        console.error(error);

    }
}


async function loadCustomers() {

    try {

        const response =
            await fetch(
                `${API_URL}/reports/customers`,
                {
                    headers: getHeaders()
                }
            );


        const data =
            await response.json();


        if (!response.ok) {
            throw new Error("Failed to load customer report");
        }

        const table = document.getElementById("customersTableBody");


        table.innerHTML = "";


        data.report.forEach(
            customer => {

                const row =
                    document.createElement(
                        "tr"
                    );


                row.innerHTML = `

                    <td>
                        ${customer.customer_id}
                    </td>

                    <td>
                        ${customer.customer_name}
                    </td>

                    <td>
                        ${customer.email}
                    </td>

                    <td>
                        ${customer.total_orders}
                    </td>

                    <td>
                        ₹${customer.total_amount}
                    </td>

                `;


                table.appendChild(row);

            }
        );

    }
    catch (error) {

        console.error(error);

    }
}


loadInventory();
loadCustomers();