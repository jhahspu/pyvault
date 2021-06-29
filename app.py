import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import messagebox, filedialog
import sqlite3
import random


conn = sqlite3.connect("pyvault.db")
# TEST IN MEMORY (uncommenct next line)
# conn = sqlite3.connect(":memory:")
c = conn.cursor()
CREATE_TBL = """
CREATE TABLE data (
  app varchar(100),
  username varchar(50),
  password varchar(20),
  details varchar(200)
)
"""
# c.execute(CREATE_TBL)
# conn.commit()


def selected_row(event):
  print("[double clicked a row] ")
  # rowid = trv.identify_row(event.y)
  item = trv.item(trv.focus())
  # item['values'][0]
  e1.set(item['values'][0])
  e2.set(item['values'][1])
  e3.set(item['values'][2])
  e4.set(item['values'][3])

def search_all():
  pass

def get_all():
  c.execute("""
  SELECT * FROM data
  """
  )
  rows = c.fetchall()
  trv.delete(*trv.get_children())
  for i in rows:
    trv.insert('', 'end', values=i)

def app_add():
  with conn:
    c.execute("""
    INSERT INTO data
      VALUES (:app, :username, :password, :details)
    """, {'app': e1.get(), 'username': e2.get(), 'password': e3.get(), 'details': e4.get()}
    )
  get_all()

def app_update():
  with conn:
    c.execute("""
    UPDATE data
      SET password=:password, details=:details
      WHERE app=:app
      AND username=:username
    """, {'app': e1.get(), 'username': e2.get(), 'password': e3.get(), 'details': e4.get()}
    )
  get_all()

def app_delete():
  if messagebox.askyesno("Confirmation needed", "Are you sure you to delete App?"):
    with conn:
      c.execute("""
      DELETE FROM data
        WHERE app=:app
        AND username=:username
      """, {'app': e1.get(), 'username': e2.get()}
      )
    get_all()

def generate_password():
  choice = random.SystemRandom().choice
  lowercase = 'abcdefghijklmnopqrstuvwxyz'
  uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  digits = '0123456789'
  punctuation = '!#$%&()*+,-./:;<=>?@[]^_{|}~' # excluded \' and "
  allowed = lowercase + uppercase + digits + punctuation
  password_chars = [
    choice(lowercase),
    choice(uppercase),
    choice(digits),
    choice(punctuation)
  ] + random.sample(allowed, 14)
  res = ''.join(password_chars)
  e3.set(res)


root = tk.Tk()

wrapper1 = tk.LabelFrame(root, text="List")
wrapper2 = tk.LabelFrame(root, text="Search")
wrapper3 = tk.LabelFrame(root, text="Update")

wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

# List: Wrapper 1
trv = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4), show="headings", height="6")
trv.heading(1, text="App")
trv.heading(2, text="Username")
trv.heading(3, text="Password")
trv.heading(4, text="Details")
trv.pack()

trv.bind('<Double 1>', selected_row)

# Search: Wrapper 2
lbl = tk.Label(wrapper2, text="Search")
lbl.pack(side=tk.LEFT, padx=10)

q = StringVar()
ent = tk.Entry(wrapper2, textvariable=q)
ent.pack(side=tk.LEFT, padx=6)

btn = tk.Button(wrapper2, text="Search", command=search_all)
btn.pack(side=tk.LEFT, padx=6)

cbtn = tk.Button(wrapper2, text="Clear", command=get_all)
cbtn.pack(side=tk.LEFT, padx=6)

# Update: Wrapper 3
e1 = StringVar()
lbl1 = tk.Label(wrapper3, text="App")
lbl1.grid(row=0, column=0, padx=5, pady=3)
ent1 = tk.Entry(wrapper3, textvariable=e1)
ent1.grid(row=0, column=1, padx=5, pady=3)


e2 = StringVar()
lbl2 = tk.Label(wrapper3, text="Username")
lbl2.grid(row=1, column=0, padx=5, pady=3)
ent2 = tk.Entry(wrapper3, textvariable=e2)
ent2.grid(row=1, column=1, padx=5, pady=3)


e3 = StringVar()
lbl3 = tk.Label(wrapper3, text="Password")
lbl3.grid(row=2, column=0, padx=5, pady=3)
ent3 = tk.Entry(wrapper3, textvariable=e3)
ent3.grid(row=2, column=1, padx=5, pady=3)
passBtn = tk.Button(wrapper3, text="Generate", command=generate_password)
passBtn.grid(row=2, column=2, padx=5, pady=3)


e4 = StringVar()
lbl4 = tk.Label(wrapper3, text="Details")
lbl4.grid(row=3, column=0, padx=5, pady=3)
ent4 = tk.Entry(wrapper3, textvariable=e4)
ent4.grid(row=3, column=1, padx=5, pady=3)


addBtn = tk.Button(wrapper3, text="Create", command=app_add)
addBtn.grid(row=5, column=1, padx=5, pady=3)

updateBtn = tk.Button(wrapper3, text="Update", command=app_update)
updateBtn.grid(row=5, column=2, padx=5, pady=3)

deleteBtn = tk.Button(wrapper3, text="Detele", command=app_delete)
deleteBtn.grid(row=5, column=3, padx=5, pady=3)

get_all()

root.title("Py Vault")
root.geometry("800x700")
root.mainloop()

conn.close()