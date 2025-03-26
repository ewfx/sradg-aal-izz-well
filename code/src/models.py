import numpy as np

def linear_model(x, a, b): return a * x + b

def sin_model(x, a, b, c): return a * np.sin(b * x + c)

def quadratic_model(x, a, b, c): return a * x**2 + b * x + c

def log_model(x, a, b): return a * np.log(x + 1) + b
