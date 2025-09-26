from supabase import create_client, Client
import os 
from dotenv import load_dotenv
load_dotenv()
from user import post_data_
url: str = os.getenv('url')
key: str = os.getenv('key')
supabase: Client = create_client(url, key)

def delet_posts():
    try:
        data=post_data_()[-1:]
        for img in ["img1","img2","img3","img4"]:
            to_delete= data[0][img]
            if to_delete is not None:
                response = supabase.storage.from_("images").remove([f"posts/{data[0][img]}"])
        response = supabase.table("lahrour").delete().eq("id",data[0]["id"]).execute()
        return True
    except Exception as e:
        print("Error deleting posts:", e)
        return False

def get_storage_size(bucket_name: str, folder_path: str = ""):
    try:
        files = supabase.storage.from_(bucket_name).list(path=folder_path)
    except Exception as e:
        return e
    total_size = 0
    for file in files:
        size = file.get("metadata", {}).get("size", 0)
        total_size += float(size)
    max_size= 950 * 1024 * 1024  # 950 MB in bytes
    if total_size < max_size:
        return True
    else:
        return delet_posts()

