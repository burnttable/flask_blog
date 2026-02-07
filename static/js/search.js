document.addEventListener('DOMContentLoaded', function() {
    const searchForms = document.querySelectorAll('.search-form');

    searchForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const query = this.querySelector('input[name="query"]').value;
            const resultsContainer = document.getElementById('search-results');

            if (!query.trim()) {
                return;
            }

            fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `query=${encodeURIComponent(query)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    displayResults(data.results, resultsContainer);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    function displayResults(results, container) {
        if (!container) {
            return;
        }

        if (results.length === 0) {
            container.innerHTML = '<p class="text-center">No results found.</p>';
            return;
        }

        container.innerHTML = results.map(post => `
            <div class="post-card">
                <h2 class="post-title">
                    <a href="/posts/${post.id}">${post.title}</a>
                </h2>
                <div class="post-meta">
                    <span class="post-author">By ${post.author}</span>
                    <span class="post-date">${post.created_at}</span>
                </div>
                <div class="post-summary">
                    ${post.summary}
                </div>
            </div>
        `).join('');
    }
});
