
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Ellipse
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm, colorbar
from matplotlib.lines import Line2D

import numpy as np 
from sklearn.preprocessing import minmax_scale

def plot_map(som, nrows, ncols,feature_names = [], size=(10,10),topology='rectangular', normalize_weights = True, um = False, um_val = []):
    '''
    Gráfico dos pesos da matriz de pesos.

    '''
    if topology == 'rectangular':
        if um == False:
            W = som.get_weights()
        else:
            W = um_val
        plt.figure(figsize=size)
        for i, f in enumerate(feature_names):
            plt.subplot(nrows, ncols, i+1)
            plt.title(f)
            plt.pcolor(W[:,:,i].T, cmap='coolwarm')
            
            plt.xticks(np.arange(W.shape[0]+1))
            plt.yticks(np.arange(W.shape[1]+1))
        plt.tight_layout()
        plt.show()

    elif topology == 'hexagonal':
        xx, yy = som.get_euclidean_coordinates()

        if um == False:
            weights = som.get_weights()
        else:
            weights = um_val
        for k, fname in enumerate(feature_names):
            #plt.subplot(nrows, ncols, k+1)
            #plt.figure(figsize=(10,10))
            f = plt.figure(figsize=size)

            ax = f.add_subplot(nrows, ncols, k+1)

            ax.set_aspect('equal')

            plt.title(fname)

            n_weight = np.copy(weights[:,:,k])

            if normalize_weights:
                n_weight = minmax_scale(n_weight)
            # iteratively add hexagons
            for i in range(weights.shape[0]):
                for j in range(weights.shape[1]):
                    wy = yy[(i, j)] * np.sqrt(3) / 2
                    hex = RegularPolygon((xx[(i, j)], wy), 
                                        numVertices=6, 
                                        radius=.95 / np.sqrt(3),
                                        facecolor=cm.Blues(n_weight[i, j]), 
                                        alpha=.4, 
                                        edgecolor='gray')
                    ax.add_patch(hex)

            xrange = np.arange(weights.shape[0])
            yrange = np.arange(weights.shape[1])
            plt.xticks(xrange-.5, xrange)
            plt.yticks(yrange * np.sqrt(3) / 2, yrange)
            plt.xlim((-1,weights.shape[0]))
            plt.ylim((-0.5,weights.shape[1]))
            #plt.show()
        
    else:
        print('Topology not understood. It should be rectangular or hexagonal')


def plot_umatrix(som,topology):

    umatrix = som.distance_map()

    um = umatrix.reshape(umatrix.shape[0],umatrix.shape[1],1)
    names = ['umatrix']

    plot_map(som, 1, 1,feature_names = names, topology=topology, normalize_weights = True, um = True, um_val = um)


