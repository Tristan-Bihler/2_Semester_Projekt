document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const loginSection = document.getElementById('login-section');
    const mainSection = document.getElementById('main-section');
    const favoritesSection = document.getElementById('favorites-section');

    const loginUsernameInput = document.getElementById('loginUsername');
    const loginButton = document.getElementById('loginButton');
    const signupUsernameInput = document.getElementById('signupUsername');
    const signupButton = document.getElementById('signupButton');

    const favoritesButton = document.getElementById('favoritesButton');
    const backToMainButton = document.getElementById('backToMainButton');

    const searchFilmInput = document.getElementById('searchFilm');
    const clearSearchButton = document.getElementById('clearSearch');
    const availableFilmsList = document.getElementById('availableFilmsList');
    const recommendedFilmsList = document.getElementById('recommendedFilmsList');
    const likedFilmsList = document.getElementById('likedFilmsList');

    const detailFilmName = document.getElementById('detailFilmName');
    const detailFilmDescription = document.getElementById('detailFilmDescription');
    const trailerButton = document.getElementById('trailerButton');
    const addToWatchlistButton = document.getElementById('addToWatchlistButton');
    const removeFromListButton = document.getElementById('removeFromListButton');

    let currentUser = null;
    let allFilms = []; // To store all film data
    let currentSelectedFilm = null; // Stores full film object for details

    // --- Utility Functions ---
    function showSection(section) {
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
        section.classList.add('active');
    }

    function clearFilmDetails() {
        detailFilmName.textContent = "Name: No Film Selected";
        detailFilmDescription.textContent = "Beschreibung: Select a film from the lists above to see its details.";
        trailerButton.disabled = true;
        currentSelectedFilm = null;
    }

    function populateList(listElement, items) {
        listElement.innerHTML = '';
        items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            listElement.appendChild(li);
        });
    }

    // --- API Simulation (Replace with actual Fetch to your backend) ---
    // In a real web app, these would be async functions making HTTP requests.
    // For this example, we'll use placeholder data.

    async function fetchUsers() {
        // Replace with: const response = await fetch('/api/users');
        // const data = await response.json();
        // return data.map(u => u.name.toLowerCase());
        return ['user1', 'testuser', 'demo']; // Placeholder
    }

    async function fetchAllFilms() {
        // Replace with: const response = await fetch('/api/films');
        // return await response.json();
        return [ // Placeholder Film Data
            { name: "Movie A", description: "A great action movie.", genre: ["Action", "Adventure"], youtubeTrailerUrl: "https://www.youtube.com/watch?v=trailerA" },
            { name: "Movie B", description: "A heartwarming drama.", genre: ["Drama", "Romance"], youtubeTrailerUrl: "https://www.youtube.com/watch?v=trailerB" },
            { name: "Movie C", description: "Hilarious comedy.", genre: ["Comedy"], youtubeTrailerUrl: "" }, // No trailer
            { name: "Movie D", description: "Sci-Fi classic.", genre: ["Sci-Fi"], youtubeTrailerUrl: "https://www.youtube.com/watch?v=trailerD" },
            { name: "Movie E", description: "Fantasy epic.", genre: ["Fantasy", "Adventure"], youtubeTrailerUrl: "https://www.youtube.com/watch?v=trailerE" },
        ];
    }

    async function getUserLikedFilms(username) {
        // Replace with: const response = await fetch(`/api/users/${username}/liked_films`);
        // return await response.json();
        // Placeholder: in a real app, this would fetch from a database
        const userData = JSON.parse(localStorage.getItem('userData')) || {};
        return userData[username] ? userData[username].favorite_movies : [];
    }

    async function getRecommendations(username) {
        // This logic would ideally be on the backend, given the complexity.
        // For frontend simulation, we'll replicate the core logic here.
        const likedMovies = await getUserLikedFilms(username);
        if (likedMovies.length === 0) return [];

        const likedGenres = [];
        likedMovies.forEach(likedTitle => {
            const movie = allFilms.find(f => f.name.toLowerCase() === likedTitle.toLowerCase());
            if (movie && movie.genre) {
                likedGenres.extend(movie.genre);
            }
        });

        const genreCounts = likedGenres.reduce((acc, genre) => {
            acc[genre] = (acc[genre] || 0) + 1;
            return acc;
        }, {});

        const recommendationsWithScores = {};
        allFilms.forEach(movie => {
            const movieTitle = movie.name;
            if (likedMovies.map(m => m.toLowerCase()).includes(movieTitle.toLowerCase())) {
                return; // Skip already liked movies
            }

            let score = 0;
            movie.genre.forEach(genre => {
                score += genreCounts[genre] || 0;
            });

            if (score > 0) {
                recommendationsWithScores[movieTitle] = score;
            }
        });

        return Object.entries(recommendationsWithScores)
            .sort(([, scoreA], [, scoreB]) => scoreB - scoreA)
            .map(([title,]) => title);
    }

    // --- Event Handlers ---

    loginButton.addEventListener('click', async () => {
        const username = loginUsernameInput.value.trim().toLowerCase();
        const users = await fetchUsers();
        if (users.includes(username)) {
            currentUser = username;
            loadMainScreen();
            showSection(mainSection);
            alert(`Welcome, ${username}!`);
        } else {
            alert("User not found.");
            console.log("Es gibt den User nicht"); // Match console output from Python
        }
    });

    signupButton.addEventListener('click', async () => {
        const username = signupUsernameInput.value.trim().toLowerCase();
        if (!username) {
            alert("Please enter a username to sign up.");
            return;
        }

        // Simulate writing to JSON (in a real app, this would be a POST request)
        const userData = JSON.parse(localStorage.getItem('userData')) || {};
        if (userData[username]) {
            alert("User already exists. Please choose a different username.");
            return;
        }
        userData[username] = { name: username, favorite_movies: [] };
        localStorage.setItem('userData', JSON.stringify(userData));
        alert(`User '${username}' registered successfully! You can now log in.`);
        signupUsernameInput.value = '';
    });

    favoritesButton.addEventListener('click', async () => {
        if (!currentUser) {
            alert("Please log in first.");
            return;
        }
        await loadFavoritesScreen();
        showSection(favoritesSection);
    });

    backToMainButton.addEventListener('click', () => {
        if (!currentUser) {
            alert("Please log in first.");
            return;
        }
        loadMainScreen();
        showSection(mainSection);
    });

    searchFilmInput.addEventListener('keyup', () => {
        filterFilms();
    });

    clearSearchButton.addEventListener('click', () => {
        searchFilmInput.value = '';
        filterFilms();
        clearFilmDetails();
    });

    availableFilmsList.addEventListener('click', (event) => {
        if (event.target.tagName === 'LI') {
            document.querySelectorAll('#availableFilmsList li').forEach(li => li.classList.remove('selected'));
            event.target.classList.add('selected');

            const selectedFilmName = event.target.textContent;
            currentSelectedFilm = allFilms.find(film => film.name === selectedFilmName);

            if (currentSelectedFilm) {
                detailFilmName.textContent = `Name: ${currentSelectedFilm.name}`;
                detailFilmDescription.textContent = `Description: ${currentSelectedFilm.description}`;
                trailerButton.disabled = !currentSelectedFilm.youtubeTrailerUrl;
            } else {
                clearFilmDetails();
            }
        }
    });

    trailerButton.addEventListener('click', () => {
        if (currentSelectedFilm && currentSelectedFilm.youtubeTrailerUrl) {
            window.open(currentSelectedFilm.youtubeTrailerUrl, '_blank');
        } else {
            alert("No trailer link available for the selected film.");
        }
    });

    addToWatchlistButton.addEventListener('click', async () => {
        if (!currentUser) {
            alert("Please log in first.");
            return;
        }
        if (currentSelectedFilm) {
            // Simulate writing to JSON (in a real app, this would be a POST/PUT request)
            const userData = JSON.parse(localStorage.getItem('userData')) || {};
            if (userData[currentUser]) {
                if (!userData[currentUser].favorite_movies.includes(currentSelectedFilm.name)) {
                    userData[currentUser].favorite_movies.push(currentSelectedFilm.name);
                    localStorage.setItem('userData', JSON.stringify(userData));
                    alert(`${currentSelectedFilm.name} added to your watchlist!`);
                    await updateRecommendedFilms();
                } else {
                    alert(`${currentSelectedFilm.name} is already in your watchlist.`);
                }
            } else {
                alert("Error: User data not found. Please re-login.");
            }
        } else {
            alert("Please select a film first.");
        }
    });

    removeFromListButton.addEventListener('click', async () => {
        if (!currentUser) {
            alert("Please log in first.");
            return;
        }
        const selectedItem = likedFilmsList.querySelector('li.selected');
        if (selectedItem) {
            const filmToRemove = selectedItem.textContent;
            const userData = JSON.parse(localStorage.getItem('userData')) || {};
            if (userData[currentUser] && userData[currentUser].favorite_movies) {
                const initialCount = userData[currentUser].favorite_movies.length;
                userData[currentUser].favorite_movies = userData[currentUser].favorite_movies.filter(film => film !== filmToRemove);
                if (userData[currentUser].favorite_movies.length < initialCount) {
                    localStorage.setItem('userData', JSON.stringify(userData));
                    alert(`${filmToRemove} removed from your watchlist.`);
                    await loadFavoritesScreen(); // Reload favorites list
                } else {
                    alert(`Film '${filmToRemove}' not found in your favorites.`);
                }
            }
        } else {
            alert("Please select a film to remove from your favorites.");
        }
    });

    likedFilmsList.addEventListener('click', (event) => {
        if (event.target.tagName === 'LI') {
            document.querySelectorAll('#likedFilmsList li').forEach(li => li.classList.remove('selected'));
            event.target.classList.add('selected');
        }
    });

    // --- Data Loading / UI Updates ---

    async function filterFilms() {
        const searchTerm = searchFilmInput.value.trim().toLowerCase();
        const filteredFilms = allFilms.filter(film =>
            film.name.toLowerCase().includes(searchTerm)
        ).map(film => film.name);
        populateList(availableFilmsList, filteredFilms);
        clearFilmDetails();
    }

    async function updateRecommendedFilms() {
        if (currentUser) {
            const recommended = await getRecommendations(currentUser);
            populateList(recommendedFilmsList, recommended);
        } else {
            recommendedFilmsList.innerHTML = '';
        }
    }

    async function loadMainScreen() {
        allFilms = await fetchAllFilms();
        filterFilms(); // Populate available films initially
        await updateRecommendedFilms();
        clearFilmDetails();
    }

    async function loadFavoritesScreen() {
        if (currentUser) {
            const likedFilms = await getUserLikedFilms(currentUser);
            populateList(likedFilmsList, likedFilms);
        } else {
            likedFilmsList.innerHTML = '';
        }
        // Clear selection when loading the screen
        document.querySelectorAll('#likedFilmsList li').forEach(li => li.classList.remove('selected'));
    }

    // Initial load: show login section
    showSection(loginSection);
});
