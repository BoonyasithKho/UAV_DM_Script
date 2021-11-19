#======== Import Library =====================================
import os

def main():
    #======== Directory ==========================
    directory = "Work_Folder/"
    sub_dir = "Photo"
    #======== Parent Directory path ==============
    parent_dir = "D:/"
    
    #======== Path ===============================
    path = os.path.join(parent_dir, directory)
    sub_path = os.path.join(path, sub_dir)
    
    #======== Create the directory ===============
    try:
        os.makedirs(path, exist_ok = True)
        os.mkdir(sub_path)        
        print("Directory '%s' created successfully" % directory)
        os.startfile(path)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)
        os.startfile(path)

if __name__ == "__main__":
    main()