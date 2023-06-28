from PIL import Image
import pyproj
import math
import os


def maptile(imgurl,zoomlevel,leftup_lon,leftup_lat,rightbottom_lon,rightbottom_lat,path):
    # 经纬度控制
    if leftup_lat > 85.05112877980659:
        leftup_lat = 85.05112877980659
    if rightbottom_lat < -85.05112877980659:
        rightbottom_lat = -85.05112877980659
    # 创建路径  
    savePath = os.path.join(path,f"tiles/{zoomlevel}")
    if os.path.exists(savePath) == False:
        os.makedirs(savePath)

    ################ 图像定位 #################
    img = Image.open(imgurl)
    # 新建画布
    tilesize = 256
    canvasSize = tilesize*2**zoomlevel
    canvas = Image.new("RGBA", (canvasSize, canvasSize))#缺省色彩值为透明底色
    # 经纬度坐标转化为投影坐标epsg:3857
    proj_in = pyproj.Proj(init='epsg:4326')  # WGS84经纬度坐标系
    proj_out = pyproj.Proj(init='epsg:3857')  # Web Mercator投影坐标系
    x1, y1 = pyproj.transform(proj_in, proj_out, leftup_lon, leftup_lat)
    x2, y2 = pyproj.transform(proj_in, proj_out, rightbottom_lon, rightbottom_lat)
    # 匹配投影坐标至当前画布尺寸
    if x1 > 0:
        x1 = int(round(x1*canvasSize/(20037508.342789244*2))+canvasSize/2)
    else:
        x1 = int(-round(x1*canvasSize/(20037508.342789244*2))-canvasSize/2)
    if y1 > 0:
        y1 = int(round(y1*canvasSize/(20037508.342789244*2))-canvasSize/2)
    else:
        y1 = int(-round(y1*canvasSize/(20037508.342789244*2))+canvasSize/2)
    if x2 > 0:
        x2 = int(round(x2*canvasSize/(20037508.342789244*2))+canvasSize/2)
    else:
        x2 = int(-round(x2*canvasSize/(20037508.342789244*2))-canvasSize/2)
    if y2 > 0:
        y2 = int(round(y2*canvasSize/(20037508.342789244*2))-canvasSize/2)
    else:
        y2 = int(-round(y2*canvasSize/(20037508.342789244*2))+canvasSize/2)
 
    ################ 图像附着 #################
    projTransImg = img
    # 规整图像size
    projTransImg = projTransImg.resize((x2-x1,y2-y1),resample=Image.BILINEAR)
    # 图像加载至画布
    canvas.paste(projTransImg, (x1, y1, x2, y2))


    ################ 切图 #################
    wi = canvas.width
    he = canvas.height
    # 贴图所在extent范围
    extentX1 = int(x1/256)
    extentY1 = int(y1/256)
    extentX2 = math.ceil(x2/256)
    extentY2 = math.ceil(y2/256)
    # 切片输出
    for i in range( extentX1, extentX2):
        for j in range( extentY1, extentY2):
            # 图像剪裁canvas.crop((l,u,r,b))
            canvasTile = canvas.crop((i*tilesize,j*tilesize,(i+1)*tilesize,(j+1)*tilesize))
            canvasTile.save(f"{savePath}/{i}_{j}.png",dpi = (96, 96))


