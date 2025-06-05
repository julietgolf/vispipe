import re,os,glob,shutil

def get_example(path=None):
    if path is None:
        path=os.getcwd()

    source_dir=os.path.dirname(os.path.abspath(__file__))
    npz_pattern = os.path.join(source_dir, '*.npz')
    npz_files_to_copy = glob.glob(npz_pattern)
    for npz in npz_files_to_copy:
        shutil.copy2(npz,os.path.join(path,os.path.basename(npz)))

    with open(os.path.join(source_dir,"config.json"),"r") as source_json, open(os.path.join(path,"config.json"),"w") as target_json:
        target_json.write(re.sub(r"%PATH%",path.replace("\\","/"),source_json.read()))
    
get_example()