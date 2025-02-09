from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from flask_login import login_required, login_user
from src.models import Post, Comment
from src.auth import register_user, authenticate_user,User
from datetime import datetime
from supabase_client import supabase
import uuid

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/")
def home():
    return render_template("index.html")

@routes_bp.route("/register")
def register_page():
    return render_template("register.html")

@routes_bp.route("/login")
def login_page():
    return render_template("login.html")

@routes_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@routes_bp.route("/posts")
def posts_page():
    posts = Post.get_all()
    return render_template("posts.html", posts=posts)

@routes_bp.route("/posts/<uuid:post_id>")
def post_page(post_id):
    post = Post.get_by_id(post_id)
    if post:
        user_response = supabase.table('users').select('username').eq('id', post['user_id']).execute()
        if user_response.data:
            post['username'] = user_response.data[0]['username']
        else:
            post['username'] = 'Unknown'
    comments = Comment.get_by_post_id(post_id)
    # Retrieve usernames for comments
    for comment in comments:
        user_response = supabase.table('users').select('username').eq('id', comment['user_id']).execute()
        if user_response.data:
            comment['username'] = user_response.data[0]['username']
        else:
            comment['username'] = 'Unknown'
    return render_template("post.html", post=post, comments=comments)

@routes_bp.route("/api/register", methods=["POST"])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    print("Register data received:", username, email, password)  # Debugging statement
    if not email or not password:
        flash("Email and password are required", "danger")
        return redirect(url_for('routes.register_page'))

    result = register_user(username, email, password)
    print("User registered:", result)  # Debugging statement
    if result.get("error"):
        flash(result["error"], "danger")
        return redirect(url_for('routes.register_page'))
    flash(result["message"], "success")
    return redirect(url_for('routes.login_page'))

@routes_bp.route("/api/login", methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    print("Login data received:", email, password)  # Debugging statement
    if not email or not password:
        flash("Email and password are required", "danger")
        return redirect(url_for('routes.login_page'))

    result = authenticate_user(email, password)
    if result.get("error"):
        flash(result["error"], "danger")
        return redirect(url_for('routes.login_page'))
    print("User logged in:", result)  # Debugging statement
    user = User(id=result['user_id'], username=email, email=email)
    login_user(user)  # Log the user in
    session['email'] = email  # Store email in session
    session['user_id'] = result['user_id']  # Store user ID in session
    flash(result["message"], "success")
    return redirect(url_for('routes.dashboard'))

@routes_bp.route("/api/posts", methods=["POST"])
@login_required
def create_post():
    content = request.form.get('content')
    user_id = session.get('user_id')  # Get user ID from session
    print("Create post data received:", content, user_id)  # Debugging statement
    if not content or not user_id:
        flash("Content and user ID are required", "danger")
        return redirect(url_for('routes.dashboard'))

    post = Post.create(content=content, user_id=user_id)
    print("Post created:", post)  # Debugging statement
    flash("Post created successfully", "success")
    return redirect(url_for('routes.dashboard'))

@routes_bp.route("/api/posts/<uuid:post_id>/comments", methods=["POST"])
@login_required
def add_comment(post_id):
    content = request.form.get('content')
    user_id = session.get('user_id')  # Get user ID from session
    print("Add comment data received:", content, user_id)  # Debugging statement
    if not content or not user_id:
        flash("Content and user ID are required", "danger")
        return redirect(url_for('routes.post_page', post_id=post_id))

    comment = Comment.create(post_id=str(post_id), content=content, user_id=user_id)
    print("Comment added:", comment)  # Debugging statement
    flash("Comment added successfully", "success")
    return redirect(url_for('routes.post_page', post_id=post_id))

@routes_bp.route("/api/posts/<uuid:post_id>/upvote", methods=["POST"])
@login_required
def upvote_post(post_id):
    user_id = session.get('user_id')
    print("Upvote post data received:", post_id, user_id)  # Debugging statement
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    post = Post.upvote(str(post_id), user_id)
    if post.get("error"):
        return jsonify(post), 400

    print("Post upvoted:", post)  # Debugging statement
    post['id'] = str(post['id'])  # Convert UUID to string
    flash("Post upvoted successfully", "success")
    return redirect(url_for('routes.post_page', post_id=post_id))

@routes_bp.route("/api/posts/<uuid:post_id>/downvote", methods=["POST"])
@login_required
def downvote_post(post_id):
    user_id = session.get('user_id')
    print("Downvote post data received:", post_id, user_id)  # Debugging statement
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    post = Post.downvote(str(post_id), user_id)
    if post.get("error"):
        return jsonify(post), 400

    print("Post downvoted:", post)  # Debugging statement
    post['id'] = str(post['id'])  # Convert UUID to string
    flash("Post downvoted successfully", "success")
    return redirect(url_for('routes.post_page', post_id=post_id))

@routes_bp.route("/api/comments/<uuid:comment_id>/upvote", methods=["POST"])
@login_required
def upvote_comment(comment_id):
    user_id = session.get('user_id')
    print("Upvote comment data received:", comment_id, user_id)  # Debugging statement
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    # Fetch current upvote count from Supabase
    comment_response = supabase.table('comments').select('upvotes').eq('id', str(comment_id)).execute()
    if comment_response.data:
        current_upvotes = comment_response.data[0]['upvotes']
    else:
        return jsonify({"error": "Comment not found"}), 404

    # Increment upvote count
    new_upvotes = current_upvotes + 1
    update_response = supabase.table('comments').update({'upvotes': new_upvotes}).eq('id', str(comment_id)).execute()
    if update_response.data is None:
        return jsonify({"error": "Failed to update upvotes"}), 400

    print("Comment upvoted:", update_response.data)  # Debugging statement
    flash("Comment upvoted successfully", "success")
    return redirect(url_for('routes.post_page', post_id=comment_id))

@routes_bp.route("/api/comments/<uuid:comment_id>/downvote", methods=["POST"])
@login_required
def downvote_comment(comment_id):
    user_id = session.get('user_id')
    print("Downvote comment data received:", comment_id, user_id)  # Debugging statement
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    # Fetch current downvote count from Supabase
    comment_response = supabase.table('comments').select('downvotes').eq('id', str(comment_id)).execute()
    if comment_response.data:
        current_downvotes = comment_response.data[0]['downvotes']
    else:
        return jsonify({"error": "Comment not found"}), 404

    # Increment downvote count
    new_downvotes = current_downvotes + 1
    update_response = supabase.table('comments').update({'downvotes': new_downvotes}).eq('id', str(comment_id)).execute()
    if update_response.data is None:
        return jsonify({"error": "Failed to update downvotes"}), 400

    print("Comment downvoted:", update_response.data)  # Debugging statement
    flash("Comment downvoted successfully", "success")
    return redirect(url_for('routes.post_page', post_id=comment_id))

@routes_bp.route("/api/posts", methods=["GET"])
def get_all_posts():
    posts = Post.get_all()
    return jsonify(posts), 200

@routes_bp.route("/api/posts/<uuid:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.get_by_id(post_id)
    if post:
        return jsonify(post), 200
    return jsonify({"error": "Post not found"}), 404

@routes_bp.route("/api/posts/<uuid:post_id>/comments", methods=["GET"])
def get_comments(post_id):
    comments = Comment.get_by_post_id(post_id)
    return jsonify(comments), 200

