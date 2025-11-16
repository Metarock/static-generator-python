import os
import shutil

# TO DO: create a recursive function to copy all contents
# from static directory to public directory

# 1. It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
def delete_all_contents(directory):
    if os.path.exists(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
# 2. It should copy all files and subdirectories, nested files, etc.
def copy_contents(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)
        if os.path.isdir(src_item):
            copy_contents(src_item, dest_item)
        else:
            shutil.copy2(src_item, dest_item)
            print(f"Copied {src_item} to {dest_item}")
    
# 3. I recommend logging the path of each file you copy, so you can see what's happening as you run and debug your code.

def copy_static_to_public(static_dir='static', public_dir='public'):
    delete_all_contents(public_dir)
    copy_contents(static_dir, public_dir)
    
    print(f"Copied contents from {static_dir} to {public_dir}")
    
    