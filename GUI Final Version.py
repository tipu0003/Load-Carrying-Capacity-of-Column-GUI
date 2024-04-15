import pickle
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from xgboost import XGBRegressor
import unicodeit

# Load and preprocess dataset
data = pd.read_excel("Dataset.xlsx")
X = data.iloc[:, :-1]  # Assuming all other columns are features
y = data.iloc[:, -1]  # Assuming the last column is the target

# Load the trained XGBRegressor model
with open('PGLU_DNN_Pu.pkl', 'rb') as model_file:
    xgboost_loaded = pickle.load(model_file)

# tkinter GUI
root = tk.Tk()
root.title(f"Prediction of {unicodeit.replace('P_u')}")

canvas1 = tk.Canvas(root, width=650, height=550)
canvas1.configure(background='#e9ecef')
canvas1.pack()

# label0 = tk.Label(root, text='Developed by Mr. Rupesh Kumar', font=('Times New Roman', 15, 'bold'), bg='#e9ecef')
# canvas1.create_window(20, 20, anchor="w", window=label0)
#
# label_phd = tk.Label(root, text='*K. R. Mangalam University, India, Email: tipu0003@gmail.com',
#                      font=('Futura Md Bt', 12), bg='#e9ecef')
# canvas1.create_window(20, 50, anchor="w", window=label_phd)

label_input = tk.Label(root, text='Input Variables', font=('Times New Roman', 12, 'bold', 'italic', 'underline'),
                       bg='#e9ecef')
canvas1.create_window(10, 70, anchor="w", window=label_input)

# Labels and entry boxes
labels = ['Concrete strength (MPa)', 'Height of column (mm)', 'Diameter of outer steel tube (from outer to outer) (mm)',
          'Diameter of outer steel tube (from inner to inner) (mm)', 'Yield strength of outer steel tube (MPa)',
          'Yield strength of longitudinal reinforcing rebars (MPa)', r'Ratio of longitudinal reinforcing rebars (\rho_{v})',
          r'Volumetric ratio of circular/spiral reinforcing rebars (k_{es} × \rho_{h})', 'Yield strength of circular/spiral reinforcing '
                                                                    'rebars (MPa)',
          'Total area of internal reinforcing steel section (mm\u00b2)', 'Yield strength of internal reinforcing '
                                                                         'steel section (MPa)', 'Eccentricity (mm)'
          ]

entry_boxes = []
for i, label_text in enumerate(labels):
    label = tk.Label(root, text=unicodeit.replace(label_text), font=('Times New Roman', 12, 'italic'), bg='#e9ecef', pady=5)
    canvas1.create_window(20, 100 + i * 30, anchor="w", window=label)

    entry = tk.Entry(root)
    canvas1.create_window(520, 100 + i * 30, window=entry)
    entry_boxes.append(entry)

# Normal text label
label_output1 = tk.Label(root, text='Load Carrying Capacity,', font=('Times New Roman', 12, 'bold'), bg='#e9ecef')
canvas1.create_window(50, 510, anchor="nw", window=label_output1)

# Italic text label for "P_u"
label_output2 = tk.Label(root, text=f'{unicodeit.replace("P_u")}', font=('Times New Roman', 12, 'italic'), bg='#e9ecef')
# Calculating the width of the first label to position the second one correctly
label_output1.update_idletasks()  # Update "requested size" from Tkinter's geometry manager
offset = label_output1.winfo_reqwidth()
canvas1.create_window(50 + offset, 510, anchor="nw", window=label_output2)


def values():
    # Validate and get the values from the entry boxes
    input_values = []
    for entry_box in entry_boxes:
        value = entry_box.get().strip()
        if value:
            try:
                input_values.append(float(value))
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter valid numeric values.")
                return
        else:
            messagebox.showerror("Error", "Please fill in all the input fields.")
            return

    # If all input values are valid, proceed with prediction
    input_data = pd.DataFrame([input_values],
                              columns=X.columns)

    # Predict using the loaded XGBRegressor model
    prediction_result = xgboost_loaded.predict(input_data)
    prediction_result = round(prediction_result[0], 2)

    # Display the prediction on the GUI
    label_prediction = tk.Label(root, text=f'{prediction_result:.2f} kN', font=('Times New Roman', 20, 'bold'), bg='white')
    canvas1.create_window(300, 520, anchor="w", window=label_prediction)


button1 = tk.Button(root, text='Predict', command=values, bg='#4285f4', fg='white', font=('Times New Roman', 12,'bold'),
                    bd=3, relief='ridge')
canvas1.create_window(480, 520, anchor="w", window=button1)

root.mainloop()
