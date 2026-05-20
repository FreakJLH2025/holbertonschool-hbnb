const API_URL = "https://web-80-218-221.cod-us-east-1.hbtn.io";

document.addEventListener("DOMContentLoaded", () => {
    console.log("SCRIPT RUNNING");
    const token = getCookie("token");
    const currentPage = window.location.pathname.split("/").pop();
    const publicPages = ["login.html", "register.html"];
    if (!token && !publicPages.includes(currentPage)) {
    window.location.href = "login.html?message=login_required";
    }
    
    const params = new URLSearchParams(window.location.search);

    if (params.get("message") === "login_required") {
        alert("You have to login first!");
    }

    const userGreeting = document.getElementById("user-greeting");
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            console.log("LOGIN CLICKED");
            event.preventDefault();
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch(API_URL + "/api/v1/auth/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = "token=" + data.access_token + "; path=/";
                    document.cookie = "user_id=" + data.user_id + "; path=/";
                    window.location.href = "index.html";
                } else {
                    const errorData = await response.json();
                    alert("Login failed: " + (errorData.message || response.statusText));
                }
            } catch (error) {
                alert("Error connecting to server: " + error.message);
                console.log(error)
            }
        });
    }

    const registerForm = document.getElementById("register-form");

    if (registerForm) {
        registerForm.addEventListener("submit", async (event) => {
    
            event.preventDefault();
    
            const first_name = document.getElementById("first_name").value;
            const last_name = document.getElementById("last_name").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
    
            try {
    
                const response = await fetch(API_URL + "/api/v1/users/", {
                    method: "POST",
    
                    headers: {
                        "Content-Type": "application/json"
                    },
    
                    body: JSON.stringify({
                        first_name,
                        last_name,
                        email,
                        password
                    })
                });
    
                if (response.ok) {
    
                    alert("Account created successfully!");
                    window.location.href = "login.html";
    
                } else {
    
                    const errorData = await response.json();
    
                    alert(
                        "Registration failed: " +
                        (errorData.error || response.statusText)
                    );
                }
    
            } catch (error) {
    
                alert("Error: " + error.message);
            }
        });
    }

    async function loadUserGreeting() {

        const userId = getCookie("user_id");
        console.log(userId);
        if (!userId) return;
    
        try {
    
            const response = await fetch(API_URL + "/api/v1/users/" + userId);
            console.log(response.status);

            if (response.ok) {
    
                const user = await response.json();
                console.log(user);

                if (userGreeting) {
                    userGreeting.textContent =
                        "Welcome, " + user.first_name;
                }
            }
    
        } catch (error) {
    
            console.log(error);
        }
    }

    const registerLink = document.getElementById("register-link");
    const logoutLink = document.getElementById("logout-link");
    const loginLink = document.getElementById("login-link");

    if (token) {

        if (loginLink) loginLink.style.display = "none";

        if (registerLink) registerLink.style.display = "none";

        if (logoutLink) logoutLink.style.display = "inline";

        loadUserGreeting();

    } else {

        if (loginLink) loginLink.style.display = "inline";

        if (registerLink) registerLink.style.display = "inline";

        if (logoutLink) logoutLink.style.display = "none";

        loadUserGreeting();
    }

    if (logoutLink) {

        logoutLink.addEventListener("click", (event) => {
    
            event.preventDefault();
    
            document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
            document.cookie = "user_id=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    
            window.location.href = "login.html";
        });
    }

    const placesList = document.getElementById("places-list");
    const priceFilter = document.getElementById("price-filter");

    if (placesList) {
        checkAuthenticationIndex();
    }

    function checkAuthenticationIndex() {
        const token = getCookie("token");
        if (!token) {
            if (loginLink) loginLink.style.display = "block";
        } else {
            if (loginLink) loginLink.style.display = "none";
        }
        fetchPlaces(token);
    }

    async function fetchPlaces(token) {
        try {
            const headers = {};
            if (token) headers["Authorization"] = "Bearer " + token;

            const response = await fetch(API_URL + "/api/v1/places/", {
                method: "GET",
                headers: headers
            });

            if (response.ok) {
                const places = await response.json();
		console.log("PLACES DATA");
		console.log(places);
                displayPlaces(places);
                setupFilter();
            } 
            else {
                alert("Failed to fetch places");
            }
        } catch (error) {
            alert("Error fetching places: " + error.message);
        }
    }

    function displayPlaces(places) {
        placesList.innerHTML = "";
        places.forEach(place => {
            const card = document.createElement("div");
            card.className = "place-card";
            card.dataset.price = place.price;

            card.innerHTML =
                "<h2>" + place.name + "</h2>" +
                "<p>$" + place.price + " per night</p>" +
                "<p>" + (place.description || "") + "</p>" +
                "<a href=\"place.html?id=" + place.id + "\" class=\"details-button\">View Details</a>";

            placesList.appendChild(card);
        });
    }

    function setupFilter() {
        if (priceFilter) {
            priceFilter.innerHTML =
                "<option value=\"all\" selected>All</option>" +
                "<option value=\"10\">$10</option>" +
                "<option value=\"50\">$50</option>" +
                "<option value=\"100\">$100</option>" +
                "<option value=\"200\">$200</option>";

            priceFilter.addEventListener("change", (event) => {
                const maxPrice = event.target.value;
                const cards = document.querySelectorAll(".place-card");
                cards.forEach(card => {
                    const price = parseInt(card.dataset.price, 10);
                    if (maxPrice === "all" || price <= parseInt(maxPrice, 10)) {
                        card.style.display = "block";
                    } else {
                        card.style.display = "none";
                    }
                });
            });
        }
    }

    const placeDetailsSection = document.querySelector(".place-info");
    const addReviewSection = document.getElementById("add-review");

    if (placeDetailsSection) {
        const placeId = getPlaceIdFromURL();
        const token = getCookie("token");

        if (!token) {
            if (addReviewSection) addReviewSection.style.display = "none";
        } else {
            if (addReviewSection) addReviewSection.style.display = "block";
        }

        fetchPlaceDetails(token, placeId);
    }

    async function fetchPlaceDetails(token, placeId) {
        try {
            const headers = {};
            if (token) headers["Authorization"] = "Bearer " + token;

            const response = await fetch(API_URL + "/api/v1/places/" + placeId, {
                method: "GET",
                headers: headers
            });

            if (response.ok) {
                const place = await response.json();
                displayPlaceDetails(place);
            } else {
                alert("Failed to fetch place details");
            }
        } catch (error) {
            alert("Error fetching place details: " + error.message);
        }
    }

    async function displayPlaceDetails(place) {
        const amenitiesList = place.amenities.map(a => "<li>" + a.name + "</li>").join("");

        placeDetailsSection.innerHTML =
            "<h2>" + place.name + "</h2>" +
            "<p><b>Price: $" + place.price + " per night</b></p>" +
            "<p>Description: " + (place.description || "") + "</p>" +
            "<p>Amenities:</p>" +
            "<ul>" + amenitiesList + "</ul>";

        const reviewsSection = document.getElementById("reviews");

        if (reviewsSection) {
            reviewsSection.innerHTML = "<h3>Reviews</h3>";
            if (place.reviews && place.reviews.length > 0) {
                await Promise.all(place.reviews.map(async (review) => {
                    const answer = await fetch(API_URL + "/api/v1/users/" + review.user_id);
                    console.log(answer)
                    const revuser = await answer.json();
                    console.log(revuser)
                    const card = document.createElement("div");
                    card.className = "review-card";
                    card.innerHTML =
                        "<p><i>\"" + review.text + "\"</i></p>" +
                        "<p><b>User: " + revuser.first_name + " " + revuser.last_name + "</b></p>" +
                        "<p>Rating: " + "★".repeat(review.rating) + "☆".repeat(5 - review.rating) + "</p>";
                    reviewsSection.appendChild(card);
                }));
            } else {
                reviewsSection.innerHTML += "<p>No reviews yet.</p>";
            }
        }
    }

    const reviewForm = document.getElementById("review-form");
    if (reviewForm) {
        const token = checkAuthenticationReview();
        const placeId = getPlaceIdFromURL();

        reviewForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById("review-text") || document.getElementById("review");
            const rating = document.getElementById("rating").value;
            const userId = getCookie("user_id");

            if (!userId) {
                alert("You must be logged in to submit a review.");
                window.location.href = "login.html";
                return;
            }

            try {
                const response = await fetch(API_URL + "/api/v1/reviews/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + token
                    },
                    body: JSON.stringify({
                        text: reviewText.value,
                        rating: parseInt(rating, 10),
                        user_id: userId,
                        place_id: placeId
                    })
                });

                if (response.ok) {
                    alert("Review submitted successfully!");
                    reviewForm.reset();
                    window.location.reload();
                } else {
                    const errorData = await response.json();
                    alert("Failed to submit review: " + (errorData.error || response.statusText));
                }
            } catch (error) {
                alert("Error submitting review: " + error.message);
            }
        });
    }
    const addPlaceForm = document.getElementById("add-place-form");
    if (addPlaceForm) {
        const token = getCookie("token");
        const userId = getCookie("user_id");

        async function loadAmenities() {
            try {
                const response = await fetch(API_URL + "/api/v1/amenities/");
                if (response.ok) {
                    const amenities = await response.json();
                    const amenitiesList = document.getElementById("amenities-list");
                    amenities.forEach(amenity => {
                        const label = document.createElement("label");
                        label.style.flexDirection = "row";
                        label.style.alignItems = "center";
                        label.style.gap = "8px";
                        const checkbox = document.createElement("input");
                        checkbox.type = "checkbox";
                        checkbox.value = amenity.id;
                        checkbox.id = "amenity-" + amenity.id;
                        label.appendChild(checkbox);
                        label.appendChild(document.createTextNode(amenity.name));
                        amenitiesList.appendChild(label);
                    });
                }
            } catch (error) {
                console.log("Error loading amenities: " + error.message);
            }
        }
        
        loadAmenities();

        addPlaceForm.addEventListener("submit", async (event) => {
            event.preventDefault();
        
            const name = document.getElementById("name").value;
            const description = document.getElementById("description").value;
            const price = parseFloat(document.getElementById("price").value);
        
            const selectedAmenities = [];
            document.querySelectorAll("#amenities-list input[type='checkbox']:checked").forEach(cb => {
                selectedAmenities.push(cb.value);
            });
        
            try {
                const response = await fetch(API_URL + "/api/v1/places/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + token
                    },
                    body: JSON.stringify({
                        name: name,
                        description: description,
                        price: price,
                        owner_id: userId,
                        amenity_ids: selectedAmenities
                    })
                });
        
                if (response.ok) {
                    alert("Place added successfully!");
                    window.location.href = "index.html";
                } else {
                    const errorData = await response.json();
                    alert("Failed to add place: " + (errorData.error || response.statusText));
                }
            } catch (error) {
                alert("Error adding place: " + error.message);
            }
        });
    }
    function getCookie(name) {
        const value = "; " + document.cookie;
        const parts = value.split("; " + name + "=");
        if (parts.length === 2) return parts.pop().split(";").shift();
        return null;
    }

    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get("id");
    }

    function checkAuthenticationReview() {
        const token = getCookie("token");
        if (!token) {
            window.location.href = "index.html";
        }
        return token;
    }
})