let userToken = null;

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function setupLoginForm() {
  const loginForm = document.getElementById('login-form');
  if (!loginForm) return;

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
      const response = await fetch('http://localhost:5000/api/v1/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        userToken = data.access_token;
        window.location.href = 'index.html';
      } else {
        const error = await response.json();
        alert('Login failed: ' + (error.message || response.statusText));
      }
    } catch (err) {
      console.error('Error:', err);
      alert('Something went wrong. Please try again later.');
    }
  });
}

function checkAuthentication() {
  userToken = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (loginLink) {
    loginLink.style.display = userToken ? 'none' : 'block';
  }
  fetchPlaces(userToken);
}

async function fetchPlaces(token) {
  try {
    const response = await fetch('http://localhost:5000/api/v1/places', {
      method: 'GET',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
    });

    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
      setupPriceFilter(places);
    } else {
      alert('Failed to fetch places');
    }
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

function displayPlaces(places) {
  const list = document.getElementById('places-list');
  if (!list) return;
  list.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.classList.add('place-card');
    card.setAttribute('data-price', place.price);

    card.innerHTML = `
      <h3>${place.name}</h3>
      <p>$${place.price}/night</p>
      <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
    `;

    list.appendChild(card);
  });
}

function setupPriceFilter(places) {
  const filter = document.getElementById('price-filter');
  if (!filter) return;

  filter.innerHTML = `
    <option value="All">All</option>
    <option value="10">Under $10</option>
    <option value="50">Under $50</option>
    <option value="100">Under $100</option>
  `;

  filter.addEventListener('change', (event) => {
    const maxPrice = event.target.value;
    document.querySelectorAll('.place-card').forEach(card => {
      const price = parseFloat(card.getAttribute('data-price'));
      card.style.display = (maxPrice === 'All' || price <= parseFloat(maxPrice)) ? 'block' : 'none';
    });
  });
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

function checkPlaceAuthentication() {
  userToken = getCookie('token');
  const addReviewSection = document.getElementById('add-review');
  const placeId = getPlaceIdFromURL();

  if (addReviewSection) {
    addReviewSection.style.display = userToken ? 'block' : 'none';
  }

  fetchPlaceDetails(userToken, placeId);
}

async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
    });

    if (response.ok) {
      const place = await response.json();
      displayPlaceDetails(place);
    } else {
      alert('Failed to fetch place details');
    }
  } catch (error) {
    console.error('Error fetching place:', error);
  }
}

function displayPlaceDetails(place) {
  const section = document.getElementById('place-details');
  if (!section) return;
  section.innerHTML = '';

  const container = document.createElement('div');
  container.classList.add('place-info');
  container.innerHTML = `
    <h2>${place.name}</h2>
    <p><strong>Host:</strong> ${place.host}</p>
    <p><strong>Price:</strong> $${place.price}/night</p>
    <p><strong>Description:</strong> ${place.description}</p>
    <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
  `;
  section.appendChild(container);

  const reviewsSection = document.getElementById('reviews');
  if (!reviewsSection) return;
  reviewsSection.innerHTML = '<h3>Reviews</h3>';
  place.reviews.forEach(review => {
    const reviewCard = document.createElement('div');
    reviewCard.classList.add('review-card');
    reviewCard.innerHTML = `
      <p><strong>${review.user}:</strong> ${review.comment}</p>
      <p>Rating: ${'⭐'.repeat(review.rating)}</p>
    `;
    reviewsSection.appendChild(reviewCard);
  });
}

function checkReviewAuth() {
  const token = getCookie('token');
  if (!token) {
    window.location.href = 'index.html';
  }
  return token;
}

async function submitReview(token, placeId, reviewText, rating) {
  try {
    const response = await fetch('http://localhost:5000/api/v1/reviews', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        place_id: placeId,
        comment: reviewText,
        rating: parseInt(rating)
      })
    });

    if (response.ok) {
      alert('Review submitted successfully!');
      document.getElementById('review-form').reset();
    } else {
      const error = await response.json();
      alert('Failed to submit review: ' + (error.message || response.statusText));
    }
  } catch (error) {
    console.error('Error submitting review:', error);
    alert('Something went wrong. Try again later.');
  }
}

function setupReviewForm() {
  const token = checkReviewAuth();
  const placeId = getPlaceIdFromURL();
  const reviewForm = document.getElementById('review-form');

  if (reviewForm) {
    reviewForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const reviewText = document.getElementById('review').value;
      const rating = document.getElementById('rating').value;
      submitReview(token, placeId, reviewText, rating);
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (window.location.pathname.includes('login.html')) {
    setupLoginForm();
  }

  if (window.location.pathname.includes('index.html')) {
    checkAuthentication();
  }

  if (window.location.pathname.includes('place.html')) {
    checkPlaceAuthentication();
  }

  if (window.location.pathname.includes('add_review.html')) {
    setupReviewForm();
  }
});
