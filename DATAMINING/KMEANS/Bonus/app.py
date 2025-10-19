from model import model_SL_predict, get_model_SL
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk 
from tkinter import filedialog, messagebox

def prepare_model(model):
    for c in set(model.columns) :       
        model[c] = model[c].apply(lambda x : tuple(x.tolist()) if isinstance(x,np.ndarray) else x)
        model[c] = model[c].apply(lambda x : tuple(x) if isinstance(x,list) else x)
    return model
def run_terminal():
    fname = input("input model(.parquet) filepath without '.parquet'  : ")
    fname+=".parquet"
    model = pd.read_parquet(fname)
    model = prepare_model(model)
    tps = model["TYPE"].unique()
    for i,t in enumerate(tps):
        print(f"{i} - [{t}]")
    choice_t : int = None
    while(choice_t == None):
        choice_t = input("Pick one : ")
        choice_t = int(choice_t)
        if choice_t < 0 or choice_t >= len(tps):
            print("wrong pick again.")
            choice_t = None
    picked_t = tps[choice_t]
    print("you pick choice : ",picked_t)
    locs = model["LOC"].loc[model["TYPE"] == tps[choice_t]].unique()
    choice_l : int = None
    for i,t in enumerate(locs):
        print(f"{i} - [{t}]")
    while(choice_l == None):
        choice_l = input("Pick one : ")
        choice_l = int(choice_l)
        if choice_l <= 0 or choice_l >= len(locs):
            print("wrong pick again.")
            choice_l = None
    picked_l = locs[choice_l]
    print("you pick choice : ",picked_l)
    loop = True
    while(loop):
        print("Format : [area-terrain-dispo-neuf-chambre-piece-floor-floors]")
        input_point = input("Input : ")
        try :
            dataPt = tuple(map(float, input_point.split("-")))
            #dataPt = tuple(map(float, input_point.split("-")))
            cat = tuple([str(picked_t),str(picked_l)])
            data = {
                "CAT" : cat,
                "POINT" : dataPt
            }
            predicted_price = model_SL_predict(model = model, data=data )
            if predicted_price :
                predicted_price = next(iter(predicted_price))
            print(f"Predicted price : {int(predicted_price)} EUR")
            loop = False
        except Exception :
            print(f"[ERROR] received {input_point}")

def open_model():
    path = filedialog.askopenfilename(
        title="Choose a .parquet file",
        filetypes=[("Parquet files", "*.parquet"), ("All files", "*.*")]
    )
    if not path:
        return None
    try:
        df = pd.read_parquet(path)
        return prepare_model(df)
    except Exception as e:
        messagebox.showerror("Error loading file", str(e))
        return None

FIELD_ORDER = [
    ("area",   "Area (m²)"),
    ("terrain","Terrain (m²)"),
    ("dispo",  "Disponible (0/1)"),
    ("neuf",   "Neuf (0/1)"),
    ("chambre","Chambres"),
    ("piece",  "Pièces"),
    ("floor",  "Étage"),
    ("floors", "Nb étages (immeuble)"),
]

def run_interface():
    root = tk.Tk()
    root.title("Predict")
    root.geometry("540x520")
    status = tk.StringVar(value="No file selected")
    model = None
    ttk.Button(root, text="Open model.parquet", command=lambda: on_open()).pack(pady=(10,6))
    ttk.Label(root, textvariable=status).pack(pady=(0,10))
    ttk.Label(root, text="TYPE").pack()
    tps_var = tk.StringVar()
    tps_cb  = ttk.Combobox(root, textvariable=tps_var, state="disabled")
    tps_cb.pack(padx=10, pady=(0,8), fill="x")
    ttk.Label(root, text="LOC").pack()
    locs_var = tk.StringVar()
    locs_cb  = ttk.Combobox(root, textvariable=locs_var, state="disabled")
    locs_cb.pack(padx=10, pady=(0,10), fill="x")
    inputs = {}
    frm = ttk.Frame(root)
    frm.pack(padx=10, pady=6, fill="x")
    for key, label in FIELD_ORDER:
        row = ttk.Frame(frm)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=label, width=28, anchor="w").pack(side="left")
        ent = ttk.Entry(row, width=20)
        ent.pack(side="left", fill="x", expand=True)
        inputs[key] = ent
    result_var = tk.StringVar(value="Predicted price: —")
    ttk.Button(root, text="Predict", command=lambda: on_predict()).pack(pady=(10,4))
    ttk.Label(root, textvariable=result_var, font=("Arial", 12, "bold")).pack(pady=(2,12))
    ttk.Button(root, text="Quit", command=root.destroy).pack(pady=6)
    def populate_types():
        nonlocal model
        tps = list(map(str, pd.unique(model["TYPE"])))
        tps_cb.configure(values=tps, state="readonly")
        if tps:
            tps_cb.current(0)
            on_type_change()
    def on_type_change(event=None):
        nonlocal model
        chosen_type = tps_var.get()
        locs = list(map(str, pd.unique(model.loc[model["TYPE"] == chosen_type, "LOC"])))
        locs_cb.configure(values=locs, state="readonly")
        if locs:
            locs_cb.current(0)
    tps_cb.bind("<<ComboboxSelected>>", on_type_change)
    def on_open():
        nonlocal model
        m = open_model()
        if m is None:
            return
        model = m
        status.set(f"Model loaded ✔  ({len(model):,} rows)")
        populate_types()
    def on_predict():
        if model is None:
            messagebox.showwarning("No model", "Load a .parquet model first.")
            return
        picked_t = tps_var.get()
        picked_l = locs_var.get()
        if not picked_t or not picked_l:
            messagebox.showwarning("Missing selection", "Pick TYPE and LOC.")
            return
        try:
            values = []
            for key, _ in FIELD_ORDER:
                txt = inputs[key].get().strip()
                values.append(float(txt))
            if len(values) != 8:
                raise ValueError
        except Exception:
            messagebox.showerror(
                "Invalid input",
                "Enter 8 numeric values: area-terrain-dispo-neuf-chambre-piece-floor-floors"
            )
            return

        data = {
            "CAT": (str(picked_t), str(picked_l)),
            "POINT": tuple(values)
        }
        try:
            predicted_price = model_SL_predict(model=model, data=data)
            if predicted_price:
                predicted_price = next(iter(predicted_price))
            result_var.set(f"Predicted price: {int(predicted_price):,} EUR".replace(",", " "))
        except Exception as e:
            messagebox.showerror("Prediction error", str(e))

    root.mainloop()

if __name__ == "__main__":
    run_interface()