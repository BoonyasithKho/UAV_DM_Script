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
    os.mkdir("D:\\Buffer\\")
    buffer_Path = "D:\\Buffer\\"

    #======== Get full path in each project ======================
    rootfolder = os.listdir(rootpath)
    fullpathSource = []
    fullpathDestination = []

    insidePathSourceDSM = '\\04_Report\\03_Orthophoto_UTM\\'
    insidePathDestinationDSM = '\\04_Report\\04_Orthophoto_LatLong\\'

    for projectFolder in rootfolder:
        fullpathSource.append(rootpath + projectFolder + insidePathSourceDSM)
        fullpathDestination.append(rootpath + projectFolder + insidePathDestinationDSM)

    #======== Down Bands and Reprojection Orthophoto file ========
    for i in range(len(fullpathSource)):
        listFNInside = os.listdir(fullpathSource[i])
        for fn in listFNInside:
            sourceFN = fullpathSource[i]+fn
            destinationFN = fullpathDestination[i]+fn
            if fn.endswith(".prj") or fn.endswith(".tfw"):
                shutil.copy(sourceFN, destinationFN)
            elif fn.endswith(".tif"):
                buff = r'D:/Buffer/buff.tif'
                ds = gdal.Open(os.path.abspath(sourceFN))
                ds = gdal.Translate(buff, ds , bandList=[1,2,3])
                shutil.copy(buff, sourceFN)
                ds = None
                # print(fn + " --> Decrease Bands Successfully!!")
                es = gdal.Open(buff)
                es = gdal.Warp(destinationFN,es,dstSRS='EPSG:4326')
                es = None
                os.remove(buff)
                print(fn + " --> Decrease Bands and Reprojection Successfully!!")
    
    shutil.rmtree(buffer_Path)
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()