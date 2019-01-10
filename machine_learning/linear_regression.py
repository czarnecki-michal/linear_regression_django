import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_regression_line(x, y, coef, x_label = "", y_label = "", title = ""): 
    """Wyrysowuje linię regresji
    x - zmienne niezależne (features)
    y - zmienne zależne (labels)
    coef - lista współczynników regresji 
    """
    y_pred = coef[0] * x + coef[1]

    plt.scatter(x, y, color = "gray", marker = ".", s = 30) 
    plt.plot(x, y_pred, color = "g", zorder = 0, linewidth=0.5) 

    plt.text(4, 11000, "f(x) = " + str(round(coef[0], 4)) + " x + " + str(round(coef[1], 4)))
    plt.xlabel(x_label) 
    plt.ylabel(y_label) 
    plt.title(title)

class LinearRegression:
    coef = []
    r_squared = 0

    def fit(self, x, y):  
        """Oblicza współczynniki regresji potrzebne to wyznaczenia lini regresji i oszacowania wartości
        x - zmienne niezależne (features)
        y - zmienne zależne (labels)
        """
        x_mean, y_mean = np.mean(x), np.mean(y)
        xy_mean, x2_mean = np.mean(x*y), np.mean(x**2)
    
        a = (x_mean * y_mean - xy_mean) / (x_mean**2 - x2_mean)
        b = y_mean - a * x_mean
    
        self.coef = [a, b]

    def predict(self, x):
        """Przewiduje brakujące wartości na postawie danych wejściowych i zwraca listę
        x - zmienne niezależne (features)
        """
        return [int(self.coef[0] * value + self.coef[1]) for value in x]
    
    def calculate_error(self, y, y_pred):
        """Na postawie części danych, które są kompletne oblicza współczynnik determinacji
        y - rzeczywista wartość zmiennej Y
        y_pred - wartość teoretyczna (przewidywana) zmiennej
        """

        SSres = pow(y - y_pred, 2) # suma kwadratów dla modelu
        SStot = pow(y - np.mean(y), 2) # suma kwadratów całkowita
        self.r_squared = 1 - sum(SSres)/sum(SStot) # współczynnik determinacji

        return self.r_squared

    def print_results(self, x, y):
        print("Współczynnik kierunkowy: {}\nWyraz wolny: {} \nWspółczynnik determinacji R^2: {}".format(round(self.coef[0], 5), round(self.coef[1], 5), round(self.r_squared, 5)))

        print("\t", "workedYears", "\t", "salaryBrutto", "\n", "\t", "-----------", "\t", "------------")
        for i in range(len(y)):
            print("\t", x[i], "\t\t", y[i])