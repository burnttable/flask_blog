document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.btn-like, .btn-dislike');
    const commentForm = document.querySelector('.comment-form');
    const commentsList = document.getElementById('comments-list');
    const deleteCommentButtons = document.querySelectorAll('.delete-comment');

    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            const type = this.getAttribute('data-type');
            const url = `/api/posts/${postId}/${type}`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.querySelector('.like-count').textContent = data.like_count;
                    document.querySelector('.dislike-count').textContent = data.dislike_count;

                    likeButtons.forEach(btn => btn.classList.remove('active'));

                    if (data.action === 'added' || data.action === 'changed') {
                        this.classList.add('active');
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const postId = this.getAttribute('data-post-id');
            const content = this.querySelector('textarea[name="content"]').value;
            const url = `/api/posts/${postId}/comments`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `content=${encodeURIComponent(content)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const commentHtml = `
                        <div class="comment" data-comment-id="${data.comment.id}">
                            <div class="comment-header">
                                <span class="comment-author">${data.comment.author}</span>
                                <span class="comment-date">${data.comment.created_at}</span>
                            </div>
                            <div class="comment-content">${data.comment.content.replace(/\n/g, '<br>')}</div>
                            <button class="btn btn-sm btn-danger delete-comment" data-comment-id="${data.comment.id}">Delete</button>
                        </div>
                    `;
                    commentsList.insertAdjacentHTML('beforeend', commentHtml);
                    this.querySelector('textarea[name="content"]').value = '';

                    const deleteBtn = commentsList.lastElementChild.querySelector('.delete-comment');
                    attachDeleteListener(deleteBtn);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    function attachDeleteListener(button) {
        button.addEventListener('click', function() {
            if (!confirm('Are you sure you want to delete this comment?')) {
                return;
            }

            const commentId = this.getAttribute('data-comment-id');
            const url = `/api/comments/${commentId}`;

            fetch(url, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const commentElement = document.querySelector(`.comment[data-comment-id="${commentId}"]`);
                    if (commentElement) {
                        commentElement.remove();
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    deleteCommentButtons.forEach(button => {
        attachDeleteListener(button);
    });
});
