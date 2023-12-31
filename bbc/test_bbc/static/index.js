// script.js
document.addEventListener("DOMContentLoaded", function() {
    const movieList = document.querySelector(".movies");
    const searchInput = document.getElementById("movieQuery");

    // Load the movies JSON file
    async function loadMovies() {
        const response = await fetch('/static/movies.json');
        const data = await response.json();
        return data;
    }

    // Handle the search input
    searchInput.addEventListener("input", function(e) {
        const query = e.target.value.toLowerCase();
        loadMovies().then(movies => {
            const filteredMovies = movies.filter(movie => movie.title.toLowerCase().includes(query));
            displayMovies(filteredMovies);
        });
    });

    function displayMovies(movies) {
        let htmlString = "";

        movies.forEach((movie) => {
            htmlString += `
                <li class="movie">
                    <figure class="movie__figure">
                        <a href="/play_movie/${movie.title}">
                            <img src="${movie.image}" class="movie__poster">
                        </a>
                    </figure>
                </li>
            `;
        });
        

        movieList.innerHTML = htmlString;
    }

    // Initial movie load
    loadMovies().then(movies => {
        displayMovies(movies);
    });
});

// Toggle sidebar
const burgerMenu = document.querySelector('.burger-menu');
const sidebar = document.querySelector('.sidebar');

burgerMenu.addEventListener('click', () => {
    if (sidebar.style.width === '0px' || sidebar.style.width === '') {
        sidebar.style.width = '250px';
    } else {
        sidebar.style.width = '0px';
    }
});

