document.getElementById("checkButton").addEventListener("click", async function() {
    const content = document.getElementById("contentInput").value;

    if (!content) {
        alert("Please enter content to verify.");
        return;
    }

    const API_URL = window.location.hostname === "localhost" ? "http://127.0.0.1:5000/api/fact-check" : "https://vercify-prototype.vercel.app/api/fact-check";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content: content })
        });

        const result = await response.json();

        document.getElementById("resultContainer").style.display = "block";
        document.getElementById("status").innerText = `Status: ${result.status}`;
        document.getElementById("score").innerText = `Score: ${result.score}/10`;
        document.getElementById("explanation").innerText = `Explanation: ${result.verification_details}`;
    } catch (error) {
        console.error("Error:", error);
    }
});

document.getElementById("postButton").addEventListener("click", async function() {
    const postContent = document.getElementById("postContent").value;

    if (!postContent) {
        alert("Please enter content for the post.");
        return;
    }

    const API_URL = window.location.hostname === "localhost" ? "http://127.0.0.1:5000/api/posts" : "https://vercify-prototype.vercel.app/api/posts";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content: postContent })
        });

        const result = await response.json();
        alert("Post created successfully!");
        document.getElementById("postContent").value = ""; // Clear input
        loadPosts(); // Reload posts
    } catch (error) {
        console.error("Error:", error);
    }
});

async function loadPosts() {
    const API_URL = window.location.hostname === "localhost" ? "http://127.0.0.1:5000/api/posts" : "https://vercify-prototype.vercel.app/api/posts";

    try {
        const response = await fetch(API_URL);
        const posts = await response.json();
        const postsContainer = document.getElementById("postsContainer");
        postsContainer.innerHTML = ""; // Clear existing posts

        posts.forEach(post => {
            const postElement = document.createElement("div");
            postElement.className = "post";
            postElement.innerHTML = `
                <h3>${post.user}</h3>
                <p>${post.content}</p>
                <button onclick="upvotePost(${post.id})">Upvote (${post.upvotes})</button>
                <button onclick="downvotePost(${post.id})">Downvote (${post.downvotes})</button>
                <div id="comments-${post.id}"></div>
                <textarea id="commentInput-${post.id}" placeholder="Add a comment..."></textarea>
                <button onclick="addComment(${post.id})">Comment</button>
            `;
            postsContainer.appendChild(postElement);
            loadComments(post.id);
        });
    } catch (error) {
        console.error("Error loading posts:", error);
    }
}

async function loadComments(postId) {
    const API_URL = window.location.hostname === "localhost" ? `http://127.0.0.1:5000/api/posts/${postId}/comments` : `https://vercify-prototype.vercel.app/api/posts/${postId}/comments`;

    try {
        const response = await fetch(API_URL);
        const comments = await response.json();
        const commentsContainer = document.getElementById(`comments-${postId}`);
        commentsContainer.innerHTML = ""; // Clear existing comments

        comments.forEach(comment => {
            const commentElement = document.createElement("div");
            commentElement.className = "comment";
            commentElement.innerHTML = `<strong>${comment.user}</strong>: ${comment.content}`;
            commentsContainer.appendChild(commentElement);
        });
    } catch (error) {
        console.error("Error loading comments:", error);
    }
}

async function addComment(postId) {
    const commentInput = document.getElementById(`commentInput-${postId}`);
    const commentContent = commentInput.value;

    if (!commentContent) {
        alert("Please enter a comment.");
        return;
    }

    const API_URL = window.location.hostname === "localhost" ? `http://127.0.0.1:5000/api/posts/${postId}/comments` : `https://vercify-prototype.vercel.app/api/posts/${postId}/comments`;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content: commentContent })
        });

        const result = await response.json();
        alert("Comment added successfully!");
        commentInput.value = ""; // Clear input
        loadComments(postId); // Reload comments
    } catch (error) {
        console.error("Error adding comment:", error);
    }
}

async function upvotePost(postId) {
    const API_URL = window.location.hostname === "localhost" ? `http://127.0.0.1:5000/api/posts/${postId}/upvote` : `https://vercify-prototype.vercel.app/api/posts/${postId}/upvote`;

    try {
        await fetch(API_URL, { method: "POST" });
        loadPosts(); // Reload posts to update upvote count
    } catch (error) {
        console.error("Error upvoting post:", error);
    }
}

async function downvotePost(postId) {
    const API_URL = window.location.hostname === "localhost" ? `http://127.0.0.1:5000/api/posts/${postId}/downvote` : `https://vercify-prototype.vercel.app/api/posts/${postId}/downvote`;

    try {
        await fetch(API_URL, { method: "POST" });
        loadPosts(); // Reload posts to update downvote count
    } catch (error) {
        console.error("Error downvoting post:", error);
    }
}

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    const response = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    if (response.redirected) {
        window.location.href = response.url;
    } else {
        const result = await response.json();
        alert(result.message || result.error);
    }
});

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    if (response.redirected) {
        window.location.href = response.url;
    } else {
        const result = await response.json();
        alert(result.message || result.error);
    }
});

document.getElementById('create-post-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const content = document.getElementById('post-content').value;

    const response = await fetch('/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content })
    });

    const result = await response.json();
    alert(result.message || result.error);
});

document.getElementById('fact-check-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const content = document.getElementById('fact-check-content').value;

    const response = await fetch('/api/fact-check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content })
    });

    const result = await response.json();
    alert(result.verification_details || result.error);
});

// Load posts on page load
window.onload = loadPosts;