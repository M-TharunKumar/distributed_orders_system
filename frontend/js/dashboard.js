const API_URL =
    "http://127.0.0.1:8000";


const token =
    localStorage.getItem(
        "access_token"
    );


const username =
    localStorage.getItem(
        "username"
    );


if (!token) {

    window.location.href =
        "login.html";
}


const welcomeUser = document.getElementById("username");

if (welcomeUser) {
    welcomeUser.textContent = username || "";
}


function getHeaders() {

    return {
        "Authorization":
            `Bearer ${token}`,

        "Content-Type":
            "application/json"
    };
}


function logout() {

    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "username"
    );

    window.location.href =
        "login.html";
}


async function loadSummary() {

    try {

        const [response, ordersResponse] = await Promise.all([
            fetch(`${API_URL}/reports/summary`, {
                headers: getHeaders()
            }),
            fetch(`${API_URL}/orders/`, {
                headers: getHeaders()
            })
        ]);


        if (!response.ok || !ordersResponse.ok) {

            console.error(
                "Failed to load dashboard summary"
            );

            return;
        }


        const data =
            await response.json();


        const report =
            data.report;

        const ordersData = await ordersResponse.json();
        const orders = ordersData.orders || ordersData;

        document.getElementById(
            "latestOrderId"
        ).textContent =
            orders.length ? orders[0].order_id : "-";

        document.getElementById(
            "pendingOrders"
        ).textContent =
            orders.filter(order => order.processing_status === "PENDING").length;


        document.getElementById(
            "totalOrders"
        ).textContent =
            report.total_orders;


        document.getElementById(
            "successfulOrders"
        ).textContent =
            report.successful_orders;


        document.getElementById(
            "failedOrders"
        ).textContent =
            report.failed_orders;


        document.getElementById(
            "retriedOrders"
        ).textContent =
            report.retried_orders;

    }
    catch (error) {

        console.error(error);

    }
}


loadSummary();