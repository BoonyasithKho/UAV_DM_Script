#======== Import Library =====================================
from osgeo import gdal
import os
import shutil

def main():
    #======== Input path of all project ==========================
    print("Input Path of Project. (ex. L:01_UAV/00_Data/2021/)")
    rootpath = input("Path : ")+"\\"
    print("")

    #======== Global Variable ====================================

    #======== Get full path in each project ======================
    rootfolder = os.listdir(rootpath)
    fullpathSource = []
    fullpathDestination = []

    insidePathSourceDSM = '\\04_Report\\01_DSM_UTM\\'
    insidePathDestinationDSM = '\\04_Report\\02_DSM_LatLong\\'

    for projectFolder in rootfolder:
        fullpathSource.append(rootpath + projectFolder + insidePathSourceDSM)
        fullpathDestination.append(rootpath + projectFolder + insidePathDestinationDSM)

    #======== Reprojection file of DSM in Project ================
    for i in range(len(fullpathSource)):
        listFNInside = os.listdir(fullpathSource[i])
        for fn in listFNInside:
            sourceFN = fullpathSource[i]+fn
            destinationFN = fullpathDestination[i]+fn
            if fn.endswith(".prj") or fn.endswith(".tfw"):
                shutil.copy(sourceFN, destinationFN)
                    
            elif fn.endswith(".tif"):
                ds = gdal.Open(sourceFN)
                ds = gdal.Warp(destinationFN,ds,dstSRS='EPSG:4326')
                ds = None
                print(fn + " --> Reprojection Successfully!!")

    input("Press Enter to continue...")

if __name__ == "__main__":
    main()