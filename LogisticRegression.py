import numpy as np
import matplotlib.pyplot as plt

mean_1 = np.array([1, 0.5])
cov_1 = np.array([[1, 0.1],
                  [0.1, 1.2]])

mean_2 = np.array([4, 5])
cov_2 = np.array([[1.21, 0.1],
                  [0.1, 1.3]])

dist_01 = np.random.multivariate_normal(mean_1, cov_1, 500)
dist_02 = np.random.multivariate_normal(mean_2, cov_2, 500)

data = np.zeros((1000, 3))
data[:500, :2] = dist_01
data[500:, :2] = dist_02
data[500:, -1] = 1.0

np.random.shuffle(data)
split = int(.8 * data.shape[0])

X_train = data[:split, :-1]
X_test = data[split:, :-1]

Y_train = data[:split, -1]
Y_test = data[split:, -1]


def hypothesis(x, w, b):
    h = np.dot(x, w) + b
    return sigmoid(h)


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-1.0 * z))


def error(y_true, x, w, b):
    m = x.shape[0]
    err = 0.0

    for i in range(m):
        hx = hypothesis(x[i], w, b)
        err += y_true[i] * np.log2(hx) + (1 - y_true[i]) * np.log2(1 - hx)

    return -err / m


def get_grads(y_true, x, w, b):
    grad_w = np.zeros(w.shape)
    grad_b = 0.0

    m = x.shape[0]

    for i in range(m):
        hx = hypothesis(x[i], w, b)
        grad_w += (y_true[i] - hx) * x[i]
        grad_b += (y_true[i] - hx)

    grad_b /= m
    grad_w /= m
    return [grad_w, grad_b]


def grad_descent(x, y_true, w, b, learning_rate=0.1):
    err = error(y_true, x, w, b)
    [grad_w, grad_b] = get_grads(y_true, x, w, b)

    w = w + learning_rate * grad_w
    b = b + learning_rate * grad_b

    return err, w, b


def predict(x, w, b):
    confidence = hypothesis(x, w, b)

    if confidence < 0.5:
        return 0
    else:
        return 1


def get_acc(x_tst, y_tst, w, b):
    y_pred = []

    for i in range(y_tst.shape[0]):
        p = predict(x_tst[i], w, b)
        y_pred.append(p)

    y_pred = np.array(y_pred)
    return float((y_pred == y_tst).sum()) / y_tst.shape[0]


loss = []
acc = []

W = np.random.random((dist_01.shape[1],))
b = np.random.random()

for i in range(1000):
    l, W, b = grad_descent(X_train, Y_train, W, b, learning_rate=0.5)
    acc.append(get_acc(X_test, Y_test, W, b))
    loss.append(l)

plt.scatter(dist_01[:, 0], dist_01[:, 1])
plt.scatter(dist_02[:, 0], dist_02[:, 1], color='orange')
x = np.linspace(-4, 8, 10)
y = - (W[0] * x + b) / W[1]
plt.plot(x, y, color='black')
plt.show()
