import math
import numpy as np
import matplotlib.pyplot as plt
from main import Node

# 3-Layer Feedforward Neural Network
def forward_3layer(x_node, W1_nodes, b1_nodes, W2_nodes, b2_nodes, W3_nodes, b3_node):
    # 3-layer NN:
    #   Layer1: h1 = sin(x * W1 + b1)
    #   Layer2: h2 = sin(h1 * W2 + b2)
    #   Output: y  = sum(h2_i * W3_i) + b3

    h1 = [(x_node * W1_nodes[i] + b1_nodes[i]).sin() for i in range(len(W1_nodes))]

    h2 = []
    for j in range(len(b2_nodes)):
        z = Node(0.0)
        for i in range(len(W1_nodes)):
            z = z + h1[i] * W2_nodes[i][j]
        z = z + b2_nodes[j]
        h2.append(z.sin())

    y = Node(0.0)
    for k in range(len(W3_nodes)):
        y = y + h2[k] * W3_nodes[k]
    y = y + b3_node

    return y


np.random.seed(0)

# Data: y = sin(x) + small noise
X = np.linspace(-2 * math.pi, 2 * math.pi, 80)
Y = np.sin(X) + 0.1 * np.random.randn(len(X))

hidden1 = 8
hidden2 = 8
W1 = [Node(np.random.randn() * 0.5) for _ in range(hidden1)]
b1 = [Node(0.0) for _ in range(hidden1)]
W2 = [[Node(np.random.randn() * 0.5) for _ in range(hidden2)] for _ in range(hidden1)]
b2 = [Node(0.0) for _ in range(hidden2)]
W3 = [Node(np.random.randn() * 0.5) for _ in range(hidden2)]
b3 = Node(0.0)

params = sum(W2, []) + W1 + b1 + b2 + W3 + [b3]

# Hyperparameters
lr = 0.01
epochs = 1000
grad_flow = []

for epoch in range(epochs):
    total_loss = 0.0
    grads_per_epoch = []

    for x_val, y_true in zip(X, Y):
        x = Node(x_val)
        y_pred = forward_3layer(x, W1, b1, W2, b2, W3, b3)
        loss = (y_pred - y_true) ** 2
        total_loss += loss.value

        loss.backward()

        grads_per_epoch.append(np.mean([abs(p.grad) for p in params]))

        for p in params:
            p.value -= lr * p.grad

        def reset(node, seen=set()):
            if node in seen:
                return
            seen.add(node)
            node.grad = 0.0
            for parent, _ in node.parents:
                reset(parent, seen)
        reset(loss)

    grad_flow.append(np.mean(grads_per_epoch))

    if epoch % 100 == 0:
        print(f"Epoch {epoch:4d} | Loss {total_loss/len(X):.6f}")

# Evaluate model after training
y_preds = []
for x_val in X:
    x = Node(x_val)
    y_pred = forward_3layer(x, W1, b1, W2, b2, W3, b3)
    y_preds.append(y_pred.value)

# Plot results
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.title("Autodiff fitting sin(x)")
plt.scatter(X, Y, s=15, alpha=0.6, label="Data")
plt.plot(X, y_preds, 'r', label="Prediction")
plt.legend()

plt.subplot(1, 2, 2)
plt.title("Gradient Flow over Epochs")
plt.plot(grad_flow)
plt.xlabel("Epoch")
plt.ylabel("Mean Gradient")

plt.tight_layout()
plt.show()