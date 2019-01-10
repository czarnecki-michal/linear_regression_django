from linear_regression import LinearRegression, plot_regression_line
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    reg = LinearRegression()
    data = pd.read_csv("salary.csv")
    x = data["workedYears"][:47].values
    y = data["salaryBrutto"][:47].values
    reg.fit(x, y)
    x_pred = data["workedYears"][47:].values
    y_pred = reg.predict(x_pred)

    reg.print_results(x_pred, y_pred)

    predicted_plot = plt.scatter(x_pred, y_pred, color = "b", marker = "o", zorder = 10, label = "Przewidywane zarobki/lata pracy")
    plot_regression_line(x, y, reg.coef, x_label = "workedYears", y_label = "salaryBrutto", title = "Przewidywanie zarobków za pomocą regresji liniowej")
    plt.legend(handles=[predicted_plot])
    plt.show()

if __name__ == "__main__":
    main()

