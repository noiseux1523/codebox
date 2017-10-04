import numpy as npy
import History
import sys
import copy
from numpy import ma
import matplotlib.pyplot as plt


#La classe history sert de format pour une histoire des evaluations pour nimporte quel solveur


class HistorySet:

#   Initialisations
    def __init__(self):
        self.historyList = []
        self.numberProblem = '1'
        self.numberStrat = '1'
        self.numberSeed = '1'
        self.prolemClass = 'undefined'
        self.algo = 'undefined'

#   Getters and setters
    def getNumberProblem(self):
        return self.numberProblem

    def setNumberProblem(self, entry):
        self.numberProblem = entry
        return

    def getNumberStrat(self):
        return self.numberStrat

    def setNumberStrat(self, entry):
        self.numberStrat = entry
        return

    def getNumberSeed(self):
        return self.numberSeed

    def setNumberSeed(self, entry):
        self.numberSeed = entry
        return

    def getAlgo(self):
        return self.algo

    def setAlgo(self, entry):
        self.algo = entry
        return

    def getProblemClass(self):
        return self.problemClass

    def setProblemClass(self, entry):
        self.problemClass = entry
        return

    def getHistoryList(self):
        return self.historyList

    def addHistory(self,entry):
        if type(entry) is History.History:
            self.historyList.append(entry)
        else:
            print('Objet non ajouté a l ensemble d histoires car pas de la classe History')
        return

#   Trace de profils

    def plotPerformance(self,ratio):

        #Dictionnaire pour les meilleures solution de chaque probleme
        bestDict = {}

        #On trouve les meilleures solutions de chaque problème
        # Marche meme si on a différentes seeds
        for history in self.historyList:
            currentBest=history.findBestSolution()
            if (history.problem) not in bestDict: #Clé du dictionnaire : %probname
                bestDict[history.problem]=currentBest
            elif (bestDict[history.problem]>currentBest):
                bestDict[history.problem]=currentBest

        #Doit retourner le nombre d'iterations que ca prends pour satisfaire le test
        #Pour chaque resolution
        # equivalent à t(p,s)
        nbItDict = {} #pour le nombre de iteration
        bestNbItDict = {} # meilleur par probleme
        whoHasBest = {}
        for history in self.historyList:
            tempArray = npy.array(history.getTable())
            nbLigne = len(history.table)
            #Itere sur les lignes
            for x in range(0, nbLigne):
                #Si le test est satisfait on append au dic avec key history : le nb d'iteration
                if (tempArray[0,1]-tempArray[x,1])>=(1-ratio)*(tempArray[0,1]-bestDict[history.problem]):
                    nbItDict[history]=tempArray[x,0]
                    break
            #Si le test n'est jamais satisfait
            if history not in nbItDict:
                nbItDict[history] = 1000000

        # Créer un dictionnaire avec key = strategie, objet = liste des profils
        for history in self.historyList:
            if (history.problem) not in bestNbItDict:
                bestNbItDict[history.problem]=nbItDict[history]
                whoHasBest[history.problem]=history.getStrat()
            elif nbItDict[history]<bestNbItDict[history.problem]:
                bestNbItDict[history.problem]=nbItDict[history]
                whoHasBest[history.problem] = history.getStrat()

        # montrer les resultats
        # n, ol, os, om = 0, 0, 0, 0
        # print("pour le ratio" + str(ratio) + '\n')
        # for prob in whoHasBest:
        #     if whoHasBest[prob]=='om':
        #         om = om+1
        #     if whoHasBest[prob]=='ol':
        #         ol = ol+1
        #     if whoHasBest[prob]=='os':
        #         os = os+1
        #     if whoHasBest[prob]=='n':
        #         n = n+1
        # print ("n = %d \n" %n)
        # print("os = %d \n" % os)
        # print("ol = %d \n" % ol)
        # print("om = %d \n" % om)


        # r(p,s)
        perfRatioDict={}
        for x in self.historyList:
            if x.strat not in perfRatioDict:
                perfRatioDict[x.strat]=[]
                perfRatioDict[x.strat].append(nbItDict[x] / bestNbItDict[x.problem])
            else:
                perfRatioDict[x.strat].append(nbItDict[x] / bestNbItDict[x.problem])

        # Ordonner les ratio dans le dictionnaire et créer les profils
        sortedPerfRatioDict = {}
        x,y,x2,y2 = {},{},{},{}
        for strat in perfRatioDict:
            sortedPerfRatioDict[strat]=sorted(perfRatioDict[strat])
            x[strat],y[strat]=[],[]
            nbProbTraite = 0
            # Cette boucle créer les profils de performance à tracer
            for pt in sortedPerfRatioDict[strat]:
                x[strat].append(pt)
                x[strat].append(pt)
                y[strat].append(nbProbTraite / len(perfRatioDict[strat]))
                nbProbTraite=nbProbTraite +1
                y[strat].append(nbProbTraite/len(perfRatioDict[strat]))
            x2[strat] = HistorySet.markerize(x[strat],13)
            y2[strat] = HistorySet.markerize(y[strat], 13)

        #Définition de la nomenclature pour les plots
        nomenclature = {'n': 'Sans opport.', 'ol': 'Lexico', 'os': 'Succes', 'om': 'Modeles', 'g': 'GPS',
                        'm': 'MADS','or':'Aleatoire','c':'CS','oo':'Omniscient','0n':'Negative-Omni.',
                        0.1: '01', 0.01: '001', 0.001: '0001'}
        colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
        color_index = 0

        # Plot
        for strat in sortedPerfRatioDict:
            plt.step(x[strat],y[strat],color = colors[color_index])
            plt.plot(x2[strat],y2[strat],marker = 'o', linestyle = 'None',label = nomenclature[strat], color = colors[color_index])
            color_index = color_index +1

        #Mettre graphe beau
        plt.ylim((0, 1.01))
        plt.xlim((1, 3))
        plt.legend(loc=4)
        plt.xlabel('Ratio de performance')
        plt.ylabel('Proportion de problème résolus')
        titre = 'Profil de performance avec ' + nomenclature[
            self.algo] + ' \n pour des problemes de type ' + self.getProblemClass() + ' et ' + r'$\tau$' + '=' + str(
            ratio)
        plt.title(titre)
        plt.savefig('perf_' + self.algo + '_' + self.problemClass + '_' + nomenclature[ratio] + '.png')
        plt.clf()
        return
        # # nombre de problème
        # sizeP=len(bestNbItDict)*int(self.getNumberSeed())
        #
        # #Dictionnaire avec clé = strat, value = liste de tuple (pts a plotter en escalier)
        # perfProfileDict = {}
        #
        # #Creer une liste avec les meme elements que la liste originale
        # tempList = list()
        # for x in self.historyList:
        #     tempList.append(x)
        #
        #
        #
        # # On fait un dictionnaire pour savoir combien de probleme sont traité par strategie
        # # Créer aussi le dictionnaire qui attache la liste de points à une strategie
        # probTraitParStratDict={}
        # for k in self.historyList:
        #     if perfProfileDict.get(k.strat)== None:
        #         perfProfileDict[k.strat] = list()
        #         probTraitParStratDict[k.strat] = 0
        # self.setNumberStrat(len(perfProfileDict))

        #On teste chaque point
        # for x in range(0,int(self.getNumberProblem())*int(self.getNumberSeed())):
        #     for y in self.historyList:
        #         isMin = True
        #         for z in tempList:
        #             #Si il y a un element plus petit dans le ratio pour une meme stratégie
        #             if y.strat==z.strat and perfRatioDict[y]>perfRatioDict[z]:
        #                 isMin = False
        #                 break
        #
        #         # Si c'est le minimum pour cette strategie présent dans l'ensemble
        #         # On l'enleve de l'ensemble temporaire et on y mets les deux points associés
        #         if isMin and y in tempList:
        #             point1=(perfRatioDict[y],((probTraitParStratDict[y.strat])/sizeP))
        #             point2=(perfRatioDict[y],((probTraitParStratDict[y.strat]+1)/sizeP))
        #             perfProfileDict[y.strat].append(point1)
        #             perfProfileDict[y.strat].append(point2)
        #             tempList.remove(y)
        #             probTraitParStratDict[y.strat]+=1

        #Fabrique le dictionnaire pour formater les titres
        # nomenclature={'n':'Sans opport.','ol':'Lexico','os':'Succes','om':'Model','g': 'GPS','m' : 'MADS',0.1:'01', 0.01:'001',0.001:'0001'}
        # colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
        # color_index = 0
        # # On itere sur les stratégies et on créer les points à plotter par strategie
        # for strat in perfProfileDict:
        #     lastPoint=perfProfileDict[strat][-1]
        #     perfProfileDict[strat].append((2000,(lastPoint[1])))
        #     x=list()
        #     y=list()
        #     for point in perfProfileDict[strat]:
        #         x.append(point[0])
        #         y.append(point[1])

            # Trace pour cette stratégie

        #xLimMaxForPlot=

    def plotData(self, ratio):

        # Dictionnaire pour les meilleures solution de chaque probleme
        bestDict = {}

        # On trouve les meilleures solutions de chaque problème
        # Marche meme si on a différentes seeds
        for history in self.historyList:
            currentBest = history.findBestSolution()
            if (history.problem) not in bestDict:  # Clé du dictionnaire : %probname
                bestDict[history.problem] = currentBest
            elif (bestDict[history.problem] > currentBest):
                bestDict[history.problem] = currentBest

        # Doit retourner le nombre d'iterations que ca prends pour satisfaire le test
        # Pour chaque resolution
        # equivalent à t(p,s)
        nbItDict = {}  # pour le nombre de iteration
        for history in self.historyList:
            tempArray = npy.array(history.getTable())
            nbLigne = len(history.table)
            # Itere sur les lignes
            for x in range(0, nbLigne):
                # Si le test est satisfait on append au dic avec key history : le nb d'iteration
                if (tempArray[0, 1] - tempArray[x, 1]) >= (1 - ratio) * (tempArray[0, 1] - bestDict[history.problem]):
                    nbItDict[history] = tempArray[x, 0]
                    break
            # Si le test n'est jamais satisfait
            if history not in nbItDict:
                nbItDict[history] = 1000000

        dataDict = {}
        for x in self.historyList:
            if x.strat not in dataDict:
                dataDict[x.strat]=[]
                dataDict[x.strat].append(nbItDict[x] / (int(x.nbVar)+1))
            else:
                dataDict[x.strat].append(nbItDict[x] / (int(x.nbVar)+1))

        # Ordonner les ratio dans le dictionnaire et créer les profils
        sortedDataDict = {}
        x, y, x2, y2 = {}, {}, {}, {}
        for strat in dataDict:
            sortedDataDict[strat] = sorted(dataDict[strat])
            x[strat], y[strat] = [], []
            nbProbTraite = 0
            # Cette boucle créer les profils de performance à tracer
            for pt in sortedDataDict[strat]:
                x[strat].append(pt)
                x[strat].append(pt)
                y[strat].append(nbProbTraite / len(dataDict[strat]))
                nbProbTraite = nbProbTraite + 1
                y[strat].append(nbProbTraite / len(dataDict[strat]))
            x2[strat] = HistorySet.markerize(x[strat], 13)
            y2[strat] = HistorySet.markerize(y[strat], 13)

        # Définition de la nomenclature pour les plots
        nomenclature = {'n': 'Sans opport.', 'ol': 'Lexico', 'os': 'Succes', 'om': 'Modeles', 'g': 'GPS',
                        'm': 'MADS','or':'Aleatoire','c':'CS','oo':'Omniscient','0n':'Negative-Omni.',
                        0.1: '01', 0.01: '001', 0.001: '0001'}
        colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
        color_index = 0

        # Plot
        for strat in sortedDataDict:
            plt.step(x[strat], y[strat], color=colors[color_index])
            plt.plot(x2[strat], y2[strat], marker='o', linestyle='None', color=colors[color_index], label = nomenclature[strat])
            color_index = color_index + 1

        # Mettre graphe beau
        plt.ylim((0, 1.01))
        plt.xlim((1, 75))
        plt.legend(loc=4)
        plt.xlabel('Nombre de gradient simplex')
        plt.ylabel('Proportion de problème résolus')
        titre = 'Profil de donnees avec ' + nomenclature[
            self.algo] + ' \n pour des problemes de type ' + self.getProblemClass() + ' et ' + r'$\tau$' + '=' + str(
            ratio)
        plt.title(titre)
        plt.savefig('data_' + self.algo + '_' + self.problemClass + '_' + nomenclature[ratio] + '.png')
        plt.clf()

        return

    def markerize(entry,number):
        # Retourne une liste avec 8 points à peu pres equidistant
        if len(entry)<=number:
            result = entry
        else:
            gap = int(npy.floor(len(entry)/number))
            indexes = []
            index=0
            result = []
            for i in range(number):
                index = index+gap
                indexes.append(index)
                result.append(entry[index])
        return result