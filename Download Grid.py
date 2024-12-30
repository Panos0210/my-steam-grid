import os, urllib.request, zipfile, shutil

repo = 'https://github.com/Panos0210/my-steam-grid/archive/refs/heads/main.zip'
output = 'grid.zip'
userdata_path = r"C:\Program Files (x86)\Steam\userdata"

print('Downloading Grid...')
urllib.request.urlretrieve(repo, output)

print('Extracting Grid...')
with zipfile.ZipFile(output, 'r') as zip_ref:
    zip_ref.extractall("extracted_repo") 

config_folder_path = os.path.join("extracted_repo", "my-steam-grid-main", "config")
if not os.path.exists(config_folder_path):
    print("Error: 'config' folder not found in the extracted ZIP!")
    exit(1)

for folder_name in os.listdir(userdata_path):
    folder_path = os.path.join(userdata_path, folder_name)
    if os.path.isdir(folder_path) and folder_name.isdigit():  
        dest_path = os.path.join(folder_path, "config")
        shutil.copytree(config_folder_path, dest_path, dirs_exist_ok=True)
        print(f"Copied 'config' folder to: {dest_path}")

shutil.rmtree("extracted_repo")
os.remove(output) 
print("Cleanup complete. All done!")