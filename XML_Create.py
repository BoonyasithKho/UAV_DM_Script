#-------------------------------------------------------------------------------
#   Import Library
#-------------------------------------------------------------------------------
# from os import SEEK_SET
from osgeo import gdal, osr
from pathlib import Path
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import datetime, pytz, sys, os

#-------------------------------------------------------------------------------
# Global Parameter
#-------------------------------------------------------------------------------
__names__ = "นายรัฐวัชร์ วสุหิรัณยฤทธิ์"
__position__ = "รักษาการหัวหน้าฝ่ายระบบสำรวจภาคพื้นพิภพ"
__voiceNo__ = "+66 (0) 2141-4636"
__facNo__ = "+66 (0) 2143-9596"
__organisation__ = "สำนักงานพัฒนาเทคโนโลยีอวกาศและภูมิสารสนเทศ (องค์การมหาชน)"
__address__ = "ศูนย์ราชการเฉลิมพระเกียรติ 80 พรรษา 5 ธันวาคม 2550 เลขที่ 120  ถนนแจ้งวัฒนะ  แขวงทุ่งสองห้อง  เขตหลักสี่"
__city__ = "กรุงเทพ"
__postcode__ = "10210"
__email__ = "lss@gistda.or.th"
__abstract__ = "ผลิตภัณฑ์จากภาพถ่ายทางอากาศด้วยอากาศยานไร้คนขับ (UAV) ที่ผ่านการประมวลผล เพื่อสร้างข้อมูลภาพ Orthophoto ข้อมูลโมเดลความสูงเชิงเลข ซึ่งมีความถูกต้องและสามารถนำไปใช้งานร่วมกับข้อมูลภูมิสารสนเทศอื่นๆ ได้"
__purpose__ = "เพื่อใช้สนับสนุนในโครงการพัฒนาพื้่นที่ต้นแบบการพัฒนาคุณภาพชีวิตตามหลักทฤษฎี ประยุกต์สู่ โคก หนอง นา โมเดล กิจกรรมการจัดหาภาพถ่ายทางอากาศจากอากาศยานไร้คนขับ (UAV)"
__distributionDate__ = "2021-09-30"

#-------------------------------------------------------------------------------
# Global Parameter
#-------------------------------------------------------------------------------
spHD = ['http://www.isotc211.org/2005/gmi','http://www.isotc211.org/2005/gmx','http://www.isotc211.org/2005/gsr','http://www.isotc211.org/2005/gss','http://www.isotc211.org/2005/gts','http://www.opengis.net/gml/3.2','http://www.w3.org/2001/XMLSchema-instance','http://purl.org/dc/elements/1.1/','http://inspire.ec.europa.eu/schemas/common/1.0','http://www.w3.org/2005/Atom','http://www.w3.org/2001/XMLSchema','http://purl.org/dc/terms/','http://www.opengis.net/ows','http://www.opengis.net/cat/csw/apiso/1.0','http://gcmd.gsfc.nasa.gov/Aboutus/xml/dif/','http://www.w3.org/1999/xlink','http://www.isotc211.org/2005/gco','http://www.isotc211.org/2005/gmd','http://www.w3.org/1999/02/22-rdf-syntax-ns#','http://www.isotc211.org/2005/srv','http://www.opengis.net/ogc','http://www.opengis.net/cat/csw/csdgm','http://inspire.ec.europa.eu/schemas/inspire_ds/1.0','http://www.opengis.net/cat/csw/2.0.2','http://a9.com/-/spec/opensearch/1.1/','http://www.w3.org/2003/05/soap-envelope','http://www.sitemaps.org/schemas/sitemap/0.9','http://www.isotc211.org/2005/gmi http://www.ngdc.noaa.gov/metadata/published/xsd/schema.xsd','http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode','http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode','http://www.isotc211.org/2005/resources/Codelist/ML_gmxCodelists.xml#LanguageCode','http://www.isotc211.org/2005/resources/Codelist/ML_gmxCodelists.xml#Country','http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_DimensionNameTypeCode','http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CellGeometryCode','http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode','http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_PresentationFormCode','http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ProgressCode','http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_MaintenanceFrequencyCode','http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_KeywordTypeCode','http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_SpatialRepresentationTypeCode','http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CoverageContentTypeCode','http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ImagingConditionCode','http://www.opengis.net/def/crs/EPSG/0/']

#-------------------------------------------------------------------------------
#   FN : Main funtion
#-------------------------------------------------------------------------------
def main():
    dataFN = readFileName()
    # #======== Rename in file of product in Project ==============
    for pathFD in dataFN:
        if not pathFD.startswith("L:\\01_UAV\\00_Data\\2021\\OneNote Table Of Contents.onetoc2\\") :
            folfn = pathFD.split("\\")
            listFNInside = os.listdir(pathFD)

            for fn in listFNInside:
                if fn.endswith(".tif") :
                    dsss = gdal.Open(pathFD+fn)
                    fname = Path(fn).stem
                    cornerPoint = getCornerPoint(dsss)
                    srs = getProjections(dsss)
                    numOfBand = chkband(dsss)
                    xmlData = createXML(cornerPoint,fname,srs,numOfBand)
                    output_file = open(pathFD+fname+'.xml', 'w') #สร้างไฟล์ตามชื่อข้อมูลในรูปแบบไฟล์ .xml
                    output_file.write('<?xml version="1.0" encoding="UTF-8"?>\n') #เพิ่มส่วนหัว xml
                    output_file.write(ElementTree.tostring(xmlData).decode('utf-8')) #เขียนไฟล์ xml จากข้อมูลที่กำหนด โดยข้อมูลที่ได้จะเป็น bytes ต้องแปลงให้เป็น str ด้วย decode
                    output_file.close()
                    print(fn+" was created successfully.")
    input("Press Enter to continue...")

#-------------------------------------------------------------------------------
#   FN : Get file in each folder
#-------------------------------------------------------------------------------
def readFileName():
    '''
        Return filename in full path
        @rtype:     C{osgeo.gdal.Dataset} and C{str}
        @return:    fullpath of file
    '''
    #======== Input path of all project ==========================
    print("Input Path of Project. (ex. L:01_UAV/00_Data/2021)")
    rootpath = input("Path : ")+"\\"

    #======== Get full path in each project ======================
    rootfolder = os.listdir(rootpath)
    fullpath = []

    insidePathDSMUTM = '\\04_Report\\01_DSM_UTM\\'
    insidePathDSMLatLong = '\\04_Report\\02_DSM_LatLong\\'
    insidePathORTUTM = '\\04_Report\\03_Orthophoto_UTM\\'
    insidePathORTLatLon = '\\04_Report\\04_Orthophoto_LatLong\\'

    for projectFolder in rootfolder:
        fullpath.append(rootpath + projectFolder + insidePathDSMUTM)
        fullpath.append(rootpath + projectFolder + insidePathDSMLatLong)
        fullpath.append(rootpath + projectFolder + insidePathORTUTM)
        fullpath.append(rootpath + projectFolder + insidePathORTLatLon)

    return fullpath

#-------------------------------------------------------------------------------
#   FN : Get extent of data
#-------------------------------------------------------------------------------
def getExtent(gt,cols,rows):
    '''
        Return list of corner coordinates from a geotransform
        @type gt:    C{tuple/list}
        @param gt:   geotransform
        @type cols:  C{int}
        @param cols: number of columns in the dataset
        @type rows:  C{int}
        @param rows: number of rows in the dataset
        @rtype:      C{[float,...,float]}
        @return:     coordinates of each corner
    '''
    ext = []
    xarr = [0,cols]
    yarr = [0,rows]

    for px in xarr:
        for py in yarr:
            x = gt[0] + (px*gt[1]) + (py*gt[2])
            y = gt[3] + (px*gt[4]) + (py*gt[5])
            ext.append([x,y])
        yarr.reverse()
    return ext

#-------------------------------------------------------------------------------
#   FN : Get Position of Conner Point of DATA (Upper Left point and Lower Right point)
#-------------------------------------------------------------------------------
def getCornerPoint(ds):
    ''' 
        Return list of corner extent point
        @type ds:   C{tuple/list}
        @param ds:  List of [[x,y],...[x,y]] coordinates
        @rtype:     C{tuple/list}
        @return:    List of corner point [[x,y],...[x,y]] coordinates
    '''
    gt = ds.GetGeoTransform()
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    ext = getExtent(gt,cols,rows)

    U_L = ext[0]
    L_R = ext[2]
    return U_L[0],U_L[1],L_R[0],L_R[1],cols,rows

#-------------------------------------------------------------------------------
#   FN : Get projection code of input data
#-------------------------------------------------------------------------------
def getProjections(dn):
    ''' 
        Return projection code of input data
        @type ds:   C{tuple/list}
        @param ds:  List of [[x,y],...[x,y]] coordinates
        @rtype:     C{int}
        @return:    Projection code of input data
    '''
    sPro = dn.GetProjection()
    srs = osr.SpatialReference(wkt=sPro)
    if not srs.GetAttrValue('projcs'):
        projectionSystem = 4326
    else:
        ckPro = srs.GetAttrValue('projcs')
        checkProj = ckPro.split(" / ")
        if checkProj[1] == 'UTM zone 47N':
            projectionSystem = 32647
        else:
            projectionSystem = 32648
    return projectionSystem

#-------------------------------------------------------------------------------
#   FN : Counting bands(layer) of image
#-------------------------------------------------------------------------------
def chkband(ds):
    ''' 
        Return number of image bands
        @type ds:   C{tuple/list}
        @param ds:  List of [[x,y],...[x,y]] coordinates
        @rtype:     C{int}
        @return:    number of counting bands
    '''
    if ds is not None:
        cBand = ds.RasterCount
    return cBand

#-------------------------------------------------------------------------------
#   FN : Make XML File and return Data XML
#-------------------------------------------------------------------------------
def createXML(cnP,fname,srsCode,bands):
    ''' 
        Return metadata of input dataset
        @type hd:       C{str}
        @param hd:      header of XML and XML tags
        @type cnP:      C{tuple/list}
        @param cnP:     List of corner point and number of columns and rows
        @type fname:    C{str}
        @param fname:   filename without file extension
        @type srsCode:  C{int}
        @param srsCode: code of projection
        @rtype:         C{xml.etree.ElementTree.Element}
        @return:        Metadata in xml element tree
    '''
    # spHD = hd.split('\n')
    data = Element('gmi:MI_Metadata')
    data.set('xmlns:gmi',spHD[0])
    data.set('xmlns:gmx',spHD[1])
    data.set('xmlns:gsr',spHD[2])
    data.set('xmlns:gss',spHD[3])
    data.set('xmlns:gts',spHD[4])
    data.set('xmlns:gml',spHD[5])
    data.set('xmlns:xsi',spHD[6])
    data.set('xmlns:dc',spHD[7])
    data.set('xmlns:inspire_common',spHD[8])
    data.set('xmlns:atom',spHD[9])
    data.set('xmlns:xs',spHD[10])
    data.set('xmlns:dct',spHD[11])
    data.set('xmlns:ows',spHD[12])
    data.set('xmlns:apiso',spHD[13])
    data.set('xmlns:dif',spHD[14])
    data.set('xmlns:xlink',spHD[15])
    data.set('xmlns:gco',spHD[16])
    data.set('xmlns:gmd',spHD[17])
    data.set('xmlns:rdf',spHD[18])
    data.set('xmlns:srv',spHD[19])
    data.set('xmlns:ogc',spHD[20])
    data.set('xmlns:fgdc',spHD[21])
    data.set('xmlns:inspire_ds',spHD[22])
    data.set('xmlns:csw',spHD[23])
    data.set('xmlns:os',spHD[24])
    data.set('xmlns:soapenv',spHD[25])
    data.set('xmlns:sitemap',spHD[26])
    data.set('xsi:schemaLocation',spHD[27])

    se1 = SubElement(data,'gmd:fileIdentifier')
    se2 = SubElement(se1,'gco:CharacterString')
    se2.text = '00000000-0000-0000-0000-000000000000'

    se1 = SubElement(data,'gmd:language')
    se2 = SubElement(se1,'gco:CharacterString')
    se2.text = 'tha'

    se1 = SubElement(data,'gmd:characterSet')
    se2 = SubElement(se1,'gmd:MD_CharacterSetCode')
    se2.set('codeList',spHD[28])
    se2.set('codeListValue','utf8')
    se2.text = 'UTF 8'

    se1 = SubElement(data,'gmd:contact')
    se2 = SubElement(se1,'gmd:CI_ResponsibleParty')
    se3 = SubElement(se2,'gmd:individualName')
    se4 = SubElement(se3,'gco:CharacterString')
    se4.text = __names__
    se3 = SubElement(se2,'gmd:organisationName')
    se4 = SubElement(se3,'gco:CharacterString')
    se4.text = __organisation__
    se3 = SubElement(se2,'gmd:positionName')
    se4 = SubElement(se3,'gco:CharacterString')
    se4.text = __position__
    se3 = SubElement(se2,'gmd:contactInfo')
    se4 = SubElement(se3,'gmd:CI_Contact')
    se5 = SubElement(se4,'gmd:phone')
    se6 = SubElement(se5,'gmd:CI_Telephone')
    se7 = SubElement(se6,'gmd:voice')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = __voiceNo__
    se7 = SubElement(se6,'gmd:facsimile')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = __facNo__
    se5 = SubElement(se4,'gmd:address')
    se6 = SubElement(se5,'gmd:CI_Address')
    se7 = SubElement(se6,'gmd:deliveryPoint')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = __address__
    se7 = SubElement(se6,'gmd:city')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = __city__
    se7 = SubElement(se6,'gmd:administrativeArea')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = __city__
    se7 = SubElement(se6,'gmd:postalCode')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = __postcode__
    se7 = SubElement(se6,'gmd:country')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = "ประเทศไทย"
    se7 = SubElement(se6,'gmd:electronicMailAddress')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = __email__
    se5 = SubElement(se4,'gmd:onlineResource')
    se6 = SubElement(se5,'gmd:CI_OnlineResource')
    se7 = SubElement(se6,'gmd:linkage')
    se8 = SubElement(se7,'gmd:URL')
    se7 = SubElement(se6,'gmd:protocol')
    se8 = SubElement(se7,'gco:CharacterString')
    se7 = SubElement(se6,'gmd:name')
    se8 = SubElement(se7,'gco:CharacterString')
    se7 = SubElement(se6,'gmd:description')
    se8 = SubElement(se7,'gco:CharacterString')
    se5 = SubElement(se4,'gmd:hoursOfService')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = "8:30 - 16:30"
    se5 = SubElement(se4,'gmd:contactInstructions')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = "Please make appointment."
    se3 = SubElement(se2,'gmd:role')
    se4 = SubElement(se3,'gmd:CI_RoleCode')
    se4.set('codeList',spHD[29])
    se4.set('codeListValue','resourceProvider')

    se1 = SubElement(data,'gmd:dateStamp')
    se2 = SubElement(se1,'gco:DateTime')
    se2.set('xmlns:gmx',spHD[1])
    se2.set('xmlns:srv',spHD[19])
    se2.text = datetime.datetime.now(pytz.timezone('Asia/Bangkok')).isoformat()

    se1 = SubElement(data,'gmd:metadataStandardName')
    se2 = SubElement(se1,'gco:CharacterString')
    se2.text = "ISO 19115-2 Geographic Information - Metadata Part 2 Extensions for imagery and gridded data"

    se1 = SubElement(data,'gmd:metadataStandardVersion')
    se2 = SubElement(se1,'gco:CharacterString')
    se2.text = "ISO 19115-2:2009(E)"

    se1 = SubElement(data,'gmd:locale')
    se2 = SubElement(se1,'gmd:PT_Locale')
    se3 = SubElement(se2,'gmd:languageCode')
    se4 = SubElement(se3,'gmd:LanguageCode')
    se4.set('codeList',spHD[30])
    se4.set('codeListValue','eng')
    se3 = SubElement(se2,'gmd:country')
    se4 = SubElement(se3,'gmd:Country')
    se4.set('codeList',spHD[31])
    se4.set('codeListValue','USA')    
    se3 = SubElement(se2,'gmd:characterEncoding')
    se4 = SubElement(se3,'gmd:MD_CharacterSetCode')
    se4.set('codeList',spHD[28])
    se4.set('codeListValue','utf8')
    se4.text = 'UTF 8'

    se1 = SubElement(data,'gmd:locale')
    se2 = SubElement(se1,'gmd:PT_Locale')
    se3 = SubElement(se2,'gmd:languageCode')
    se4 = SubElement(se3,'gmd:LanguageCode')
    se4.set('codeList',spHD[30])
    se4.set('codeListValue','tha')
    se3 = SubElement(se2,'gmd:country')
    se4 = SubElement(se3,'gmd:Country')
    se4.set('codeList',spHD[31])
    se4.set('codeListValue','Thailand')    
    se3 = SubElement(se2,'gmd:characterEncoding')
    se4 = SubElement(se3,'gmd:MD_CharacterSetCode')
    se4.set('codeList',spHD[28])
    se4.set('codeListValue','utf8')
    se4.text = 'UTF 8'

    se1 = SubElement(data,'gmd:spatialRepresentationInfo')
    se2 = SubElement(se1,'gmi:MI_Georectified')
    se3 = SubElement(se2,'gmd:numberOfDimensions')
    se4 = SubElement(se3,'gco:Integer')
    se4.text = "2"
    se3 = SubElement(se2,'gmd:axisDimensionProperties')
    se4 = SubElement(se3,'gmd:MD_Dimension')
    se5 = SubElement(se4,'gmd:dimensionName')
    se6 = SubElement(se5,'gmd:MD_DimensionNameTypeCode')
    se6.set('codeList',spHD[32])
    se6.set('codeListValue','row')
    se5 = SubElement(se4,'gmd:dimensionSize')
    se6 = SubElement(se5,'gco:Integer')
    se6.text = str(cnP[5])
    se3 = SubElement(se2,'gmd:axisDimensionProperties')
    se4 = SubElement(se3,'gmd:MD_Dimension')
    se5 = SubElement(se4,'gmd:dimensionName')
    se6 = SubElement(se5,'gmd:MD_DimensionNameTypeCode')
    se6.set('codeList',spHD[32])
    se6.set('codeListValue','column')
    se5 = SubElement(se4,'gmd:dimensionSize')
    se6 = SubElement(se5,'gco:Integer')
    se6.text = str(cnP[4])
    se3 = SubElement(se2,'gmd:cellGeometry')
    se4 = SubElement(se3,'gmd:MD_CellGeometryCode')
    se4.set('codeListValue','area')
    se4.set('codeList',spHD[33])
    se3 = SubElement(se2,'gmd:transformationParameterAvailability')
    se4 = SubElement(se3,'gco:Boolean')
    se4.text = "0"
    se3 = SubElement(se2,'gmd:checkPointAvailability')
    se4 = SubElement(se3,'gco:Boolean')
    se4.text = "0"
    se3 = SubElement(se2,'gmd:cornerPoints')
    se4 = SubElement(se3,'gml:Point')
    se4.set('gml:id','gistda9')
    se5 = SubElement(se4,'gml:description')
    se5.text = "gistda"
    se5 = SubElement(se4,'gml:identifier')
    se5.set('codeSpace','SI')
    se5.text = "meters"
    se5 = SubElement(se4,'gml:name')
    se5.text = "gistda"
    se5 = SubElement(se4,'gml:pos')
    se5.set('srsName',spHD[42]+str(srsCode))
    se5.text = str(cnP[0])+" "+str(cnP[1])
    se3 = SubElement(se2,'gmd:cornerPoints')
    se4 = SubElement(se3,'gml:Point')
    se4.set('gml:id','gistda9')
    se5 = SubElement(se4,'gml:description')
    se5.text = "gistda"
    se5 = SubElement(se4,'gml:identifier')
    se5.set('codeSpace','SI')
    se5.text = "meters"
    se5 = SubElement(se4,'gml:name')
    se5.text = "gistda"
    se5 = SubElement(se4,'gml:pos')
    se5.set('srsName',spHD[42]+str(srsCode))
    se5.text = str(cnP[2])+" "+str(cnP[3])
    se3 = SubElement(se2,'gmd:pointInPixel')
    se4 = SubElement(se3,'gmd:MD_PixelOrientationCode')
    se4.text = 'upperleft'

    se1 = SubElement(data,'gmd:referenceSystemInfo')
    se2 = SubElement(se1,'gmd:MD_ReferenceSystem')
    se3 = SubElement(se2,'gmd:referenceSystemIdentifier')
    se4 = SubElement(se3,'gmd:RS_Identifier')
    se5 = SubElement(se4,'gmd:code')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = "WGS 1984"

    se1 = SubElement(data,'gmd:identificationInfo')
    se2 = SubElement(se1,'gmd:MD_DataIdentification')
    se3 = SubElement(se2,'gmd:citation')
    se3 = SubElement(se2,'gmd:CI_Citation')
    se4 = SubElement(se3,'gmd:title')
    se5 = SubElement(se4,'gco:CharacterString')
    se5.text = "รูปแบบคำอธิบายข้อมูลสำหรับข้อมูลเชิงภาพ (Raster)"

    dateFile = fname.split('_')
    __createDate__ = dateFile[1]

    se4 = SubElement(se3,'gmd:date')
    se5 = SubElement(se4,'gmd:CI_date')
    se6 = SubElement(se5,'gmd:date')
    se7 = SubElement(se6,'gco:Date')
    se7.text = __createDate__[0:4]+"-"+__createDate__[4:6]+"-"+__createDate__[6:8]
    se6 = SubElement(se5,'gmd:dateType')
    se7 = SubElement(se6,'gmd:CI_DateTypeCode')
    se7.set('codeListValue','creation')
    se7.set('codeList',spHD[34])
    se4 = SubElement(se3,'gmd:date')
    se5 = SubElement(se4,'gmd:CI_date')
    se6 = SubElement(se5,'gmd:date')
    se7 = SubElement(se6,'gco:Date')
    se7.text = __createDate__[0:4]+"-"+__createDate__[4:6]+"-"+__createDate__[6:8]
    se6 = SubElement(se5,'gmd:dateType')
    se7 = SubElement(se6,'gmd:CI_DateTypeCode')
    se7.set('codeListValue','revision')
    se7.set('codeList',spHD[34])
    se4 = SubElement(se3,'gmd:edition')
    se5 = SubElement(se4,'gco:CharacterString')
    se5.text = "1"
    se4 = SubElement(se3,'gmd:presentationForm')
    se5 = SubElement(se4,'gmd:CI_PresentationFormCode')
    se5.set('codeListValue','imageDigital')
    se5.set('codeList',spHD[35])
    se3 = SubElement(se2,'gmd:abstract')
    se4 = SubElement(se3,'gco:CharacterString')
    se4.text = __abstract__
    se3 = SubElement(se2,'gmd:purpose')
    se4 = SubElement(se3,'gco:CharacterString')
    se4.text = __purpose__
    se3 = SubElement(se2,'gmd:status')
    se4 = SubElement(se3,'gmd:MD_ProgressCode')
    se4.set('codeListValue','historicalArchive')
    se4.set('codeList',spHD[36])
    se3 = SubElement(se2,'gmd:pointOfContact')
    se4 = SubElement(se3,'gmd:CI_ResponsibleParty')
    se5 = SubElement(se4,'gmd:individualName')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = __names__
    se5 = SubElement(se4,'gmd:organisationName')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = __organisation__
    se5 = SubElement(se4,'gmd:positionName')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = __position__
    se5 = SubElement(se4,'gmd:contactInfo')
    se6 = SubElement(se5,'gmd:CI_Contact')
    se7 = SubElement(se6,'gmd:phone')
    se8 = SubElement(se7,'gmd:CI_Telephone')
    se9 = SubElement(se8,'gmd:voice')
    se10 = SubElement(se9,'gco:CharacterString')
    se10.text = __voiceNo__
    se9 = SubElement(se8,'gmd:facsimile')
    se10 = SubElement(se9,'gco:CharacterString')
    se10.text = __facNo__
    se7 = SubElement(se6,'gmd:address')
    se8 = SubElement(se7,'gmd:CI_Address')
    se9 = SubElement(se8,'gmd:deliveryPoint')
    se10 = SubElement(se9,'gco:CharacterString')
    se10.text = __address__
    se9 = SubElement(se8,'gmd:city')
    se10 = SubElement(se9,'gco:CharacterString')
    se10.text = __city__
    se9 = SubElement(se8,'gmd:administrativeArea')
    se10 = SubElement(se9,'gco:CharacterString')
    se10.text = __city__
    se9 = SubElement(se8,'gmd:postalCode')
    se10 = SubElement(se9,'gco:CharacterString')
    se10.text = __postcode__
    se9 = SubElement(se8,'gmd:country')
    se10 = SubElement(se9,'gco:CharacterString')
    se10.text = "ประเทศไทย"
    se9 = SubElement(se8,'gmd:electronicMailAddress')
    se10 = SubElement(se9,'gco:CharacterString')
    se10.text = __email__
    se7 = SubElement(se6,'gmd:onlineResource')
    se8 = SubElement(se7,'gmd:CI_OnlineResource')
    se9 = SubElement(se8,'gmd:linkage')
    se10 = SubElement(se9,'gmd:URL')
    se9 = SubElement(se8,'gmd:protocol')
    se10 = SubElement(se9,'gco:CharacterString')
    se9 = SubElement(se8,'gmd:name')
    se10 = SubElement(se9,'gco:CharacterString')
    se9 = SubElement(se8,'gmd:description')
    se10 = SubElement(se9,'gco:CharacterString')
    se7 = SubElement(se6,'gmd:hoursOfService')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = "8:30 - 16:30"
    se7 = SubElement(se6,'gmd:contactInstructions')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = "Please make appointment."
    se5 = SubElement(se4,'gmd:role')
    se6 = SubElement(se5,'gmd:CI_RoleCode')
    se6.set('codeList',spHD[29])
    se6.set('codeListValue','resourceProvider')
    se3 = SubElement(se2,'gmd:resourceMaintenance')
    se4 = SubElement(se3,'gmd:MD_MaintenanceInformation')
    se5 = SubElement(se4,'gmd:maintenanceAndUpdateFrequency')
    se6 = SubElement(se5,'gmd:MD_MaintenanceFrequencyCode')
    se6.set('codeListValue','notPlanned')
    se6.set('codeList',spHD[37])
    se3 = SubElement(se2,'gmd:graphicOverview')
    se4 = SubElement(se3,'gmd:MD_BrowseGraphic')
    se5 = SubElement(se4,'gmd:fileName')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = fname
    se5 = SubElement(se4,'gmd:fileDescription')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = "UAV_yyyymmdd_yyyymmdd_fieldname_res_order_producttype"
    se5 = SubElement(se4,'gmd:fileType')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = "tiff"
    se3 = SubElement(se2,'gmd:descriptiveKeywords')
    se4 = SubElement(se3,'gmd:MD_Keywords')
    se5 = SubElement(se4,'gmd:keyword')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = "UAV"
    se5 = SubElement(se4,'gmd:keyword')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = "ข้อมูลภาพถ่ายทางอากาศ"
    se5 = SubElement(se4,'gmd:type')
    se6 = SubElement(se5,'gmd:MD_KeywordTypeCode')
    se6.set('codeListValue','theme')
    se6.set('codeList',spHD[38])
    se3 = SubElement(se2,'gmd:spatialRepresentationType')
    se4 = SubElement(se3,'gmd:MD_SpatialRepresentationTypeCode')
    se4.set('codeListValue','grid')
    se4.set('codeList',spHD[39])
    se3 = SubElement(se2,'gmd:language')
    se4 = SubElement(se3,'gco:CharacterString')
    se4.text = "THA,ENG"
    se3 = SubElement(se2,'gmd:characterSet')
    se4 = SubElement(se3,'gmd:MD_CharacterSetCode')
    se4.set('codeListValue','utf8')
    se4.set('codeList',spHD[28])
    se3 = SubElement(se2,'gmd:topicCategory')
    se4 = SubElement(se3,'gmd:MD_TopicCategoryCode')
    se4.text = "location"
    se3 = SubElement(se2,'gmd:extent')
    se4 = SubElement(se3,'gmd:EX_Extent')
    se5 = SubElement(se4,'gmd:geographicElement')
    se6 = SubElement(se5,'gmd:EX_GeographicBoundingBox')
    se7 = SubElement(se6,'gmd:westBoundLongitude')
    se8 = SubElement(se7,'gco:Decimal')
    se8.text = str(cnP[1])
    se7 = SubElement(se6,'gmd:eastBoundLongitude')
    se8 = SubElement(se7,'gco:Decimal')
    se8.text = str(cnP[3])
    se7 = SubElement(se6,'gmd:southBoundLatitude')
    se8 = SubElement(se7,'gco:Decimal')
    se8.text = str(cnP[2])
    se7 = SubElement(se6,'gmd:northBoundLatitude')
    se8 = SubElement(se7,'gco:Decimal')
    se8.text = str(cnP[0])
    se3 = SubElement(se2,'gmd:supplementalInformation')
    se4 = SubElement(se3,'gco:CharacterString')

    se1 = SubElement(data,'gmd:contentInfo')
    se2 = SubElement(se1,'gmi:MI_ImageDescription')
    se3 = SubElement(se2,'gmd:attributeDescription')
    se4 = SubElement(se3,'gco:RecordType')
    se4.text = "Spectral Bands: These images contain " + str(bands) + " spectral band(s)"
    se3 = SubElement(se2,'gmd:contentType')
    se4 = SubElement(se3,'gmd:MD_CoverageContentTypeCode')
    se4.set('codeListValue','image')
    se4.set('codeList',spHD[40])
    se3 = SubElement(se2,'gmd:imagingCondition')
    se4.set('codeListValue','cloud')
    se4.set('codeList',spHD[41])
    se3 = SubElement(se2,'gmd:cloudCoverPercentage')
    se4 = SubElement(se3,'gco:Real')
    se4.text = "0.000000"
    se3 = SubElement(se2,'gmd:processingLevelCode')
    se4 = SubElement(se3,'gmd:RS_Identifier')
    se5 = SubElement(se4,'gmd:code')
    se6 = SubElement(se5,'gco:CharacterString')
    se3 = SubElement(se2,'gmd:cameraCalibrationInformationAvailability')
    se4 = SubElement(se3,'gco:Boolean')
    se4.text = "0"   
    se3 = SubElement(se2,'gmd:filmDistortionInformationAvailability')
    se4 = SubElement(se3,'gco:Boolean')
    se4.text = "0"
    se3 = SubElement(se2,'gmd:lensDistortionInformationAvailability')
    se4 = SubElement(se3,'gco:Boolean')
    se4.text = "0"

    se1 = SubElement(data,'gmd:distributionInfo')
    se2 = SubElement(se1,'gmd:MD_Distribution')
    se3 = SubElement(se2,'gmd:distributionFormat')
    se4 = SubElement(se3,'gmd:MD_Format')
    se5 = SubElement(se4,'gmd:name')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = "geotiff"
    se5 = SubElement(se4,'gmd:version')
    se6 = SubElement(se5,'gco:CharacterString')
    se6.text = __distributionDate__
    se3 = SubElement(se2,'gmd:transferOptions')
    se4 = SubElement(se3,'gmd:MD_DigitalTransferOptions')
    se5 = SubElement(se4,'gmd:onLine')
    se6 = SubElement(se5,'gmd:CI_OnlineResource')
    se7 = SubElement(se6,'gmd:linkage')
    se8 = SubElement(se7,'gmd:URL')
    se8.text = "https://www.gistda.or.th"
    se7 = SubElement(se6,'gmd:protocol')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = "WWW:LINK-1.0-http--link"    
    se7 = SubElement(se6,'gmd:name')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = "GISTDA"
    se7 = SubElement(se6,'gmd:description')
    se8 = SubElement(se7,'gco:CharacterString')
    se8.text = "นำคุณค่าจากอวกาศ เพื่อพัฒนาประเทศชาติและสังคม"
    return data
    
if __name__ == "__main__":
    main()