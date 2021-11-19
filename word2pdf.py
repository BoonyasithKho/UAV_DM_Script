#======== Import Library =====================================
import os, shutil
from docx2pdf import convert

def main():
    #======== Input path of all project ==========================
    print("Input Path of Project. (ex. D:_Work/_LSS/01_UAV/03_Project/โคก หนอง นา/_Round_06/)")
    input_path = input("Path : ")
    print("")

    #======== Global Variable ====================================
    photo_path = input_path +"\\Output\\"
    os.mkdir(input_path + "\\PDF\\")
    target_Path = input_path + "\\PDF\\"

    #======== Convert Word 2 PDF =================================
    # dirss = os.listdir(photo_path)
    print("\nConverting...\n")
    
    convert(photo_path,target_Path)
    # convert("C:\\Users\\vap\\Downloads\\NPT\\Output\\ภาพประกอบจุดรังวัด แปลง NPT5.docx","C:\\Users\\vap\\Downloads\\NPT\\PDF\\ภาพประกอบจุดรังวัด_แปลง_NPT5.pdf")

if __name__ == "__main__":
    main()