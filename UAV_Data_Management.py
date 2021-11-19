from osgeo.gdal import Error
import Resize_and_Make_Word
import ORT_downBandandReproject
import DSM_Reproject
import changeFNwithProjectNo
import XML_Create
import word2pdf
import createWorkspace

def show_menu():
    print("\n    UAV and Survey Data in 'โครงการโคก หนอง นา โมเดล'")
    print("=========================================================")
    print("0. Create and Open Work Folder")
    print("1. Resize GNSS Photos and Collect in Word")
    print("2. Convert Word to PDF")
    print("3. Deceasing bands and Reprojection of Orthophoto Product")
    print("4. Reprojection of Digital Surface Model (DSM) Product")
    print("5. Change Filename of Products with Project Number")
    print("6. Create XML for metadata")
    print("7. Exit")
    print("=========================================================")

def start_app():
    try:
        while True:
            show_menu()
            menu_choice = input('Select Menu : ')
            if menu_choice == '0' :
                print("\nCreate Work Folder")
                print("---------------------------------------------------------\n")
                createWorkspace.main()
            elif menu_choice == '1' :
                print("\nResize GNSS Photos and Collect in Word")
                print("---------------------------------------------------------\n")
                Resize_and_Make_Word.main()
            elif menu_choice == '2':
                print("\nConvert Word to PDF")
                print("---------------------------------------------------------\n")
                word2pdf.main()
            elif menu_choice == '3':
                print("\nDeceasing bands and Reprojection of Orthophoto Product")
                print("---------------------------------------------------------\n")
                ORT_downBandandReproject.main()
            elif menu_choice == '4':
                print("\nReprojection of Digital Surface Model (DSM) Product")
                print("---------------------------------------------------------\n")
                DSM_Reproject.main()
            elif menu_choice == '5':
                print("\nChange Filename of Products with Project Number")
                print("---------------------------------------------------------\n")
                changeFNwithProjectNo.main()
            elif menu_choice == '6':
                print("\nCreate XML for metadata")
                print("---------------------------------------------------------\n")
                XML_Create.main() 
            elif menu_choice == '7':
                break
    except (RuntimeError, TypeError, NameError):
        print(Error)

if __name__ == "__main__":
    start_app()