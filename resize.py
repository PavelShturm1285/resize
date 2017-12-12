from PIL import Image
from math import *


def interpolacao(x, y, x1, y1, x2, y2, q11, q21, q12, q22):
    fxy1 = (((q21-q11)/(x2-x1))*(x-x1))+q11
    fxy2 = (((q22-q12)/(x2-x1))*(x-x1))+q12
    fxy = ((y2-y)/(y2-y1))*fxy1 + ((y-y1)/(y2-y1))*fxy2
    return fxy


caminho = input("Caminho: ")
imagem = input("Imagem: ")
escala = int(input("Escala: "))

nome, formato = imagem.split(".")

im = Image.open(caminho+"/"+nome+"."+formato)
im = im.convert("RGB")

width = im.size[0]
height = im.size[1]

new_img = Image.new("RGB", (width*escala, height*escala), "black")
pixelMap = new_img.load()

interp = True

xsrc = list(range(width))
ysrc = list(range(height))

xdst = list(range(width*escala))
ydst = list(range(height*escala))

x_interp = list(xdst)
y_interp = list(ydst)

for i in range(len(xdst)):
    x_interp[i] = xdst[i]/escala

for i in range(len(ydst)):
    y_interp[i] = ydst[i]/escala

img_r = [ [ 0 for x in range(width) ] for y in range(height) ]
img_g = [ [ 0 for x in range(width) ] for y in range(height) ]
img_b = [ [ 0 for x in range(width) ] for y in range(height) ]
img_dst_r = [ [ 0 for x in range(escala*width) ] for y in range(escala*height) ]
img_dst_r = [ [ 0 for x in range(escala*width) ] for y in range(escala*height) ]
img_dst_g = [ [ 0 for x in range(escala*width) ] for y in range(escala*height) ]
img_dst_b = [ [ 0 for x in range(escala*width) ] for y in range(escala*height) ]


for y in range(height):
    for x in range(width):
        r, g, b = im.getpixel((x,y))
        img_r[y][x] = r
        img_g[y][x] = g
        img_b[y][x] = b


for y in range(height*escala):
    for x in range(width*escala):
        xx = x / escala
        yy = y / escala
        if interp:
            if (xx < width-1 and yy < height -1):
                img_dst_r[y][x] = interpolacao(xx, yy,
                    floor(xx), floor(yy),
                    floor(xx+1), floor(yy+1), 
                    img_r[floor(yy)][floor(xx)], 
                    img_r[floor(yy)][floor(xx+1)], 
                    img_r[floor(yy+1)][floor(xx)], 
                    img_r[floor(yy+1)][floor(xx+1)])
                img_dst_g[y][x] = interpolacao(xx, yy,
                    floor(xx), floor(yy),
                    floor(xx+1), floor(yy+1), 
                    img_g[floor(yy)][floor(xx)], 
                    img_g[floor(yy)][floor(xx+1)], 
                    img_g[floor(yy+1)][floor(xx)], 
                    img_g[floor(yy+1)][floor(xx+1)])
                img_dst_b[y][x] = interpolacao(xx, yy,
                    floor(xx), floor(yy),
                    floor(xx+1), floor(yy+1), 
                    img_b[floor(yy)][floor(xx)], 
                    img_b[floor(yy)][floor(xx+1)], 
                    img_b[floor(yy+1)][floor(xx)], 
                    img_b[floor(yy+1)][floor(xx+1)])
        else:
            img_dst_r[y][x] = img_r[floor(yy)][floor(xx)]
            img_dst_g[y][x] = img_g[floor(yy)][floor(xx)]
            img_dst_b[y][x] = img_b[floor(yy)][floor(xx)]


for y in ydst:
    for x in xdst:
        r = int(img_dst_r[y][x])
        g = int(img_dst_g[y][x])
        b = int(img_dst_b[y][x])
        pixelMap[x,y] = (r, g, b)

new_img.save(caminho+"/"+nome+"_resize."+formato)
