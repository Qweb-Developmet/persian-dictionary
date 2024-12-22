document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/search', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        console.log(data); // Log the response data
        document.getElementById('results').innerHTML = data;
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('search_term').addEventListener('input', function() {
    fetchSuggestions(this.value);
});

function fetchSuggestions(term) {
    if (term.length < 2) {
        document.getElementById('suggestions').innerHTML = '';
        return;
    }

    fetch('/suggestions?term=' + term)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        let suggestions = '';
        data.forEach(suggestion => {
            suggestions += '<div class="suggestion-item">' + suggestion + '</div>';
        });
        document.getElementById('suggestions').innerHTML = suggestions;
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById('suggestions').addEventListener('click', function(event) {
    if (event.target.classList.contains('suggestion-item')) {
        const [persian, english] = event.target.textContent.split(' - ');
        document.getElementById('search_term').value = persian;
        document.getElementById('suggestions').innerHTML = '';
    }
});
