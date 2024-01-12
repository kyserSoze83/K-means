from asyncio.windows_events import NULL
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.collections as mc
import pylab as pl # matplotlib module



def draw2D(samples, size=10, drawLinks=True):
	# Formatting the data:
	X, Y, links, centroids = [], [], [], set()
	for sample in samples:
		X.append(sample[0])
		Y.append(sample[1])
		if len(sample) == 4:
			links.append([sample[:2], sample[2:]])
			centroids.add((sample[2], sample[3]))
	centroids = sorted(centroids) # before shuffling, to not depend on data order.
	random.seed(42) # to have consistent results.
	random.shuffle(centroids) # making less likely that close clusters have close colors.
	centroids = { cent : centroids.index(cent) for cent in centroids }
	# Colors map:
	colors = cm.rainbow(np.linspace(0, 1., len(centroids)))
	C = None # unique color!
	if len(centroids) > 0:
		C = [ colors[centroids[(sample[2], sample[3])]] for sample in samples ]
	# Drawing:
	fig, ax = pl.subplots(figsize=(size, size))
	fig.suptitle('Visualisation de %d données' % len(samples), fontsize=16)
	ax.set_xlabel('x', fontsize=12)
	ax.set_ylabel('y', fontsize=12)
	if drawLinks:
		ax.add_collection(mc.LineCollection(links, colors=C, alpha=0.1, linewidths=1))
	ax.scatter(X, Y, c=C, alpha=0.5, s=10)
	for cent in centroids:
		ax.plot(cent[0], cent[1], c='black', marker='+', markersize=8)
	ax.autoscale()
	ax.margins(0.05)
	plt.show()

points=[]
centroides=[]


def distance(centrex,centrey,x,y): #calculateur de distance entre les point et le centroïde
    return math.sqrt(math.pow(centrex -x,2.0)  + math.pow(centrey - y, 2.0)) #calcul la distance d'un point avec un centroïde


#La fonction a pour but de modifier le troisième et le quatrieme element du tuple de chaque point pour leur attribuer une  coordonnee resectivement x et y du centroide
def setCentroide(points,centroides):
    newPoints=[]
    """firstLine=["x","y","centroid_x","centroid_y"]
    newPoints.append(firstLine)""" 
    long=len(points)
    long2=len(centroides)
    #ctr=NULL
    for i in range(0,long,1):
        dMin=NULL
        #On selectionne un point qui est un liste composé d'une coord. x une coord. y d'une coordonnee x  et y du centroide le plus proche que l'on va determiner par la suite
        cordPnt=points[i] 
        #On boucle pour calculer la distance entre le point selectionné et chaque centroide pour voir lequel est le plus proche du point
        for j in range(0,long2,1):
            cordCtr=centroides[j]
            #Autre manière :((cordPnt[0]-cordCtr[0])^2+(cordPnt[1]-cordCtr[1])^2)^(1/2)
            d=distance(cordCtr[0],cordCtr[1],cordPnt[0],cordPnt[1]) 
            if dMin==NULL:
                #w=w+1
                dMin=d
                #On sauvegarde le centroide qui correspond à la distance minimale
                saveCtr=centroides[j]
            elif d<dMin and d!=NULL:
                #w=w+1
                dMin=d
                #On sauvegarde le centroide qui correspond à la distance minimale
                saveCtr=centroides[j]
            elif dMin==d and d!=NULL:
                #w=w+1
                nb=random.randint(1,3)
                if nb==1:
                    #On sauvegarde le centroide qui correspond à la distance minimale
                    saveCtr=centroides[j-1]
                elif nb==2:
                    #On sauvegarde le centroide qui correspond à la distance minimale
                    saveCtr=centroides[j]
        #on édite une liste avec les coordonées x et y du points selectionné et on lui donne aussi ls coordonnée du centroide le plus proche
        a=[cordPnt[0],cordPnt[1],saveCtr[0],saveCtr[1]]
        #on ajoute la liste créée qui represente un point à la nouvelle liste des points qui va remplacer l'ancienne grace au return 
        newPoints.append(a)    
    return newPoints
    


def newCentroides(points,centroides):
    tabCentroides=[]
    long=len(points)
    long2=len(centroides)
    for i in range(0,long2,1):
        centroide=centroides[i] 
        c=0
        d=0
        e=0
        for j in range(0,long,1):
            point=points[j]
            if point[2]==centroide[0] and point[3]==centroide[1] :
                c=c+point[0]
                d=d+point[1]
                e=e+1
        if e!=0:
            b=[round(c/e,3),round(d/e,3)]
        else:
            b=[centroide[0],centroide[1]]
        tabCentroides.append(b)
    return tabCentroides




from numpy import genfromtxt
data = genfromtxt('C:/Users/33767/Documents/python/ProjetS4/ProjetS4/mock_2d_data.csv', delimiter=',', skip_header = 1)
long=len(data)
firstLine=['x','y','centroid_x','centroid_y']
for i in range(0,long,1):
    point=[data[i,0],data[i,1],NULL,NULL]
    points.append(point)
for i in range(0,6,1):
    xCentroide=round(random.randint(-60, 60) * random.random(), 2)
    yCentroide=round(random.randint(-60, 60) * random.random(), 2)
    centroide=[xCentroide,yCentroide]
    centroides.append(centroide)
pointsSS=[]
centroidesSS=[]
while point!=pointsSS and centroides!=centroidesSS :
    pointsSS=points
    centroidesSS=centroides
    draw2D(points, size=10, drawLinks=True)
    points=setCentroide(points,centroides)
    centroides=newCentroides(points,centroides)
print(centroides)
points.insert(0,firstLine)
fichier = open("C:/Users/33767/Documents/python/ProjetS4/ProjetS4/points.csv", "w")
longueur=len(points)
strOne = ','.join(points[0])
fichier.write(strOne+"\n")
for i in range(1,longueur,1):
    strInt = ','.join([str(elem) for elem in points[i]])
    fichier.write(strInt)
    fichier.write("\n")
fichier.close()
