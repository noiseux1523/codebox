import matplotlib.pyplot as plt
import classes.History as History
import classes.HistorySet as HistorySet
import numpy as npy
import classes.nomadFonctions as NOMAD
import pickle
import subprocess
import tousFonctions as fct

def test1():
    # plt.plot([1,2,3,4])
    # plt.ylabel('some numbers')
    # plt.show()
    historySet= HistorySet.HistorySet()


    history = NOMAD.readLog('bb3_history.0.txt')
    history.clean()
    print(history.table)
    historySet.addHistory(history)

    history = NOMAD.readLog('bb2_history_mol.0.txt')
    history.setNbVar(5)
    print(history.table)
    print(history.findBestSolution())
    history.clean()
    print(history.table)
    print(history)
    return
def test2():
    for x in set.historyList:
        print(x)
        print(x.table)

    [a, b, c, d, e] = set.plotPerformance(0.1)

    for x in a:
        print(x, a[x])
    for x in b:
        print(x, b[x])
    for x in c:
        print(x, c[x])
    for x in d:
        print(x, d[x])
    for x in e:
        print(x, e[x])
    print(len(a))
    # HistorySet.addHistory(history)

    # Trouver le meilleur de tous les history
    currentbest = 10 ^ 100
    for x in range(0, len(HistorySet.historyList)):
        currentHistory = HistorySet.historyList[x]
        if currentHistory.findBestSolution() < currentbest:
            currentbest = currentHistory.findBestSolution()

    # Faire les profils de performance


    # Faire les profils de donnees


    print(currentbest)
    return
def serialNomadRuns():
    # Rouler les problèmes en serie
    algo=['g','m']
    problem=['bb1','bb2','bb3']
    ordering=['n','ol','os','om']
    currentname = ''
    for p in range(0,3):
        for a in range (0,2):
            for o in range(0,4):
                currentname = '\"%NOMAD_HOME%\\bin\\nomad.exe\" '+problem[p]+'_parameters_'+algo[a]+ordering[o]+'.txt'
                print(currentname)
                subprocess.call(currentname, shell=True)
    return
def codeRapport1():
    #########################################
    ################ CODE POUR RAPPORT 1 ####
    algo=['g','m']
    problem=['bb1','bb2','bb3']
    ordering=['n','ol','os','om']
    currentname = ''

    taux=[0.1,0.01,0.001]
    for a in algo:
        for x in taux:
            set = HistorySet.HistorySet()
            set.algo=a
            for p in range(0,3):
                for o in range(0,4):
                    nomFichier = problem[p]+"_history_"+a+ordering[o]+".0.txt"
                    history=NOMAD.readLog(nomFichier)
                    history.setProblem(problem[p])
                    history.setSolver(a)
                    history.setStrat(ordering[o])

                    ##Faire une fonction pour trouver le nombre de var. (avec stats)
                    if p==0:
                        history.setNbVar(4)
                    elif p==1:
                        history.setNbVar(5)
                    else:
                        history.setNbVar(2)

                    set.addHistory(history)
            set.setNumberProblem(p + 1)
            set.setNumberStrat(o + 1)
            set.plotPerformance(x)
            #set.plotData(x)
            # for b in dic:
            #     print(b)
            #     print(dic[b])
    #####################################################
    #####################################################
    return
def codeRapport2():
    problems = ['bb1','bb2','bb3']
    algos = ['g', 'm']
    strats = ['n','ol','os','om']
    nbPts = 100

    for problem in problems:
        ## Un fichier de paramètre random juste pour generer des points et on les sauvegarde dans un fichier texte
        generateTemplateFileName = problem + '_parameters_gos.txt'
        pts = fct.generateStartPoints(generateTemplateFileName,nbPts)
        npy.savetxt((problem+'_pts.txt'),pts)

        ## Créer un fichier avec toujours les memes points
        for algo in algos:
            for strat in strats:
                parameterTemplateName = problem + '_parameters_'+algo+strat+'.txt'
                NOMAD.generateParametersFiles(parameterTemplateName,pts)

    for algo in algos:
        set = HistorySet.HistorySet()
        for problem in problems:
            for strat in strats:
                for number in range(0,nbPts):
                    # Lignes pour rouler nomad en serie avec toutes les instances
                    # currentname = '\"%NOMAD_HOME%\\bin\\nomad.exe\" ' + problem + '_parameters_' + algo + strat + '_' + str(number+1) +'.txt'
                    # subprocess.call(currentname, shell=True)
                    if (str(number+1))[-1]=='0':
                        nomFichier=problem + '_history_' + algo + strat + '_' + str(number + 1) + '.txt'
                    else:
                        nomFichier=problem + '_history_' + algo + strat + '_' + str(number + 1) + '.0.txt'
                    history = NOMAD.readLog(nomFichier)
                    set.addHistory(history)
        set.setNumberProblem(len(problems)*nbPts)
        set.setNumberStrat(len(strats))
        set.setAlgo(algo)
        set.plotData(0.001)

    #test=NOMAD.readLog('bb1_history_gn.0.txt')

    return

def codeRapport3():

    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'g': 'GPS', 'm': 'MADS'}
    strategies = ['n', 'ol', 'os', 'om']

    for instance in instances:
        for type in types:
            # exename = instance+'_'+type+"\\bb.exe"
            # cppname = instance + '_' + type + "\\bb.cpp"
            # call(["g++", "-o", exename, cppname])
            for algo in algos:
                for strategy in strategies:
                    foldername = 'resultats' + instance + '_' + type + '\\' + algo + strategy
                    for seed in seeds:
                        filename = foldername + '\\' + seed + '_param.txt'
                        print(filename)
    return
def test4():
    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'g': 'GPS', 'm': 'MADS'}
    strategies = ['n', 'ol', 'os', 'om']
    i = 0
    set = HistorySet.HistorySet()
    for algo in algos:
        for type in types:
            set = HistorySet.HistorySet()
            for instance in instances:
                for strategy in strategies:
                    # exename = instance+'_'+type+"\\bb.exe"
                    # cppname = instance + '_' + type + "\\bb.cpp"
                    # call(["g++", "-o", exename, cppname])
                        foldername = 'resultats' +'\\' + instance + '_' + type + '\\' + algo + strategy
                        for seed in seeds:
                            historyfile = instance + '_' + type + '_history_' + seed + '_' + algo+strategy + '.' +seed + '.txt'
                            filename = foldername + '\\' + historyfile
                            currentHist = NOMAD.readLog(filename)
                            set.addHistory(currentHist)
            with open(algo+type+'.pkl', 'wb') as output:
                pickle.dump(set, output, pickle.HIGHEST_PROTOCOL)
            del set

def test5():

    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'g': 'GPS', 'm': 'MADS'}
    strategies = ['n', 'ol', 'os', 'om']

    #Pre traitement des history en enlevant les non succes (on aurait pu prendre stats)
    for algo in algos:
        for type in types:
            dumpStrat = algo+type
            fileName = "pkl_algo_type\\"+algo+type+".pkl"
            with open(fileName, 'rb') as f:
                set = pickle.load(f)
                f.close()

            # Setter les bons parametres pour le set
            set.setNumberProblem(len(instances))
            set.setNumberSeed(len(seeds))
            set.setNumberStrat(len(strategies))
            set.setAlgo(algo)

            # Nettoyer et garder seulement les succès
            for history in set.historyList:
                history.clean()
            set.setProblemClass(type)

            # Re pickler mais seulements les histoires nettoyées
            pickle.dump(set, open(fileName[:-4]+"_clean.pkl", "wb"), pickle.HIGHEST_PROTOCOL)
            del set


    return

def test6():

    seeds = [str(x + 1) for x in range(10)]
    instances = [str(x + 1) for x in range(53)]
    types = ['SMOOTH', 'NONDIFF', 'WILD3', 'NOISY3']
    algos = {'g': 'GPS', 'm': 'MADS'}
    strategies = ['n', 'ol', 'os', 'om']
    ratios = [0.1,0.01,0.001]
    for algo in algos:
        for type in types:
            fileName = "pkl_algo_type\\" + algo + type
            with open(fileName+'_clean.pkl', "rb") as f:
                testSet = pickle.load(f)
                f.close()
            for ratio in ratios:
                testSet.plotPerformance(ratio)
                testSet.plotData(ratio)
  #  testSet.plotPerformance(0.1)
#codeRapport3()
def test7():
    algo = 'g'
    ratio = 0.1
    type = 'SMOOTH'
    fileName = "pkl_algo_type\\" + algo + type
    with open(fileName + '_clean.pkl', "rb") as f:
        testSet = pickle.load(f)
        f.close()
    testSet.plotData(ratio)

    ratio = 0.001
    with open(fileName + '_clean.pkl', "rb") as f:
        testSet2 = pickle.load(f)
        f.close()
    testSet2.plotData(ratio)

    return
test6()

