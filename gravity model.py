
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def read_data(filename):
    flows = np.loadtxt(filename, dtype=np.uint16, delimiter='\t')[:,[0,2,3]]
    attraction = {}

    for f in flows:
        if f[0] not in attraction:
            attraction[f[0]] = 0
        attraction[f[0]] += f[2]
        if f[1] not in attraction:
            attraction[f[1]] = 0
        attraction[f[1]] += f[2]

    return flows, attraction


def merge_attraction(entity_file, tr_a, te_a, v_a):
    gids = []
    with open(entity_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            gids.append(int(line.strip().split('\t')[-1]))

    attraction = {}
    for gid in gids:
        attraction[gid] = 0
        if gid in tr_a:
            attraction[gid] += tr_a[gid]
        if gid in te_a:
            attraction[gid] += te_a[gid]
        if gid in v_a:
            attraction[gid] += v_a[gid]
    return attraction


def grid_dis(i, j, colnum):
    x0 = int(i) % colnum
    y0 = int(i) // colnum
    x1 = int(j) % colnum
    y1 = int(j) // colnum
    return np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)


def gravity_model(flows, attraction, colnum):
    Y = []
    X = []
    for k in flows:
        if k[2]:
            #print(k)
            Y.append(np.log(attraction[k[0]]*attraction[k[1]]/k[2]))
            X.append(np.log(grid_dis(k[0], k[1], colnum)))

    p = np.polyfit(X, Y, 1)
    beta = p[0]
    K = np.e**(-p[1])
    '''
    p1 = plt.scatter(X, Y, marker='.', color='green', s=10)
    plt.show()
    '''
    return beta, K


def evaluate(flows, attraction, beta, K, colnum):
    p = []
    r = []
    for f in flows:
        p.append(K * attraction[f[0]] * attraction[f[1]] / grid_dis(f[0], f[1], colnum) ** beta)
        r.append(f[2])

    print('\nnum of test flows:', len(r))
    print('real_min:', min(r), ', real_max:', max(r))
    print('pred_min:', int(min(p)), ', pred_max:', int(max(p)))
    print('real:', r[:20])
    print('pred:', list(map(int, p[:20])))

    p = np.array(p)
    r = np.array(r)

    print('MAE\t', round(np.mean(np.abs(r - p)),3))

    c1 = 0
    mape = 0
    c2 = 0
    ssi = 0
    for i in range(p.shape[0]):
        if r[i]:
            mape += np.abs((r[i] - p[i]) / r[i])
            c1 += 1
        if r[i] + p[i]:
            ssi += min(r[i], p[i]) / (r[i] + p[i])
            c2 += 1
    print('MAPE:', round(mape * 100 / c1, 3))

    print('MSE:', round(np.mean(np.square(r - p)), 3))
    print('RMSE:', round(np.sqrt(np.mean(np.square(r - p))), 3))

    stack = np.column_stack((p, r))
    print('CPC:', round(2 * np.sum(np.min(stack, axis=1)) / np.sum(stack), 3))

    print('SSI:', round(ssi * 2 / (c2 ^ 2), 3))

    smc = stats.spearmanr(r, p)
    print('SMC: correlation =', round(smc[0], 3), ', p-value =', round(smc[1], 3))

    llr = stats.linregress(r, p)
    print('LLR: R =', round(llr[2], 3), ', p-value =', round(llr[3], 3))
    # p1 = plt.scatter(p, r, marker='.', color='green', s=10)
    # plt.show()


if __name__ == '__main__':
    colnum = 25
    path = 'SI-GCN/data/taxi/'
    tr_f, tr_a = read_data(path + 'train.txt')
    te_f, te_a = read_data(path + 'test.txt')
    v_f, v_a = read_data(path + 'valid.txt')
    attraction = merge_attraction(path + 'entities.dict', tr_a, te_a, v_a)

    beta, K = gravity_model(tr_f, attraction, colnum)
    print('beta =', beta, ', K =', K)

    evaluate(te_f, attraction, beta, K, colnum)