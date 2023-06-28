from maptiler import maptile

################ 输入 #################
# 输入图像
imgurl = "D:/operating/文学地图-西游/geo&data/web/img.jpg"
# 放大级数0-25
zoomlevel = 4
# 经纬度范围
leftup_lon = -180
leftup_lat = 85.05112877980659
rightbottom_lon = 180
rightbottom_lat = -85.05112877980659
#保存路径
path = "C:/Users/Admin/Documents"
maptile(imgurl,zoomlevel,leftup_lon,leftup_lat,rightbottom_lon,rightbottom_lat,path)
