from flask import request, jsonify
from src.models import Post, Comment
from supabase_client import supabase

def create_post(content, user):
    post_id = supabase.table("posts").insert({"content": content, "user": user, "upvotes": 0, "downvotes": 0}).execute().data[0]['id']
    return Post(id=post_id, content=content, user=user)

def get_posts():
    posts_data = supabase.table("posts").select("*").execute().data
    return [Post(**post).dict() for post in posts_data]

def add_comment(post_id, content, user):
    comment_id = supabase.table("comments").insert({"content": content, "user": user, "post_id": post_id}).execute().data[0]['id']
    return Comment(id=comment_id, content=content, user=user, post_id=post_id)

def get_comments(post_id):
    comments_data = supabase.table("comments").select("*").eq("post_id", post_id).execute().data
    return [Comment(**comment).dict() for comment in comments_data]

def upvote_post(post_id):
    post = supabase.table("posts").select("upvotes").eq("id", post_id).execute().data[0]
    new_upvotes = post['upvotes'] + 1
    supabase.table("posts").update({"upvotes": new_upvotes}).eq("id", post_id).execute()
    return new_upvotes

def downvote_post(post_id):
    post = supabase.table("posts").select("downvotes").eq("id", post_id).execute().data[0]
    new_downvotes = post['downvotes'] + 1
    supabase.table("posts").update({"downvotes": new_downvotes}).eq("id", post_id).execute()
    return new_downvotes