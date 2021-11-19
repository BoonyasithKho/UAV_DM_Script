#======== Import Library =====================================
import os

def main():
    #======== Input path of all project ==========================
    print("Input Path of Project. (ex. L:01_UAV/00_Data/2021/)")
    rootpath = input("Path : ")+"\\"
    print("")

    #======== Global Variable ====================================

    #======== Get full path in each project ======================
    rootfolder = os.listdir(rootpath)
    fullpath = []

    insidePathDSMUTM = '\\04_Report\\01_DSM_UTM\\'
    insidePathDSMLatLong = '\\04_Report\\02_DSM_LatLong\\'
    insidePathORTUTM = '\\04_Report\\03_Orthophoto_UTM\\'
    insidePathORTLatLong = '\\04_Report\\04_Orthophoto_LatLong\\'
    insidePathPDF = '\\04_Report\\07_PDF\\'

    for projectFolder in rootfolder:
        fullpath.append(rootpath + projectFolder + insidePathDSMUTM)
        fullpath.append(rootpath + projectFolder + insidePathDSMLatLong)
        fullpath.append(rootpath + projectFolder + insidePathORTUTM)
        fullpath.append(rootpath + projectFolder + insidePathORTLatLong)
        fullpath.append(rootpath + projectFolder + insidePathPDF)

    #======== Rename in file of product in Project ==============
    for pathFD in fullpath:
        print(pathFD)
        if not pathFD.startswith("L:\\01_UAV\\00_Data\\2021\\OneNote Table Of Contents.onetoc2\\") :
            folfn = pathFD.split("\\")
            projectNo = folfn[-4].split("_")
            projectNameNo = projectNo[-2]+projectNo[-1]    
            listFNInside = os.listdir(pathFD)

            for fn in listFNInside:
                if fn != "Thumbs.db" :
                    desFNSplit = fn.split("_10cm")
                    getPJNo = desFNSplit[0].split("_")
                    newNameNo = getPJNo[0] + "_" + getPJNo[1] + "_" + getPJNo[2] + "_" + projectNameNo
                    os.rename(pathFD + fn, pathFD + newNameNo + "_10cm" + desFNSplit[1])
                    # print(pathFD + fn,"\n", pathFD + newNameNo + "_10cm" + desFNSplit[1])
    print("Rename Completed...!\n")
    input("Press Enter to continue...")
    
if __name__ == "__main__":
    main()