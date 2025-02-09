from pydantic import BaseModel
from typing import List
from supabase_client import supabase

class Post(BaseModel):
    id: int
    content: str
    user: str
    upvotes: int = 0
    downvotes: int = 0
    comments: List[dict] = []

    @staticmethod
    def create(content: str, user: str):
        response = supabase.table("posts").insert({"content": content, "user": user}).execute()
        return response.data

    @staticmethod
    def get_all():
        response = supabase.table("posts").select("*").execute()
        return response.data

    @staticmethod
    def upvote(post_id: int):
        response = supabase.table("posts").update({"upvotes": supabase.table("posts").select("upvotes").eq("id", post_id).execute()[0]["upvotes"] + 1}).eq("id", post_id).execute()
        return response.data

    @staticmethod
    def downvote(post_id: int):
        response = supabase.table("posts").update({"downvotes": supabase.table("posts").select("downvotes").eq("id", post_id).execute()[0]["downvotes"] + 1}).eq("id", post_id).execute()
        return response.data

class Comment(BaseModel):
    id: int
    content: str
    user: str
    post_id: int

    @staticmethod
    def create(content: str, user: str, post_id: int):
        response = supabase.table("comments").insert({"content": content, "user": user, "post_id": post_id}).execute()
        return response.data

    @staticmethod
    def get_by_post_id(post_id: int):
        response = supabase.table("comments").select("*").eq("post_id", post_id).execute()
        return response.data