
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats


def iter_rmse_scc():
    iv = 2
    gnn_10_rmse = np.loadtxt('data/GNN_10_RMSE.txt')[::iv]
    gnn_20_rmse = np.loadtxt('data/GNN_20_RMSE.txt')[::iv]
    gnn_30_rmse = np.loadtxt('data/GNN_30_RMSE.txt')[::iv]
    gcn_rmse = np.loadtxt('data/GCN_RMSE.txt')[::iv]

    gnn_10_scc = np.loadtxt('data/GNN_10_SMC.txt')[::iv]
    gnn_20_scc = np.loadtxt('data/GNN_20_SMC.txt')[::iv]
    gnn_30_scc = np.loadtxt('data/GNN_30_SMC.txt')[::iv]
    gcn_scc = np.loadtxt('data/GCN_SMC.txt')[::iv]

    x = np.arange(50, 10001, 50*iv)

    lw = 1
    colors = ['orangered', 'hotpink', 'limegreen', 'skyblue']
    fig, ax1 = plt.subplots()

    l1, = ax1.plot(x, gnn_10_rmse, color=colors[0], linewidth=lw, alpha=0.7, label='GNN_10')
    l2, = ax1.plot(x, gnn_20_rmse, color=colors[1], linewidth=lw, alpha=0.7, label='GNN_20')
    l3, = ax1.plot(x, gnn_30_rmse, color=colors[2], linewidth=lw, alpha=0.7, label='GNN_30')
    l4, = ax1.plot(x, gcn_rmse, color=colors[3], linewidth=lw, alpha=1, label='SI-GCN')
    ax1.set_xlabel('Iterations')
    ax1.set_ylabel('RMSE')
    #ax1.set_xlim(0, 10000)
    #ax1.set_ylim(22, 36)

    ax2 = ax1.twinx()
    l5, = ax2.plot([30], [0.5], color='gray', linewidth=lw, linestyle='-', label='RMSE')
    l6, = ax2.plot([30], [0.5], color='gray', linewidth=lw, linestyle='--', label='SCC')
    ax2.plot(x, gnn_10_scc, color=colors[0], linestyle='--', linewidth=lw, alpha=0.7)
    ax2.plot(x, gnn_20_scc, color=colors[1], linestyle='--', linewidth=lw, alpha=0.7)
    ax2.plot(x, gnn_30_scc, color=colors[2], linestyle='--', linewidth=lw, alpha=0.7)
    ax2.plot(x, gcn_scc, color=colors[3], linestyle='--', linewidth=lw, alpha=1)

    ax2.set_xlabel('Iterations')
    ax2.set_ylabel('SCC')
    #ax2.set_xlim(0, 10000)
    #ax2.set_ylim(0.2, 0.7)

    ax1.legend([l1, l2, l3, l4], labels=['GNN_10', 'GNN_20', 'GNN_30', 'SI-GCN'], bbox_to_anchor=(0.97, 0.61),
               borderaxespad=0.1, ncol=1)
    ax2.legend([l5, l6], labels=['RMSE', 'SCC'], bbox_to_anchor=(0.75, 0.55), borderaxespad=0.1, ncol=1)

    #plt.subplots_adjust(top=0.88)

    plt.show()


# determine which output produces the best prediction accuracy
def check():
    r = np.loadtxt('SI-GCN/data/taxi/test.txt', dtype=np.uint32, delimiter='\t')[:, 3]
    path = 'SI-GCN/data/output/'
    files = os.listdir(path)
    for filename in files:
        p = np.loadtxt(path + filename)[:1427]
        smc = stats.spearmanr(r, p)
        scc = round(smc[0], 3)
        rmse = round(np.sqrt(np.mean(np.square(r - p))), 3)
        print(filename, scc, rmse)


def var_threshold():
    sns.set_style('whitegrid')
    real = np.loadtxt('SI-GCN/data/taxi/test.txt', dtype=np.uint32, delimiter='\t')[:, 3]
    gcn = np.loadtxt('SI-GCN/data/output/d_39000.txt')[:1427]
    #gnn_10 = np.loadtxt('data/pred_gnn_10.txt')
    #gnn_20 = np.loadtxt('data/pred_gnn_20.txt')
    gm_p = np.loadtxt('data/pred_GM_P.txt')
    rm = np.loadtxt('data/pred_RM.txt')
    gnn_30 = np.loadtxt('data/pred_gnn_30.txt')

    ts = [30, 40, 50, 60, 70, 80, 90, 100]
    gcn_rmse = []
    gnn_10_rmse = []
    gnn_20_rmse = []
    gnn_30_rmse = []
    gm_p_rmse = []
    rm_rmse = []
    for t in ts:
        idx = np.where(real >= t)
        gcn_rmse.append(round(np.sqrt(np.mean(np.square(real[idx] - gcn[idx])))/t, 3))
        #gnn_10_rmse.append(round(np.sqrt(np.mean(np.square(real[idx] - gnn_10[idx]))), 3))
        #gnn_20_rmse.append(round(np.sqrt(np.mean(np.square(real[idx] - gnn_20[idx]))), 3))
        gnn_30_rmse.append(round(np.sqrt(np.mean(np.square(real[idx] - gnn_30[idx])))/t, 3))
        gm_p_rmse.append(round(np.sqrt(np.mean(np.square(real[idx] - gm_p[idx])))/t, 3))
        rm_rmse.append(round(np.sqrt(np.mean(np.square(real[idx] - rm[idx])))/t, 3))

    fig, ax1 = plt.subplots()
    lw = 1
    colors = ['orangered', 'hotpink', 'limegreen', 'skyblue']
    #l1, = ax1.plot(ts, gnn_10_rmse, color=colors[0], linewidth=lw, alpha=0.7, label='GNN_10')
    #l2, = ax1.plot(ts, gnn_20_rmse, color=colors[1], linewidth=lw, alpha=0.7, label='GNN_20')
    l1, = ax1.plot(ts, rm_rmse, color=colors[0], linewidth=lw, alpha=1, label='RM')
    l2, = ax1.plot(ts, gm_p_rmse, color=colors[1], linewidth=lw, alpha=1, label='GM_P')
    l3, = ax1.plot(ts, gnn_30_rmse, color=colors[2], linewidth=lw, alpha=0.7, label='GNN_30')
    l4, = ax1.plot(ts, gcn_rmse, color=colors[3], linewidth=lw, alpha=1, label='SI-GCN')

    ax1.set_xlabel('Intensity threshold')
    ax1.set_ylabel('Relative RMSE')
    ax1.set_xlim(30, 100)
    #ax1.set_ylim(20, 110)
    ax1.legend([l1, l2, l3, l4], labels=['RM', 'GM_P', 'GNN_30', 'SI-GCN'], loc='upper right', #bbox_to_anchor=(0.97, 0.61),
               borderaxespad=0.1, ncol=1)
    plt.show()


def training_size():
    ticks = ['RMSE', 'MAPE', 'SCC', 'CPC']
    RMSE = [[27.122, 27.293, 27.498, 28.772, 28.869, 28.107, 27.311, 28.663, 27.937, 27.914],
            [24.512, 25.531, 25.367, 25.322, 25.531, 25.367, 25.394, 25.242, 25.288, 25.296],
            [20.516, 20.62, 20.854, 20.191, 21.055, 20.826, 20.546, 21.049, 20.893],
            [18.398, 18.505, 18.66, 18.56, 18.405, 18.419, 18.315, 18.556, 18.503, 18.583]]

    MAPE = [[29.1, 29.1, 28.6, 28.1, 27.7, 28.9, 27.9, 28.1, 27.8, 28.1],
            [25.4, 25.3, 24.8, 25.1, 25.3, 24.8, 25.4, 25.6, 24.8, 26.4],
            [23.4, 23.1, 22.5, 22.6, 22.6, 22.9, 23.6, 22.5, 23.7],
            [22.8, 21.6, 22.6, 22.3, 22.1, 22.8, 22.8, 22.5, 23.4, 23.2]]

    SCC = [[0.558, 0.555, 0.549, 0.526, 0.53, 0.534, 0.55, 0.526, 0.546, 0.546],
           [0.636, 0.628, 0.639, 0.625, 0.628, 0.639, 0.635, 0.638, 0.631, 0.632],
           [0.709, 0.708, 0.716, 0.715, 0.713, 0.701, 0.703, 0.702, 0.712],
           [0.718, 0.722, 0.723, 0.725, 0.728, 0.719, 0.718, 0.719, 0.72, 0.727]]

    CPC = [[0.846, 0.845, 0.844, 0.839, 0.839, 0.841, 0.844, 0.838, 0.842, 0.842],
           [0.866, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.864],
           [0.884, 0.883, 0.884, 0.886, 0.884, 0.882, 0.883, 0.882, 0.882],
           [0.888, 0.889, 0.889, 0.889, 0.889, 0.889, 0.889, 0.888, 0.887, 0.888]]

    p20 = [[27.122, 27.293, 27.498, 28.772, 28.869, 28.107, 27.311, 28.663, 27.937, 27.914],
           [29.1, 29.1, 28.6, 28.1, 27.7, 28.9, 27.9, 28.1, 27.8, 28.1],
           [0.558, 0.555, 0.549, 0.526, 0.53, 0.534, 0.55, 0.526, 0.546, 0.546],
           [0.846, 0.845, 0.844, 0.839, 0.839, 0.841, 0.844, 0.838, 0.842, 0.842]]

    p40 = [[24.512, 25.531, 25.367, 25.322, 25.531, 25.367, 25.394, 25.242, 25.288, 25.296],
           [25.4, 25.3, 24.8, 25.1, 25.3, 24.8, 25.4, 25.6, 24.8, 26.4],
           [0.636, 0.628, 0.639, 0.625, 0.628, 0.639, 0.635, 0.638, 0.631, 0.632],
           [0.866, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.864]]

    p60 = [[20.516, 20.62, 20.854, 20.191, 21.055, 20.826, 20.546, 21.049, 20.893],
           [23.4, 23.1, 22.5, 22.6, 22.6, 22.9, 23.6, 22.5, 23.7],
           [0.709, 0.708, 0.716, 0.715, 0.713, 0.701, 0.703, 0.702, 0.712],
           [0.884, 0.883, 0.884, 0.886, 0.884, 0.882, 0.883, 0.882, 0.882]]

    p80 = [[18.398, 18.505, 18.66, 18.56, 18.405, 18.419, 18.315, 18.556, 18.503, 18.583],
           [22.8, 21.6, 22.6, 22.3, 22.1, 22.8, 22.8, 22.5, 23.4, 23.2],
           [0.718, 0.722, 0.723, 0.725, 0.728, 0.719, 0.718, 0.719, 0.72, 0.727],
           [0.888, 0.889, 0.889, 0.889, 0.889, 0.889, 0.889, 0.888, 0.887, 0.888]]

    #t = [p20, p40, p60, p80]
    t = [RMSE, MAPE, SCC, CPC]
    #fs1 = 10
    #fs2 = 8

    fig, ax = plt.subplots(figsize=(6, 3))
    colors = ['#fdae61', '#1b7837', '#7fbf7b', '#762a83']

    ax.set_xlabel('Training set size') #fontsize=fs1
    ax.set_ylabel('Performance')
    xs = np.array([0.5, 1.5, 2.5, 3.5])
    #xs = np.array([-3, -1, 1, 3])

    def set_box_color(bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color=color)

    bw = 0.1
    margin = 0.05

    bp = ax.boxplot(t[0], positions=[0.35, 0.45, 0.55, 0.65], sym='', widths=bw)
    set_box_color(bp, colors[0])

    bp = ax.boxplot(t[1], positions=[1.35, 1.45, 1.55, 1.65], sym='', widths=bw)
    set_box_color(bp, colors[1])

    #for n, i in enumerate([0.5, 1.5]):
    #    bp = ax.boxplot(t[n], positions=0.5 + (bw + margin / 2) * xs / 2, sym='', widths=bw)
    #    set_box_color(bp, colors[n])

    ax.set_xlim(0, 4)
    ax.set_xticks(xs)
    ax.xaxis.set_ticklabels(ticks)

    ax.set_ylim(18, 30)
    #ys = [0, 5, 10, 15, 20, 25, 30, 35]
    #ax.set_yticks(ys)
    #ylabels = [str(item) for item in ys]
    #ax.yaxis.set_ticklabels(ylabels, fontsize=fs2)

    ax1 = ax.twinx()
    bp = ax1.boxplot(t[2], positions=[2.35, 2.45, 2.55, 2.65], sym='', widths=bw)
    set_box_color(bp, colors[2])
    bp = ax1.boxplot(t[3], positions=[3.35, 3.45, 3.55, 3.65], sym='', widths=bw)
    set_box_color(bp, colors[3])
    #for n, i in enumerate([1, 3]):
    #    bp = ax1.boxplot(t[n+2], positions=xs + (bw + margin / 2) * i / 2, sym='', widths=bw)
    #    set_box_color(bp, colors[n+2])
    ax.set_xlim(0, 4)
    ax1.set_xticks(xs)
    ax1.xaxis.set_ticklabels(ticks)
    ax1.set_ylim(0.5, 1)

    pc = ['20%', '40%', '60%', '80%']
    for i in range(4):
        ax.plot([], c=colors[i], label=pc[i])
    ax.legend()

    plt.show()


def tt():
    RMSE = [[27.122, 27.293, 27.498, 28.772, 28.869, 28.107, 27.311, 28.663, 27.937, 27.914],
                     [24.512, 25.531, 25.367, 25.322, 25.531, 25.367, 25.394, 25.242, 25.288, 25.296],
                     [20.516, 20.620, 20.854, 20.191, 21.055, 20.826, 20.546, 21.049, 20.893, 20.728],
                     [18.398, 18.505, 18.660, 18.560, 18.405, 18.419, 18.315, 18.556, 18.503, 18.583]]

    MAPE = [[29.1, 29.1, 28.6, 28.1, 27.7, 28.9, 27.9, 28.1, 27.8, 28.1],
                     [25.4, 25.3, 24.8, 25.1, 25.3, 24.8, 25.4, 25.6, 24.8, 26.4],
                     [23.4, 23.1, 22.5, 22.6, 22.6, 22.9, 23.6, 22.5, 23.7, 23.0],
                     [22.8, 21.6, 22.6, 22.3, 22.1, 22.8, 22.8, 22.5, 23.4, 23.2]]

    SCC = [[0.558, 0.555, 0.549, 0.526, 0.530, 0.534, 0.550, 0.526, 0.546, 0.546],
                    [0.636, 0.628, 0.639, 0.625, 0.628, 0.639, 0.635, 0.638, 0.631, 0.632],
                    [0.709, 0.708, 0.716, 0.715, 0.713, 0.701, 0.703, 0.702, 0.712, 0.709],
                    [0.718, 0.722, 0.723, 0.725, 0.728, 0.719, 0.718, 0.719, 0.720, 0.727]]

    CPC = [[0.846, 0.845, 0.844, 0.839, 0.839, 0.841, 0.844, 0.838, 0.842, 0.842],
                    [0.866, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.864],
                    [0.884, 0.883, 0.884, 0.886, 0.884, 0.882, 0.883, 0.882, 0.882, 0.883],
                    [0.888, 0.889, 0.889, 0.889, 0.889, 0.889, 0.889, 0.888, 0.887, 0.888]]

    def set_box_color(bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color=color)

    xs = [1, 2, 3, 4]

    lw = 1
    colors = ['orangered', 'hotpink', 'limegreen', 'skyblue']
    colors = ['gray']*4
    plt.figure()

    plt.subplot(1, 4, 1)
    bp = plt.boxplot(RMSE, sym='', widths=0.5)
    set_box_color(bp, colors[0])
    plt.ylim(18, 30)
    plt.ylabel('RMSE')

    plt.subplot(1, 4, 2)
    bp = plt.boxplot(MAPE, sym='', widths=0.5)
    set_box_color(bp, colors[1])
    plt.ylim(22, 30)
    plt.ylabel('MAPE')

    plt.subplot(1, 4, 3)
    bp = plt.boxplot(SCC, sym='', widths=0.5)
    set_box_color(bp, colors[2])
    plt.ylim(0.5, 0.75)
    plt.ylabel('SCC')

    plt.subplot(1, 4, 4)
    bp = plt.boxplot(CPC, sym='', widths=0.5)
    set_box_color(bp, colors[3])
    plt.ylim(0.83, 0.89)
    plt.ylabel('CPC')

    plt.show()


def tt1():
    RMSE = np.array([[27.122, 27.293, 27.498, 28.772, 28.869, 28.107, 27.311, 28.663, 27.937, 27.914],
                     [24.512, 25.531, 25.367, 25.322, 25.531, 25.367, 25.394, 25.242, 25.288, 25.296],
                     [20.516, 20.620, 20.854, 20.191, 21.055, 20.826, 20.546, 21.049, 20.893, 20.728],
                     [18.398, 18.505, 18.660, 18.560, 18.405, 18.419, 18.315, 18.556, 18.503, 18.583]])

    MAPE = np.array([[29.1, 29.1, 28.6, 28.1, 27.7, 28.9, 27.9, 28.1, 27.8, 28.1],
                     [25.4, 25.3, 24.8, 25.1, 25.3, 24.8, 25.4, 25.6, 24.8, 26.4],
                     [23.4, 23.1, 22.5, 22.6, 22.6, 22.9, 23.6, 22.5, 23.7, 23.0],
                     [22.8, 21.6, 22.6, 22.3, 22.1, 22.8, 22.8, 22.5, 23.4, 23.2]])

    SCC = np.array([[0.558, 0.555, 0.549, 0.526, 0.530, 0.534, 0.550, 0.526, 0.546, 0.546],
                    [0.636, 0.628, 0.639, 0.625, 0.628, 0.639, 0.635, 0.638, 0.631, 0.632],
                    [0.709, 0.708, 0.716, 0.715, 0.713, 0.701, 0.703, 0.702, 0.712, 0.709],
                    [0.718, 0.722, 0.723, 0.725, 0.728, 0.719, 0.718, 0.719, 0.720, 0.727]])

    CPC = np.array([[0.846, 0.845, 0.844, 0.839, 0.839, 0.841, 0.844, 0.838, 0.842, 0.842],
                    [0.866, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.864],
                    [0.884, 0.883, 0.884, 0.886, 0.884, 0.882, 0.883, 0.882, 0.882, 0.883],
                    [0.888, 0.889, 0.889, 0.889, 0.889, 0.889, 0.889, 0.888, 0.887, 0.888]])

    RMSE = np.mean(RMSE, axis=1)
    MAPE = np.mean(MAPE, axis=1)
    SCC = np.mean(SCC, axis=1)
    CPC = np.mean(CPC, axis=1)

    xs = [1, 2, 3, 4]

    lw = 0.8
    ms = 6
    colors = ['orangered', 'hotpink', 'limegreen', 'skyblue']
    fig, ax1 = plt.subplots()
    l1, = ax1.plot(xs, RMSE, '--', marker='<', markersize=ms, color=colors[0], linewidth=lw, alpha=0.5, label='RMSE')
    l2, = ax1.plot(xs, MAPE, '--', marker='s', markersize=ms, color=colors[1], linewidth=lw, alpha=0.5, label='MAPE')
    l3, = ax1.plot(0, 0, '--', marker='D', markersize=ms, color=colors[2], linewidth=lw, alpha=0.5, label='SCC')
    l4, = ax1.plot(0, 0, '--', marker='o', markersize=ms, color=colors[3], linewidth=lw, alpha=0.5, label='CPC')
    ax1.set_ylabel('RMSE & MAPE(%)', fontname = 'Arial')
    ax1.set_ylim(18, 30)
    ax1.set_xlabel('Training set size', fontname='Arial')
    ax2 = ax1.twinx()
    l3, = ax2.plot(xs, SCC, '--', marker='D', markersize=ms, color=colors[2], linewidth=lw, alpha=0.5, label='SCC')
    l4, = ax2.plot(xs, CPC, '--', marker='o', markersize=ms, color=colors[3], linewidth=lw, alpha=0.5, label='CPC')

    ax2.set_ylabel('SCC & CPC', fontname = 'Arial')
    ax2.set_xticks(xs)
    ax2.xaxis.set_ticklabels(['20%', '40%', '60%', '80%'])
    ax2.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9])
    ax2.set_ylim(0.5, 0.9)
    ax2.set_xlim(0.9, 4.1)

    ax1.legend([l1, l2, l3, l4], labels=['RMSE', 'MAPE', 'SCC', 'CPC'], bbox_to_anchor=(0.22, 0.61), borderaxespad=0.1, ncol=1)
    #.legend([l3, l4], labels=['SCC', 'CPC'], bbox_to_anchor=(0.2, 0.55), borderaxespad=0.1, ncol=1)

    plt.show()


def tt2():
    RMSE = np.array([[27.122, 27.293, 27.498, 28.772, 28.869, 28.107, 27.311, 28.663, 27.937, 27.914],
                     [24.512, 25.531, 25.367, 25.322, 25.531, 25.367, 25.394, 25.242, 25.288, 25.296],
                     [20.516, 20.620, 20.854, 20.191, 21.055, 20.826, 20.546, 21.049, 20.893, 20.728],
                     [18.398, 18.505, 18.660, 18.560, 18.405, 18.419, 18.315, 18.556, 18.503, 18.583]])

    MAPE = np.array([[29.1, 29.1, 28.6, 28.1, 27.7, 28.9, 27.9, 28.1, 27.8, 28.1],
                     [25.4, 25.3, 24.8, 25.1, 25.3, 24.8, 25.4, 25.6, 24.8, 26.4],
                     [23.4, 23.1, 22.5, 22.6, 22.6, 22.9, 23.6, 22.5, 23.7, 23.0],
                     [22.8, 21.6, 22.6, 22.3, 22.1, 22.8, 22.8, 22.5, 23.4, 23.2]])

    SCC = np.array([[0.558, 0.555, 0.549, 0.526, 0.530, 0.534, 0.550, 0.526, 0.546, 0.546],
                    [0.636, 0.628, 0.639, 0.625, 0.628, 0.639, 0.635, 0.638, 0.631, 0.632],
                    [0.709, 0.708, 0.716, 0.715, 0.713, 0.701, 0.703, 0.702, 0.712, 0.709],
                    [0.718, 0.722, 0.723, 0.725, 0.728, 0.719, 0.718, 0.719, 0.720, 0.727]])

    CPC = np.array([[0.846, 0.845, 0.844, 0.839, 0.839, 0.841, 0.844, 0.838, 0.842, 0.842],
                    [0.866, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.863, 0.864],
                    [0.884, 0.883, 0.884, 0.886, 0.884, 0.882, 0.883, 0.882, 0.882, 0.883],
                    [0.888, 0.889, 0.889, 0.889, 0.889, 0.889, 0.889, 0.888, 0.887, 0.888]])

    RMSE_mean = np.mean(RMSE, axis=1)
    MAPE_mean = np.mean(MAPE, axis=1)
    SCC_mean = np.mean(SCC, axis=1)
    CPC_mean = np.mean(CPC, axis=1)

    RMSE_err = np.std(RMSE, axis=1)
    SCC_err = np.std(SCC, axis=1)

    xs = [1, 2, 3, 4]

    lw = 0.6
    colors = ['orangered', 'hotpink', 'limegreen', 'skyblue']
    fig, ax1 = plt.subplots()
    l1 = ax1.errorbar(xs, RMSE_mean, yerr=RMSE_err, ecolor=colors[0], elinewidth=1, linewidth=lw, linestyle='--',
                 color=colors[0], capsize=2)
    l3 = ax1.errorbar(xs, SCC_mean, yerr=SCC_err, ecolor=colors[2], elinewidth=1, linewidth=lw, linestyle='--',
                      color=colors[2], capsize=2)
    ax1.set_ylabel('RMSE', fontname = 'Arial')
    ax1.set_ylim(18, 29)
    ax1.set_xlabel('Training set size', fontname='Arial')
    ax2 = ax1.twinx()
    l3 = ax2.errorbar(xs, SCC_mean, yerr=SCC_err, ecolor=colors[2], elinewidth=1, linewidth=lw, linestyle='--',
                 color=colors[2], capsize=2)
    ax2.set_ylabel('SCC', fontname = 'Arial')
    ax2.set_xticks(xs)
    ax2.xaxis.set_ticklabels(['20%', '40%', '60%', '80%'])
    ax2.set_yticks([0.5, 0.55, 0.6, 0.65, 0.7, 0.75])
    ax2.set_ylim(0.5, 0.75)
    ax2.set_xlim(0.9, 4.1)

    ax1.legend([l1, l3], labels=['RMSE', 'SCC'], bbox_to_anchor=(0.22, 0.61), borderaxespad=0.1, ncol=1)

    plt.show()


if __name__ == '__main__':
    #iter_rmse_scc()
    #check()
    #var_threshold()
    #training_size()
    tt2()