from pydantic import BaseModel
from typing import List, Optional
from supabase_client import supabase
from uuid import uuid4
from datetime import datetime

class User:
    @staticmethod
    def create(username, email, password):
        user_id = str(uuid4())
        response = supabase.table('users').insert({
            'id': user_id,
            'username': username,
            'email': email,
            'password': password,
            'created_at': datetime.utcnow()
        }).execute()
        print("Supabase response:", response)  # Debugging statement
        return response.data

class Comment(BaseModel):
    id: int
    content: str
    user: str
    post_id: int
    upvotes: int = 0
    downvotes: int = 0

    @staticmethod
    def create(post_id, content, user_id):
        comment_id = str(uuid4())
        created_at = datetime.utcnow().isoformat()
        response = supabase.table('comments').insert({
            'id': comment_id,
            'post_id': post_id,
            'content': content,
            'user_id': user_id,
            'created_at': created_at,
            'upvotes': 0,
            'downvotes': 0
        }).execute()
        return response.data

    @staticmethod
    def get_by_post_id(post_id: int):
        response = supabase.table("comments").select("*").eq("post_id", post_id).execute()
        return response.data

    @staticmethod
    def get_all():
        response = supabase.table('comments').select('*').execute()
        return response.data

    @staticmethod
    def upvote(comment_id, user_id):
        # Check if the user has already upvoted this comment
        existing_vote = supabase.table('comment_votes').select('*').eq('comment_id', comment_id).eq('user_id', user_id).eq('vote_type', 'upvote').execute()
        if existing_vote.data:
            return {"error": "User has already upvoted this comment"}

        # Record the upvote
        vote_id = str(uuid4())
        supabase.table('comment_votes').insert({
            'id': vote_id,
            'user_id': str(user_id),
            'comment_id': str(comment_id),
            'vote_type': 'upvote',
            'created_at': datetime.utcnow().isoformat()
        }).execute()

        # Increment the upvote count
        response = supabase.rpc('increment_comment_upvotes', {'comment_id': str(comment_id)}).execute()
        if response.data:
            return response.data[0]  # Return the first comment object
        return {"error": "Failed to upvote comment"}

    @staticmethod
    def downvote(comment_id, user_id):
        # Check if the user has already downvoted this comment
        existing_vote = supabase.table('comment_votes').select('*').eq('comment_id', comment_id).eq('user_id', user_id).eq('vote_type', 'downvote').execute()
        if existing_vote.data:
            return {"error": "User has already downvoted this comment"}

        # Record the downvote
        vote_id = str(uuid4())
        supabase.table('comment_votes').insert({
            'id': vote_id,
            'user_id': str(user_id),
            'comment_id': str(comment_id),
            'vote_type': 'downvote',
            'created_at': datetime.utcnow().isoformat()
        }).execute()

        # Increment the downvote count
        response = supabase.rpc('increment_comment_downvotes', {'comment_id': str(comment_id)}).execute()
        if response.data:
            return response.data[0]  # Return the first comment object
        return {"error": "Failed to downvote comment"}

class Post(BaseModel):
    id: int
    content: str
    user: str
    upvotes: int = 0
    downvotes: int = 0
    comments: List[Comment] = []

    @staticmethod
    def create(content, user_id):
        post_id = str(uuid4())
        created_at = datetime.utcnow().isoformat()
        if user_id == "anonymous":
            user_id = str(uuid4())  # Generate a UUID for anonymous users
        response = supabase.table('posts').insert({
            'id': post_id,
            'content': content,
            'user_id': user_id,
            'created_at': created_at,
            'upvotes': 0,
            'downvotes': 0
        }).execute()
        return response.data

    @staticmethod
    def get_all():
        response = supabase.table('posts').select('*').order('upvotes', desc=True).execute()
        print("Supabase response:", response)  # Debugging statement
        return response.data

    @staticmethod
    def get_by_id(post_id: int):
        response = supabase.table('posts').select('*').eq('id', post_id).execute()
        print("Supabase response:", response)  # Debugging statement
        if response.data:
            return response.data[0]  # Return the first post object
        return None

    @staticmethod
    def upvote(post_id: int, user_id):
        # Check if the user has already upvoted this post
        existing_vote = supabase.table('post_votes').select('*').eq('post_id', post_id).eq('user_id', user_id).eq('vote_type', 'upvote').execute()
        if existing_vote.data:
            return {"error": "User has already upvoted this post"}

        # Record the upvote
        vote_id = str(uuid4())
        supabase.table('post_votes').insert({
            'id': vote_id,
            'user_id': str(user_id),
            'post_id': str(post_id),
            'vote_type': 'upvote',
            'created_at': datetime.utcnow().isoformat()
        }).execute()

        # Increment the upvote count
        response = supabase.rpc('increment_upvotes', {'post_id': str(post_id)}).execute()
        if response.data:
            return response.data[0]  # Return the first post object
        return {"error": "Failed to upvote post"}

    @staticmethod
    def downvote(post_id: int, user_id):
        # Check if the user has already downvoted this post
        existing_vote = supabase.table('post_votes').select('*').eq('post_id', post_id).eq('user_id', user_id).eq('vote_type', 'downvote').execute()
        if existing_vote.data:
            return {"error": "User has already downvoted this post"}

        # Record the downvote
        vote_id = str(uuid4())
        supabase.table('post_votes').insert({
            'id': vote_id,
            'user_id': str(user_id),
            'post_id': str(post_id),
            'vote_type': 'downvote',
            'created_at': datetime.utcnow().isoformat()
        }).execute()

        # Increment the downvote count
        response = supabase.rpc('increment_downvotes', {'post_id': str(post_id)}).execute()
        if response.data:
            return response.data[0]  # Return the first post object
        return {"error": "Failed to downvote post"}