from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
import math
import numpy as np
import tkinter as tk
from tkinter import ttk

from help import on_select

app = tk.Tk()
app.title("SVR")
app.minsize(800, 500)
app.configure(bg="lightblue")
style = ttk.Style(app)


def on_selection(combo: Any) -> None:
    selected_item = combo.get()
    print("Selected item:", selected_item)
    print("Option number:", combo
          )


label = tk.Label(app, text="combo:", font=('bold', 20), foreground="black", background="lightblue", padx=5, pady=5)
label.grid(row=11, column=0)

choices = [
    (1, "combo1"),
    (2, "combo2"),
    (3, "combo3"),
    (4, "combo4")
]

combobox = ttk.Combobox(app, values=[choice[1] for choice in choices])
combobox.grid(row=11, column=1)

combobox.bind("<<ComboboxSelected>>", on_selection)

bw_text = tk.DoubleVar(value=305)
bw_label = tk.Label(app, text="bw", font=('bold', 20), foreground="black", background="lightblue", padx=5, pady=5)
bw_label.grid(row=1, column=0)
bw_entry = tk.Entry(app, textvariable=bw_text, width=30)
bw_entry.grid(row=1, column=1)
bw_unit = tk.Label(app, text="mm", font=('bold', 20), foreground="black", background="lightblue", padx=5, pady=5)
bw_unit.grid(row=1, column=2)

d_text = tk.DoubleVar(value=368)
d_label = tk.Label(app, text="d", font=('bold', 20), foreground="black", background="lightblue", padx=5, pady=5)
d_label.grid(row=2, column=0)
d_entry = tk.Entry(app, textvariable=d_text, width=30)
d_entry.grid(row=2, column=1)
d_unit = tk.Label(app, text="mm", font=('bold', 20), foreground="black", background="lightblue", padx=5, pady=5)
d_unit.grid(row=2, column=2)

fck_text = tk.DoubleVar(value=14.5)
fck_label = tk.Label(app, text="fck", font=('bold', 20), foreground="black", background="lightblue", padx=5, pady=5)
fck_label.grid(row=3, column=0)
fck_entry = tk.Entry(app, textvariable=fck_text, width=30)
fck_entry.grid(row=3, column=1)
fck_unit = tk.Label(app, text="MPa", font=('bold', 20), foreground="black", background="lightblue", padx=5, pady=5)
fck_unit.grid(row=3, column=2)

fy_text = tk.DoubleVar(value=383)
fy_label = tk.Label(app, text="fy", font=('bold', 20), foreground="black", background="lightblue", padx=5, pady=5)
fy_label.grid(row=4, column=0)
fy_entry = tk.Entry(app, textvariable=fy_text, width=30)
fy_entry.grid(row=4, column=1)
fy_unit = tk.Label(app, text="MPa", font=('bold', 20), foreground="black", background="lightblue", padx=5, pady=5)
fy_unit.grid(row=4, column=2)

pw_text = tk.DoubleVar()
pw_text.set(1.58)
pw_label = tk.Label(app, text="pw", font=('bold', 20), foreground="black", background="lightblue", padx=5, pady=5)
pw_label.grid(row=5, column=0)
pw_entry = tk.Entry(app, textvariable=pw_text, width=30)
pw_entry.grid(row=5, column=1)

a_d_ratio_text = tk.DoubleVar()
a_d_ratio_text.set(0)
a_d_ratio_label = tk.Label(app, text="a/d ratio", font=('bold', 20), foreground="black", background="lightblue", padx=5,
                           pady=5)
a_d_ratio_label.grid(row=6, column=0)
a_d_ratio_entry = tk.Entry(app, textvariable=a_d_ratio_text, width=30)
a_d_ratio_entry.grid(row=6, column=1)

# Load the dataset
df = pd.read_csv('shear.csv', encoding='latin-1', skiprows=[1, 2])
df.head()


def getval():
    global combobox
    if combobox == 1:
        # Separate the input features and target variable
        X1 = df.iloc[3:1199, [5, 8]].values
        y = df.iloc[3:1199, 21].values
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X1, y, test_size=0.2)
        # Feature scaling - Standardization
        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train)

        # Train the SVR model
        kernel = RBF(length_scale=5.0)
        regressor = GaussianProcessRegressor(kernel=kernel)
        regressor.fit(X_train, y_train)
        # Predict on the testing set
        y_pre = regressor.predict(X_test)
        # Model evaluation
        mse = mean_squared_error(y_test, y_pre)
        r2 = r2_score(y_test, y_pre)
        print('Mean Squared Error:', mse)
        print('R-squared:', r2)

        # Creating an instance of GPR with RBF kernel and fitting the model on the data
        gpr = GaussianProcessRegressor(kernel=RBF(length_scale=5.0))
        gpr.fit(X_train_scaled, y_train)
        # Predicting on test data using both models
        gpr_pre = gpr.predict(X_test)
        X1_new = np.array([bw_text.get(), d_text.get()]).reshape(1, -1)
        Y1 = gpr.predict(X1_new)
        print(gpr_pre)
        print(Y1)
        ss_label = tk.Label(app, text="Predicted shear strength =", font=('bold', 20), foreground="black",
                            background="lightblue", padx=5, pady=5)
        ss_label.grid(row=19, column=0)
        ss_label = tk.Label(app, text=Y1, font=('normal', 20), foreground="black", background="lightblue", padx=5,
                            pady=5)
        ss_label.grid(row=19, column=2)
        print(regressor.score(X_test, y_test))

    if combobox == 2:
        # Separate the input features and target variable
        X2 = df.iloc[3:1199, [5, 8, 15]].values
        y = df.iloc[3:1199, 21].values
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X2, y, test_size=0.2, random_state=42)
        # Feature scaling - Standardization
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        # Train the SVR model
        kernel = RBF(length_scale=5)
        regressor = GaussianProcessRegressor(kernel=kernel)
        regressor.fit(X_train_scaled, y_train)
        # Predict on the testing set
        y_pre = regressor.predict(X_test_scaled)
        # Model evaluation
        mse = mean_squared_error(y_test, y_pre)
        r2 = r2_score(y_test, y_pre)
        print('Mean Squared Error:', mse)
        print('R-squared:', r2)

        # Creating an instance of GPR with RBF kernel and fitting the model on the data
        gpr = GaussianProcessRegressor(kernel=RBF(length_scale=5))
        gpr.fit(X_train_scaled, y_train)
        # Predicting on test data using both models
        gpr_pre = gpr.predict(X_test)
        X2_new = np.array([bw_text.get(), d_text.get(), math.sqrt(fck_text.get())]).reshape(1, -1)
        Y2 = gpr.predict(X2_new)
        print(gpr_pre)
        print(Y2)
        ss_label = tk.Label(app, text="Predicted shear strength =", font=('bold', 20), foreground="black",
                            background="lightblue", padx=5, pady=5)
        ss_label.grid(row=19, column=0)
        ss_label = tk.Label(app, text=Y2, font=('normal', 20), foreground="black", background="lightblue", padx=5,
                            pady=5)
        ss_label.grid(row=19, column=2)
        print(regressor.score(X_test, y_test))

    if combobox == 3:
        # Separate the input features and target variable
        X3 = df.iloc[3:1199, [5, 8, 15, 17, 13]].values
        y = df.iloc[3:1199, 21].values
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X3, y, test_size=0.2, random_state=42)
        # Feature scaling - Standardization
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        # Train the SVR model
        kernel = RBF(length_scale=0.01)
        regressor = GaussianProcessRegressor(kernel=kernel)
        regressor.fit(X_train_scaled, y_train)
        # Predict on the testing set
        y_pre = regressor.predict(X_test_scaled)
        # Model evaluation
        mse = mean_squared_error(y_test, y_pre)
        r2 = r2_score(y_test, y_pre)
        print('Mean Squared Error:', mse)
        print('R-squared:', r2)

        # Creating an instance of GPR with RBF kernel and fitting the model on the data
        gpr = GaussianProcessRegressor(kernel=RBF(length_scale=0.01))
        gpr.fit(X_train_scaled, y_train)
        # Predicting on test data using both models
        gpr_pre = gpr.predict(X_test)
        X3_new = np.array(
            [bw_text.get(), d_text.get(), math.sqrt(fck_text.get()), pw_text.get(), fy_text.get()]).reshape(1, -1)
        Y3 = gpr.predict(X3_new)
        print(gpr_pre)
        print(Y3)
        ss_label = tk.Label(app, text="Predicted shear strength =", font=('bold', 20), foreground="black",
                            background="lightblue", padx=5, pady=5)
        ss_label.grid(row=19, column=0)
        ss_label = tk.Label(app, text=Y3, font=('normal', 20), foreground="black", background="lightblue", padx=5,
                            pady=5)
        ss_label.grid(row=19, column=2)
        print(regressor.score(X_test, y_test))

    if combobox == 4:
        # Separate the input features and target variable
        X4 = df.iloc[3:1199, [5, 8, 15, 12, 17, 13]].values
        y = df.iloc[3:1199, 21].values
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X4, y, test_size=0.2, random_state=42)
        # Feature scaling - Standardization
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        # Train the SVR model
        kernel = RBF(length_scale=5)
        regressor = GaussianProcessRegressor(kernel=kernel)
        regressor.fit(X_train_scaled, y_train)
        # Predict on the testing set
        y_pre = regressor.predict(X_test_scaled)
        # Model evaluation
        mse = mean_squared_error(y_test, y_pre)
        r2 = r2_score(y_test, y_pre)
        print('Mean Squared Error:', mse)
        print('R-squared:', r2)

        # Creating an instance of GPR with RBF kernel and fitting the model on the data
        gpr = GaussianProcessRegressor(kernel=RBF(length_scale=5))
        gpr.fit(X_train_scaled, y_train)
        # Predicting on test data using both models
        gpr_pre = gpr.predict(X_test)
        X4_new = np.array([bw_text.get(), d_text.get(), math.sqrt(fck_text.get()), pw_text.get(), fy_text.get(),
                           a_d_ratio_text.get()]).reshape(1, -1)
        Y4 = gpr.predict(X4_new)
        print(gpr_pre)
        print(Y4)
        ss_label = tk.Label(app, text="Predicted shear strength =", font=('bold', 20), foreground="black",
                            background="lightblue", padx=5, pady=5)
        ss_label.grid(row=19, column=0)
        ss_label = tk.Label(app, text=Y4, font=('normal', 20), foreground="black", background="lightblue", padx=5,
                            pady=5)
        ss_label.grid(row=19, column=2)
        print(regressor.score(X_test, y_test))


button1 = tk.Button(app, text="Run", width=15, bg='#03A9F4', fg='#fff', command=getval)
# button1.pack()
button1.grid(row=16, column=2, padx=10, pady=10)

app.mainloop()
