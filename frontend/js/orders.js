function getHeaders() {

    const token = localStorage.getItem("access_token");

    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}


// ===============================
// LOAD ORDERS
// ===============================

async function loadOrders(filters = {}) {

    try {

        const query = new URLSearchParams();

        if (filters.status) {
            query.set("status", filters.status);
        }

        if (filters.source) {
            query.set("source", filters.source);
        }

        const queryString = query.toString();
        const ordersMessage = document.getElementById("ordersMessage");

        const response = await fetch(
            `${API_URL}/orders/${queryString ? `?${queryString}` : ""}`,
            {
                method: "GET",
                headers: getHeaders()
            }
        );

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to load orders");
        }

        const data = await response.json();

        console.log("Orders:", data);

        displayOrders(data.orders || data);
        if (ordersMessage) {
            ordersMessage.textContent = `${data.count ?? (data.orders || data).length} orders loaded`;
            ordersMessage.style.color = "green";
        }

    } catch (error) {

        console.error("Order loading error:", error);
        const ordersMessage = document.getElementById("ordersMessage");
        if (ordersMessage) {
            ordersMessage.textContent = error.message;
            ordersMessage.style.color = "red";
        }

    }
}


document
    .getElementById("orderFilterForm")
    ?.addEventListener("submit", function(event) {
        event.preventDefault();
        loadOrders({
            status: document.getElementById("statusFilter").value,
            source: document.getElementById("sourceFilter").value
        });
    });


document
    .getElementById("clearOrderFilters")
    ?.addEventListener("click", function() {
        document.getElementById("orderFilterForm").reset();
        loadOrders();
    });


document
    .getElementById("orderLookupForm")
    ?.addEventListener("submit", async function(event) {
        event.preventDefault();

        const result = document.getElementById("orderLookupResult");
        const orderId = document.getElementById("lookupOrderId").value;
        result.textContent = "Loading order...";

        try {
            const response = await fetch(
                `${API_URL}/orders/${encodeURIComponent(orderId)}`,
                { headers: getHeaders() }
            );
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Failed to find order");
            }

            result.textContent = Object.entries(data)
                .map(([key, value]) => `${key}: ${value}`)
                .join("\n");
        } catch (error) {
            result.textContent = error.message;
        }
    });


// ===============================
document
    .getElementById("retryLookupOrder")
    ?.addEventListener("click", function() {
        const orderIdInput = document.getElementById("lookupOrderId");

        if (!orderIdInput.reportValidity()) {
            return;
        }

        retryOrder(Number(orderIdInput.value));
    });


// DISPLAY ORDERS
// ===============================

function displayOrders(orders) {

    const tableBody =
        document.getElementById("ordersTableBody");

    if (!tableBody) {
        return;
    }

    tableBody.innerHTML = "";

    orders.forEach(order => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${order.order_id}</td>
            <td>${order.customer_id}</td>
            <td>${order.product_id}</td>
            <td>${order.quantity}</td>
            <td>${order.unit_price}</td>
            <td>${order.payment_status}</td>
            <td>${order.processing_status}</td>
            <td>${order.retry_count}</td>
            <td>${order.source}</td>
            <td>${order.order_time ? new Date(order.order_time).toLocaleString() : "-"}</td>
            <td>
                ${
                    order.processing_status === "FAILED"
                    ? `<button class="retry-btn" onclick="retryOrder(${order.order_id})">
                           Retry
                       </button>`
                    : "-"
                }
            </td>
        `;

        tableBody.appendChild(row);

    });
}


// ===============================
// PROCESS ORDER
// ===============================

document
    .getElementById("orderForm")
    ?.addEventListener("submit", async function(event) {

        event.preventDefault();

        const message =
            document.getElementById("orderMessage");

        const orderData = {

            order_id: Number(
                document.getElementById("order_id").value
            ),

            customer_id: Number(
                document.getElementById("customer_id").value
            ),

            product_id: Number(
                document.getElementById("product_id").value
            ),

            quantity: Number(
                document.getElementById("quantity").value
            ),

            unit_price: Number(
                document.getElementById("unit_price").value
            ),

            payment_status:
                document.getElementById("payment_status").value,

            source:
                document.getElementById("source").value
        };


        const orderTime =
            document.getElementById("order_time").value;

        if (orderTime) {
            orderData.order_time = orderTime;
        }


        console.log("Sending order:", orderData);


        try {

            const response = await fetch(
                `${API_URL}/orders/process`,
                {
                    method: "POST",
                    headers: getHeaders(),
                    body: JSON.stringify(orderData)
                }
            );


            const data = await response.json();

            console.log("Process response:", data);


            if (!response.ok) {

                throw new Error(
                    data.detail || "Order processing failed"
                );

            }


            message.textContent =
                `Order ${orderData.order_id} processed successfully`;

            message.style.color = "green";


            document
                .getElementById("orderForm")
                .reset();


            // Refresh dashboard data

            loadOrders();

            if (typeof loadSummary === "function") {
                loadSummary();
            }

            if (typeof loadInventory === "function") {
                loadInventory();
            }


        } catch (error) {

            console.error("Order processing error:", error);

            message.textContent = error.message;
            message.style.color = "red";

        }

    });


// ===============================
// RETRY ORDER
// ===============================

async function retryOrder(orderId) {

    if (!confirm(
        `Do you want to retry order ${orderId}?`
    )) {
        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/orders/retry/${orderId}`,
            {
                method: "POST",
                headers: getHeaders()
            }
        );


        const data = await response.json();

        console.log("Retry response:", data);


        if (!response.ok) {

            throw new Error(
                data.detail || "Retry failed"
            );

        }


        alert(
            `Order ${orderId} retry completed successfully`
        );


        loadOrders();

        if (typeof loadSummary === "function") {
            loadSummary();
        }

        if (typeof loadInventory === "function") {
            loadInventory();
        }


    } catch (error) {

        console.error("Retry error:", error);

        alert(error.message);

    }

}


// Load orders when dashboard opens
loadOrders();