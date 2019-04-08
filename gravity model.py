
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from func import *

def gravity_model_linear(flows, features):
    Y = []
    X = []
    feature_size = len(list(features.values())[0])
    if feature_size == 3:
        for k in flows:
            if k[2]:
                Y.append(np.log(features[k[0]][2] * features[k[1]][2] / k[2]))
                X.append(np.log(dis(features[k[0]][0], features[k[0]][1], features[k[1]][0], features[k[1]][1])))
    elif feature_size == 4:
        for k in flows:
            if k[2]:
                Y.append(np.log(features[k[0]][3] * features[k[1]][2] / k[2]))
                X.append(np.log(dis(features[k[0]][0], features[k[0]][1], features[k[1]][0], features[k[1]][1])))

    p = np.polyfit(X, Y, 1)
    beta = p[0]
    K = np.e**(-p[1])

    #p1 = plt.scatter(X, Y, marker='.', color='green', s=10)
    #plt.show()

    return beta, K


def predict_linear(flows, features, beta, K):
    p = []
    r = []
    feature_size = len(list(features.values())[0])
    if feature_size == 3:
        for f in flows:
            p.append(K * features[f[0]][2] * features[f[1]][2] / dis(features[f[0]][0], features[f[0]][1],
                                                                     features[f[1]][0], features[f[1]][1]) ** beta)
            r.append(f[2])
    elif feature_size == 4:
        for f in flows:
            p.append(K * features[f[0]][3] * features[f[1]][2] / dis(features[f[0]][0], features[f[0]][1],
                                                                     features[f[1]][0], features[f[1]][1]) ** beta)
            r.append(f[2])

    return p, r


def gravity_model(flows, features):
    Y = []
    X = []
    feature_size = len(list(features.values())[0])
    if feature_size == 3:
        for k in flows:
            if k[2]:
                Y.append(np.log(k[2]))
                X.append([np.log(features[k[0]][2]), np.log(features[k[1]][2]),
                          np.log(dis(features[k[0]][0], features[k[0]][1], features[k[1]][0], features[k[1]][1]))])
    elif feature_size == 4:
        for k in flows:
            if k[2]:
                Y.append(np.log(k[2]))
                X.append([np.log(features[k[0]][3]), np.log(features[k[1]][2]),
                          np.log(dis(features[k[0]][0], features[k[0]][1], features[k[1]][0], features[k[1]][1]))])

    reg = LinearRegression().fit(X, Y)
    beta = reg.coef_
    K = np.e**reg.intercept_

    #p1 = plt.scatter(X, Y, marker='.', color='green', s=10)
    #plt.show()

    return beta, K


def predict(flows, features, beta, K):
    p = []
    r = []
    feature_size = len(list(features.values())[0])
    if feature_size == 3:
        for f in flows:
            p.append(K * (features[f[0]][2] ** beta[0]) * (features[f[1]][2] ** beta[1]) *
                     (dis(features[f[0]][0], features[f[0]][1], features[f[1]][0], features[f[1]][1]) ** beta[2]))
            r.append(f[2])
    elif feature_size == 4:
        for f in flows:
            p.append(K * (features[f[0]][3]**beta[0]) * (features[f[1]][2]**beta[1]) *
                     (dis(features[f[0]][0], features[f[0]][1], features[f[1]][0], features[f[1]][1]) ** beta[2]))
            r.append(f[2])

    print('\nnum of test flows:', len(r))
    print('real_min:', min(r), ', real_max:', max(r))
    print('pred_min:', int(min(p)), ', pred_max:', int(max(p)))
    print('real:', r[0:20])
    print('pred:', list(map(int, p[0:20])))

    return p, r


if __name__ == '__main__':

    col_num = 30
    path = 'SI-GCN/data/taxi/'
    tr_f = read_flows(path + 'train.txt')
    te_f = read_flows(path + 'test.txt')
    #v_f = read_flows(path + 'valid.txt')
    features = read_features(path + 'entities.dict', path + 'features_raw.txt')

    beta, K = gravity_model_linear(tr_f, features)
    print('beta =', beta, ', K =', K)
    pred, real = predict_linear(te_f, features, beta, K)
    evaluate(pred, real)
