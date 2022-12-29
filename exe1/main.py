from osgeo import ogr
from django.contrib.gis.geos import Point
import sys
from osgeo import osr

fileName = "data/AFG_adm2.shp"
gdb = ogr.Open(fileName, 1)
layer = gdb.GetLayer(0)

def getRing(f):
    geom = f.GetGeometryRef()
    ring = geom.GetGeometryRef(0)
    return ring

features=[feature for feature in layer if(feature.GetGeometryRef().GetArea()>1)]

#משימה א

def GetAreaByFeature(f):
    geom = f.GetGeometryRef()
    area = geom.GetArea()
    return area

def getFid(f):
    return (f.GetFID())

def getName_2(f):
    return (f.NAME_2)

def getPoints(f):
    ring = getRing(f)
    return(ring.GetPoints())

def printDetails():
    for f in features:
        #א1
        print("FID: ", getFid(f))
        #א2
        print("area: ", GetAreaByFeature(f))
        #א3
        print("NAME_2: ", getName_2(f))
        #א4
        print("vertices: ", getPoints(f))
        print("neighbors: ", f.GetField("neighbors"))

#משימה ב
def createField(name):
    fld = ogr.FieldDefn(name, ogr.OFTInteger)
    layer.CreateField(fld)

def newField(name,value,feature):
    feature.SetField(name,value)
    layer.SetFeature(feature)

def returnFeatureByName(name):
    for f in layer:
        if(f.GetField("NAME_2") == name):
            return f

def distance():
    createField("distance")
    geometry = returnFeatureByName("Char Burjak")
    for f in layer:
        print(geometry.GetGeometryRef().Distance(f.GetGeometryRef()))
        if(geometry.GetGeometryRef().Distance(f.GetGeometryRef())<1):
            newField("distance", 1, f)
        else:
            newField("distance", 0, f)

def neighborsSum():
    createField("neighbors")
    features2 = [feature for feature in layer ]
    geomes = [geom.GetGeometryRef() for geom in features2]
    for i in range(len(geomes)):
        counter = 0
        for j in range(len(geomes)):
            if i == j:
                continue
            if geomes[i].Touches(geomes[j]):
                counter += 1
                print('Neighbor: ', i, j)
        print(counter)
        newField("neighbors", counter, layer[i])

#משימה ג

def ConvertToLineString(feature):
    line = ogr.Geometry(ogr.wkbLineString)
    points = getPoints(feature)
    for p in points:
        line.AddPoint(p[0], p[1])
    return line

def NewShapeFile():
    driver = ogr.GetDriverByName("ESRI Shapefile")
    outName = ("new_file.shp")
    output = driver.CreateDataSource(outName)
    newLayer = output.CreateLayer('new_file', geom_type = ogr.wkbLineString)
    newLayerDef = newLayer.GetLayerDefn()
    for f in features:
        line = ConvertToLineString(f)
        newFeature = ogr.Feature(newLayerDef)
        newFeature.SetGeometry(line)
        newFeature.SetFID(getFid(f))
        newLayer.CreateFeature(newFeature)
    
def ReadShapeFile():
    dataSource2 = ogr.Open('new_file.shp')
    layer2 = dataSource2.GetLayer(0)
    for f in layer2:
        print(f.ExportToJson())

#משימה ד

def getMaxArea():
    max = 0
    for f in features:
        area = f.GetGeometryRef().GetArea()
        if area > max:
            max = area
            maxFeature = f
    return maxFeature

def getMaxNeighbors():
    max = 0
    for f in layer:
        neighbors = f.GetField("neighbors")
        if neighbors > max:
            max = neighbors
            maxNeighbors = f
    return maxNeighbors

def createPoint(pointsArea, pointsNeighbors, i, j):
    point1 = ogr.Geometry(ogr.wkbPoint)
    point2 = ogr.Geometry(ogr.wkbPoint)
    point1.AddPoint(pointsArea.GetX(i), pointsArea.GetY(i))
    point2.AddPoint(pointsNeighbors.GetX(j), pointsNeighbors.GetY(j))
    return point1, point2

def getTwoPoints():
    maxArea = getMaxArea()
    maxNeighbors = getMaxNeighbors()
    pointsArea = maxArea.GetGeometryRef().GetGeometryRef(0)
    pointsNeighbors = maxNeighbors.GetGeometryRef().GetGeometryRef(0)
    point1, point2 = createPoint(pointsArea, pointsNeighbors, 0, 0)
    minDistance = point1.Distance(point2)
    minPoint1 = point1
    minPoint2 = point2
    for i in range(pointsArea.GetPointCount()):
        for j in range(pointsNeighbors.GetPointCount()):
            point1, point2 = createPoint(pointsArea, pointsNeighbors, i, j)
            distance = point1.Distance(point2)
            if(distance < minDistance):
                minDistance = distance
                minPoint1 = point1
                minPoint2 = point2
    return minPoint1, minPoint2

def createNewLine():
    line = ogr.Geometry(ogr.wkbLineString)
    point1, point2 = getTwoPoints()
    line.AddPoint(point1.GetX(), point1.GetY())
    line.AddPoint(point2.GetX(), point2.GetY())
    return line

def addLineString():
    line = createNewLine()
    file= ogr.Open('new_file.shp', 1)
    newLayer=file.GetLayer(0)
    newLayerDef = newLayer.GetLayerDefn()
    newFeature = ogr.Feature(newLayerDef)
    newFeature.SetGeometry(line)
    newLayer.CreateFeature(newFeature)

def main():
    printDetails()

    distance()
    neighborsSum()

    NewShapeFile()
    ReadShapeFile()

    addLineString()

main()

                