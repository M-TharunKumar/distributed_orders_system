const API_URL = "http://127.0.0.1:8000";

const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");


// ========================================
// LOGIN FORM
// ========================================

loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const username =
        document.getElementById("username").value.trim();

    const password =
        document.getElementById("password").value; 


    // Clear previous message
    message.textContent = "Logging in...";
    message.style.color = "blue";


    // ========================================  
    // VALIDATION
    // ========================================

    if (!username || !password) {

        message.textContent =
            "Please enter username and password";

        message.style.color = "red";

        return;
    }


    try {

        // ========================================
        // SEND LOGIN REQUEST
        // ========================================

        const response = await fetch(
            `${API_URL}/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }
        );


        // ========================================
        // READ RESPONSE
        // ========================================

        const data = await response.json();


        console.log(
            "Login Status:",
            response.status
        );

        console.log(
            "Login Response:",
            data
        );


        // ========================================
        // HANDLE ERROR
        // ========================================

        if (!response.ok) {

            if (Array.isArray(data.detail)) {

                const errors = data.detail
                    .map(error => error.msg)
                    .join(", ");

                throw new Error(errors);
            }

            throw new Error(
                data.detail || "Login failed"
            );
        }


        // ========================================
        // SAVE JWT
        // ========================================

        localStorage.setItem(
            "access_token",
            data.access_token
        );


        // ========================================
        // SAVE USERNAME
        // ========================================

        localStorage.setItem(
            "username",
            username
        );


        console.log(
            "JWT token saved successfully"
        );


        // ========================================
        // SUCCESS MESSAGE
        // ========================================

        message.textContent =
            "Login successful! Redirecting...";

        message.style.color = "green";


        // ========================================
        // REDIRECT TO DASHBOARD
        // ========================================

        setTimeout(function () {

            window.location.href =
                "dashboard.html";

        }, 500);


    } catch (error) {

        console.error(
            "Login Error:",
            error
        );


        message.textContent =
            error.message || "Login failed";

        message.style.color = "red";

    }

});