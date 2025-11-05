import numpy as np
import math

# Forward Mode Automatic Differentiation
class DualNumber:
    def __init__(self, value, derivative=0.0):
        self.value = float(value)
        self.derivative = float(derivative)

    def __add__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other)
        return DualNumber(self.value + other.value, self.derivative + other.derivative)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other)
        return DualNumber(self.value - other.value, self.derivative - other.derivative)

    def __rsub__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other)
        return DualNumber(other.value - self.value, other.derivative - self.derivative)

    def __mul__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other)
        return DualNumber(
            self.value * other.value,
            self.value * other.derivative + self.derivative * other.value
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other)
        return DualNumber(
            self.value / other.value,
            (self.derivative * other.value - self.value * other.derivative) / (other.value ** 2)
        )

    def __rtruediv__(self, other):
        other = other if isinstance(other, DualNumber) else DualNumber(other)
        return other.__truediv__(self)

    def __pow__(self, power):
        return DualNumber(
            self.value ** power,
            power * (self.value ** (power - 1)) * self.derivative
        )

    def sin(self):
        import math
        return DualNumber(math.sin(self.value), math.cos(self.value) * self.derivative)

    def __repr__(self):
        return f"DualNumber(value={self.value:.4f}, derivative={self.derivative:.4f})"

def f_forward(x):
    # Example function: f(x) = x^2 + 3x + 2
    return x ** 2 + 3 * x + 2


# Forward mode test
x = DualNumber(5.0, derivative=1.0)  # we want df/dx
y = f_forward(x)
print("Forward mode result:")
print("f(x):", y.value)
print("df/dx:", y.derivative)


# Reverse Mode Automatic Differentiation
class Node:
    def __init__(self, value, parents=(), grad_fn=None):
        self.value = float(value)
        self.parents = parents  # list of (parent_node, gradient w.r.t parent)
        self.grad = 0.0
        self.grad_fn = grad_fn

    def backward(self, grad_output=1.0):
        self.grad += grad_output
        for parent, grad_fn in self.parents:
            parent.backward(grad_output * grad_fn)

    def __add__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        return Node(self.value + other.value,
                    parents=[(self, 1.0), (other, 1.0)])

    def __sub__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        return Node(self.value - other.value,
                    parents=[(self, 1.0), (other, -1.0)])

    def __mul__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        return Node(self.value * other.value,
                    parents=[(self, other.value), (other, self.value)])

    def __truediv__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        return Node(self.value / other.value,
                    parents=[(self, 1.0 / other.value),
                             (other, -self.value / (other.value ** 2))])

    def __pow__(self, power):
        return Node(self.value ** power,
                    parents=[(self, power * (self.value ** (power - 1)))])

    def sin(self):
        return Node(math.sin(self.value), [(self, math.cos(self.value))])
    
    def __repr__(self):
        return f"Node(value={self.value:.4f}, grad={self.grad:.4f})"


def f_reverse(x):
    # Example: f(x) = x^2 + 3x + 2
    return (x ** 2) + (x * 3.0) + 2.0


# Reverse mode test
x = Node(5.0)
y = f_reverse(x)
y.backward()  # start backpropagation
print("\nReverse mode result:")
print("f(x):", y.value)
print("df/dx:", x.grad)
