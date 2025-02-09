from pydantic import BaseModel
from src.models import Post, Comment
from supabase_client import supabase

class PostResponse(BaseModel):
    id: int
    content: str
    user: str
    upvotes: int
    downvotes: int
    comments: list[Comment]

class CommentResponse(BaseModel):
    id: int
    content: str
    user: str
    post_id: int

# Example test for creating a post
def test_create_post():
    new_post = Post.create(content="This is a test post", user="test_user")
    assert new_post.content == "This is a test post"
    assert new_post.user == "test_user"

# Example test for creating a comment
def test_create_comment():
    post = Post.create(content="This is a test post", user="test_user")
    new_comment = Comment.create(content="This is a test comment", user="comment_user", post_id=post.id)
    assert new_comment.content == "This is a test comment"
    assert new_comment.user == "comment_user"
    assert new_comment.post_id == post.id

# Example test for upvoting a post
def test_upvote_post():
    post = Post.create(content="This is a test post", user="test_user")
    post.upvote()
    assert post.upvotes == 1

# Example test for downvoting a post
def test_downvote_post():
    post = Post.create(content="This is a test post", user="test_user")
    post.downvote()
    assert post.downvotes == 1

# Example test for retrieving posts
def test_get_posts():
    posts = Post.get_all()
    assert isinstance(posts, list)  # Ensure it returns a list of posts

# Example test for retrieving comments for a post
def test_get_comments():
    post = Post.create(content="This is a test post", user="test_user")
    comments = Comment.get_by_post_id(post.id)
    assert isinstance(comments, list)  # Ensure it returns a list of comments

# Example test for user authentication
def test_user_authentication():
    user_data = {"email": "test@example.com", "password": "password123"}
    response = supabase.auth.sign_in(**user_data)
    assert response.user is not None  # Ensure user is authenticated

# Example test for AI model interaction
def test_fact_check():
    content = "John and Susan are going to an AI conference on Friday."
    result = fact_check(content)
    assert "status" in result  # Ensure the result contains a status
    assert "score" in result  # Ensure the result contains a score
    assert "verification_details" in result  # Ensure the result contains verification details