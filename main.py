import generate_csv as gs
import sortP as sortP
import threading
import queue
import csv
import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from ctypes import *

lib = CDLL("./sortCPP.dll")
lib.ExternalSort.argtypes = [c_char_p, c_int, c_bool]
lib.ExternalSort.restype = None

filename = "data.csv"
stop = False

def workerAnimation(targetFunc, callback):
    res = targetFunc()
    root.after(0, lambda: finishAnimation(res, callback))

def finishAnimation(res, callback):
    loading_progress.stop()
    loading_frame.place_forget()
    callback(res)

def runAnimation(targetFunc, name:str, callback):
    loading_label.config(text=name)
    loading_frame.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
    loading_progress.start(10)
    threading.Thread(target=workerAnimation, args=(targetFunc, callback), daemon=True).start()

def splitStr(c):
    s = str()
    for i in c:
        s1 = str(i)
        s += s1 + ' ' * (25 - len(s1))
    return s

def checkFile(filename:str):
    if os.path.exists(filename):
        return True
    else:
        output.insert(tk.END, filename + " - не найден" + "\n\n")
        output.see(tk.END)
        return False

def outFile(filename:str, last:bool):
    with open(filename, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        output.insert(tk.END, splitStr(next(reader)) + "\n")
        output.see(tk.END)
        if last:
            q = queue.Queue()
            for row in reader:
                if q.qsize() == 10:
                    q.get()
                q.put(row)
            while not q.empty():
                output.insert(tk.END, splitStr(q.get()) + "\n")
                output.see(tk.END)
        else:
            for i in range(10):
                output.insert(tk.END, splitStr(next(reader)) + "\n")
                output.see(tk.END)
        output.insert(tk.END, "\n")
        output.see(tk.END)

def sortThread(s1, column, rev):
    start = time.time()
    if s1 == 0:
        lib.ExternalSort(filename.encode(), column, rev)
    elif s1 == 1:
        sortP.ExternalSort(filename, column, rev)
    end = time.time()
    return end - start

def sortComplete(res):
    global stop
    if res > 60:
        output.insert(tk.END, "Файл отсортирован за " + str(int(res // 60)) + " минут(ы) " + str(round(res % 60, 3)) + " секунд\n\n")
    else:
        output.insert(tk.END, "Файл отсортирован за " + str(round(res % 60, 3)) + " секунд\n\n")
    output.see(tk.END)
    stop = False

def SORT(column:int):
    global stop
    if not(checkFile(filename)) or stop:
        return
    s = lib_choice1.get()
    t = lib_choice2.get()
    if s == "C++":
        if t == "По возрастанию":
            s1 = 0
            rev = False
        elif t == "По убыванию":
            s1 = 0
            rev = True
    elif s == "Python":
        if t == "По возрастанию":
            s1 = 1
            rev = False
        elif t == "По убыванию":
            s1 = 1
            rev = True
    stop = True
    runAnimation(lambda: sortThread(s1, column, rev), "Сортировка...", sortComplete)

def out(o:int):
    if stop:
        return
    global filename
    s = lib_choice3.get()
    if o == 0:
        if s == "Неотсортированный файл":
            if checkFile(filename):
                outFile(filename, False)
        elif s == "Отсортированный файл":
            filename1 = filename.replace(".csv", ".txt")
            if checkFile(filename1):
                outFile(filename1, False)
    elif o == 1:
        if s == "Неотсортированный файл":
            if checkFile(filename):
                outFile(filename, True)
        elif s == "Отсортированный файл":
            filename1 = filename.replace(".csv", ".txt")
            if checkFile(filename1):
                outFile(filename1, True)

def generateThread(size):
    start = time.time()
    gs.generate_memory(size, filename)
    end = time.time()
    return end - start

def generateComplete(res):
    global stop
    if res > 60:
        output.insert(tk.END, "Файл создан за " + str(int(res // 60)) + " минут(ы) " + str(round(res % 60, 3)) + " секунд\n\n")
    else:
        output.insert(tk.END, "Файл создан за " + str(round(res % 60, 3)) + " секунд\n\n")
    output.see(tk.END)
    stop = False

def GenerateCSV():
    global stop
    if stop:
        return
    DEL()
    try:
        size = float(entryMemory.get())
        entryMemory.delete(0, tk.END)
    except ValueError:
        output.insert(tk.END, "Неверно указан размер файла\n\n")
        output.see(tk.END)
        entryMemory.delete(0, tk.END)
        return
    if size < 0.00001:
        output.insert(tk.END, "Размер файла слишком малый\n\n")
        output.see(tk.END)
        return
    elif size > 20:
        output.insert(tk.END, "Размер файла слишком большой\n\n")
        output.see(tk.END)
        return
    stop = True
    runAnimation(lambda: generateThread(size), "Генерация файла...", generateComplete)

def DEL():
    if stop:
        return
    try:
        os.remove(filename)
    except:
        pass
    try:
        os.remove(filename.replace(".csv", ".txt"))
    except:
        pass

root = tk.Tk()
root.geometry("1600x900")
root.title("Сортировка файла")

generane_frame = tk.Frame(root, relief=tk.RAISED, bd=2, width=200, height=150)
generane_frame.place(relx=0.12, rely=0.1, anchor=tk.CENTER)
tk.Label(generane_frame, text="Генерация файла").place(relx=0.5, rely=0.1, anchor=tk.CENTER)
tk.Label(generane_frame, text="Размер файла(в гб.):").place(relx=0.5, rely=0.25, anchor=tk.CENTER)
entryMemory = tk.Entry(generane_frame)
entryMemory.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
tk.Button(generane_frame, text = "Сгенерировать", command = GenerateCSV).place(relx=0.5, rely=0.6, anchor=tk.CENTER)
tk.Button(generane_frame, text = "Удалить файлы", command = DEL).place(relx=0.5, rely=0.85, anchor=tk.CENTER)

sort_frame = tk.Frame(root, relief=tk.RAISED, bd=2, width=800, height=150)
sort_frame.place(relx=0.45, rely=0.1, anchor=tk.CENTER)
tk.Label(sort_frame, text="Выбор сортировки:").place(relx=0.42, rely=0.1, anchor=tk.CENTER)
lib_choice1 = tk.StringVar()
lib_combo1 = ttk.Combobox(sort_frame, textvariable=lib_choice1, values=["C++", "Python"], state="readonly", width=20)
lib_combo1.place(relx=0.6, rely=0.1, anchor=tk.CENTER)
lib_combo1.current(0)
tk.Label(sort_frame, text="Выбор ключа сортировки:").place(relx=0.4, rely=0.4, anchor=tk.CENTER)
lib_choice2 = tk.StringVar()
lib_combo2 = ttk.Combobox(sort_frame, textvariable=lib_choice2, values=["По возрастанию", "По убыванию"], state="readonly", width=20)
lib_combo2.place(relx=0.6, rely=0.4, anchor=tk.CENTER)
lib_combo2.current(0)
tk.Button(sort_frame, text = "По дате", command = lambda: SORT(0)).place(relx=0.12, rely=0.8, anchor=tk.CENTER)
tk.Button(sort_frame, text = "По фамилии и имени", command = lambda: SORT(1)).place(relx=0.26, rely=0.8, anchor=tk.CENTER)
tk.Button(sort_frame, text = "По выходу на поле", command = lambda: SORT(2)).place(relx=0.44, rely=0.8, anchor=tk.CENTER)
tk.Button(sort_frame, text = "По количеству голов", command = lambda: SORT(3)).place(relx=0.62, rely=0.8, anchor=tk.CENTER)
tk.Button(sort_frame, text = "По пройденной дистанции", command = lambda: SORT(4)).place(relx=0.82, rely=0.8, anchor=tk.CENTER)

out_frame = tk.Frame(root, relief=tk.RAISED, bd=2, width=400, height=150)
out_frame.place(relx=0.843, rely=0.1, anchor=tk.CENTER)
tk.Label(out_frame, text="Вывод строк из файла").place(relx=0.5, rely=0.1, anchor=tk.CENTER)
lib_choice3 = tk.StringVar()
lib_combo3 = ttk.Combobox(out_frame, textvariable=lib_choice3, values=["Неотсортированный файл", "Отсортированный файл"], state="readonly", width=25)
lib_combo3.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
lib_combo3.current(0)
tk.Button(out_frame, text = "Первые 10 строк", command = lambda: out(0)).place(relx=0.3, rely=0.8, anchor=tk.CENTER)
tk.Button(out_frame, text = "Последние 10 строк", command = lambda: out(1)).place(relx=0.7, rely=0.8, anchor=tk.CENTER)

output = ScrolledText(root, width=200, height=35, font=("Courier New", 9))
output.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

loading_frame = tk.Frame(root)
loading_label = tk.Label(loading_frame)
loading_progress = ttk.Progressbar(loading_frame, mode='indeterminate', length=300)
loading_label.pack(padx=0, pady=5)
loading_progress.pack()

root.mainloop()