import sys
from osgeo import ogr
from geos import geometry
from django.contrib.gis.geos import Point,GEOSGeometry
from osgeo import osr, gdal

def print_hi(name):
    print(f'Hi, {name}') 
ogr.UseExceptions()
driver = ogr.GetDriverByName("OpenFileGDB")
fileName="data/AFG_adm2.shp"
try:
    gdb = ogr.Open("/home/nvmGUser/users/tepler/GDAL-exe1/data/AFG_adm2.shp",1)
except Exception():
    print (Exception)
    sys.exit()
file = ogr.Open("/home/nvmGUser/users/tepler/GDAL-exe1/dataline.shp",1)
# for layer in range(file.GetLayerCount()):
#     for i in file.GetLayer(layer):
#         print(i.ExportToJson())
# for layer in range(gdb.GetLayerCount()):
#     for i in gdb.GetLayer(layer):
#         print(i.ExportToJson())

ds = gdal.OpenEx("/home/nvmGUser/users/tepler/GDAL-exe1/data/AFG_adm2.shp")
print(ds.GetLayerCount())
print(gdb.GetLayerCount())
# print(dir(ds))
ulx, width, xrot, uly, yrot, height  = ds.GetGeoTransform()
print(ulx,uly)
########
print("ds",ds)
wkt_srs = ds.GetProjection()
gt = ds.GetGeoTransform()
xs = ds.RasterXSize
ys = ds.RasterYSize
print("gt",gt)
print("xs",xs)
print("ys",ys)
ulx, uly = gdal.ApplyGeoTransform(gt, 0, 0)
lrx, lry = gdal.ApplyGeoTransform(gt, xs, ys)
print("ulx, uly",ulx, uly)
print("lrx, lry",lrx, lry)

######
name = ("dataline.shp")
driver = ogr.GetDriverByName("ESRI Shapefile")
try:
    ds = driver.CreateDataSource(name)
except:
    print("could not creat")
srs =  osr.SpatialReference()
srs.ImportFromEPSG(4326)
# newLayer = ds.CreateLayer("dataline", geon_type=ogr.wkbPolygon)
newLayer = ds.CreateLayer("dataline", srs, ogr.wkbLineString)
if(newLayer is None):
    print("could not create layer")
    sys.exit(1)
# idField = ogr.FieldDefn("id", ogr.OFTInteger)
# newLayer.CreateField(idField)
newLayerDef=newLayer.GetLayerDefn()
for layer in gdb:
    # fld=ogr.FieldDefn("distance",ogr.OFTInteger)
    # layer.CreateField(fld)
    for feature in layer:
        geon=feature.GetGeometryRef()
        area=geon.GetArea()
        ring = geon.GetGeometryRef(0)
        from shapely.wkt import loads
        lin = loads('LineString (289.63171806167395061 -200.22555066079294761, 380.69030837004402201 -65.28898678414094547)')
        # print(dir(layer))
        # print(dir(ring.GetPoint()))
        pol = loads('Polygon ((112.23259911894263041 -229.94933920704846742, 178.75726872246687549 -113.4132158590308137, 309.44757709251092592 -114.35682819383258391, 376.44405286343607031 -230.42114537444933831, 305.67312775330390195 -344.59823788546259493, 176.39823788546246419 -345.07004405286346582, 112.23259911894263041 -229.94933920704846742))')
        # the LinearRing
        from shapely.geometry import LineString
        polin = LineString(list(pol.exterior.coords))
        # intersection 
        pt = polin.intersection(lin)
        # print(pt.wkt)
        # print(polin.wkt)
        if(feature.GetField("NAME_2")=="Char Burjak"):
            print("Char Burjak----")
            for f in layer:
                geom2 = f.GetGeometryRef()
                ring2 = geom2.GetGeometryRef(0)
                if geom2.GetGeometryName()=="POLYGON":
                    # print("NAME_2:",f.GetField("NAME_2"))
                    point=Point(ring.GetPoint())
                    point2=Point(ring2.GetPoint())
                    distance=point.distance(point2)
                    # print("distance:",distance)
                    if distance<1:
                        f.SetField("distance",1)
                        layer.SetFeature(f)
                    else:
                        f.SetField("distance",0)
                        layer.SetFeature(f)
                else:
                    print(geom2.GetGeometryName())
        if(area>1):
            print("FID: ",feature.GetFID())
            print("area: ",area)
            print("NAME_2: ",feature.NAME_2)
            powerBoffer=geon.Buffer(250)
            bufferContains=powerBoffer.Contains(geon)
            if(bufferContains==True):
                try:
            # featureDefn = newLayer.GetLayerDefn()
                    newFeature = ogr.Feature(newLayerDef)
                    newFeature.SetGeometry(geon)
                    newFeature.SetFID(feature.GetFID())
                    newLayer.CreateFeature(newFeature)
                except:
                    print("error")
                    newFeature.Destroy()
            print(dir(ring))
            points = ring.GetPointCount()

            for p in range(points):
                lon, lat, z = ring.GetPoint(p)
                # print(lon, lat )
            point=ring.GetPoint()
            # for vertex in ring.GetPoint():
            #     print("coordinates: ",vertex)
            # print(ring.GetBoundary())
            # print(dir(geon.CoordinateDimension()))

 
del gdb

if __name__ == '__main__':
    print_hi('PyCharm')
