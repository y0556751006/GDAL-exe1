from osgeo import ogr
from django.contrib.gis.geos import Point
import sys
from osgeo import osr

fileName="data/AFG_adm2.shp"
gdb = ogr.Open(fileName,1)
layer=gdb.GetLayer(0)

def getRing(f):
    geom = f.GetGeometryRef()
    ring = geom.GetGeometryRef(0)
    return ring

#משימה א

def GetAreaByFeature(f):
    geom=f.GetGeometryRef()
    area=geom.GetArea()
    return area

def getPoints(f):
    ring = getRing(f)
    return(ring.GetPoints())

def printDetails(features):
    for f in features:
        #א1
        print("FID: ",f.GetFID())
        #א2
        print("area: ",GetAreaByFeature(f))
        #א3
        print("NAME_2: ",f.NAME_2)
        #א4
        print("vertices: ",getPoints(f))
        # print("neighbors: ",f.GetField("neighbors"))

features=[feature for feature in layer if(feature.GetGeometryRef().GetArea()>1)]
printDetails(features)

#משימה ב
def createField(name):
    fld=ogr.FieldDefn(name,ogr.OFTInteger)
    layer.CreateField(fld)

def newField(name,value,feature):
    feature.SetField(name,value)
    layer.SetFeature(feature)

def returnFeatureByName(name):
    for f in layer:
        if(f.GetField("NAME_2")==name):
            return f

def distance():
    createField("distance")
    geometry=returnFeatureByName("Char Burjak")
    for f in layer:
        print(geometry.GetGeometryRef().Distance(f.GetGeometryRef()))
        if(geometry.GetGeometryRef().Distance(f.GetGeometryRef())<1):
            newField("distance",1,f)
        else:
            newField("distance",0,f)

def neighborsSum():
    createField("neighbors")
    for feature in layer:
        countNeighbors=0
        for f in layer:
            if(feature.GetGeometryRef().Touches(f.GetGeometryRef())):
                countNeighbors+=1
        print("countNeighbors ",countNeighbors)
        newField("neighbors",countNeighbors,feature)

# distance()
neighborsSum()

#משימה ג

def setFile(feature,newLayer,newLayerDef):
    geom=feature.GetGeometryRef()
    powerBoffer=geom.Buffer(250)
    bufferContains=powerBoffer.Contains(geom)
    if(bufferContains==True):
        newFeature = ogr.Feature(newLayerDef)
        newFeature.SetGeometry(geom)
        newFeature.SetFID(feature.GetFID())
        newLayer.CreateFeature(newFeature)

def createNewFile(features):
    for feature in features:
        name=("dataline.shp")
        driver = ogr.GetDriverByName("ESRI Shapefile")
        ds = driver.CreateDataSource(name)
        srs =  osr.SpatialReference()
        srs.ImportFromEPSG(4326)
        newLayer = ds.CreateLayer("dataline", srs, ogr.wkbLineString)
        if(newLayer is None):
            print("could not create layer")
            sys.exit(1)
        newLayerDef=newLayer.GetLayerDefn()
        setFile(feature,newLayer,newLayerDef)

features=[feature for feature in layer if(feature.GetGeometryRef().GetArea()>1)]
# createNewFile(features) 
                