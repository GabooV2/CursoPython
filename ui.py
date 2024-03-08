import helpers
import database as db
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING


class CenterWidgetMixin():
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry(f"{w}x{h}+{x}+{y}")


class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear Cliente")
        self.build()
        self.center()
        # Me permite bloquear la ventana principal para no tocar ninguna funcion de la misma junto con grab_set()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        Label(frame, text="DNI (2 int y 1 upper char)").grid(row=0, column=0)
        Label(frame, text="Nombre (De 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (De 2 a 30 chars)").grid(row=0, column=2)

        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 1))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 2))

        frame = Frame(self)
        frame.pack(pady=10)

        crear = Button(frame, text="Crear", command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        self.validaciones = [0, 0, 0]
        self.crear = crear
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def create_client(self):
        self.master.treeview.insert(
                parent="", index="end", iid=self.dni.get(),
                values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):
        valor = event.widget.get()
        # if index == 0:
        #     valido = helpers.validar_dni(valor, db.Clientes.lista)
        #     if valido:
        #         event.widget.configure({"bg": "limegreen"})
        #     else:
        #         event.widget.configure({"bg": "crimson"})
        # if index == 1:
        #     valido = valor.isalpha() and len(valor) >= 2 and len(valor) <= 30
        #     if valido:
        #         event.widget.configure({"bg": "limegreen"})
        #     else:
        #         event.widget.configure({"bg": "crimson"})
        # if index == 2:
        #     valido = valor.isalpha() and len(valor) >= 2 and len(valor) <= 30
        #     if valido:
        #         event.widget.configure({"bg": "limegreen"})
        #     else:
        #         event.widget.configure({"bg": "crimson"})

        valido = helpers.validar_dni(valor, db.Clientes.lista) if index == 0 else valor.isalpha(
        ) and len(valor) >= 2 and len(valor) <= 30
        event.widget.configure({"bg": "limegreen" if valido else "crimson"})

        # Cambiar el estado del boton "crear" de acuerdo a las validaciones
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones == [1,1,1] else DISABLED)
        

class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Modificar Cliente")
        self.build()
        self.center()
        # Me permite bloquear la ventana principal para no tocar ninguna funcion de la misma junto con grab_set()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        Label(frame, text="DNI (no editable)").grid(row=0, column=0)
        Label(frame, text="Nombre (De 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (De 2 a 30 chars)").grid(row=0, column=2)

        dni = Entry(frame)
        dni.grid(row=1, column=0)
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        cliente = self.master.treeview.focus()
        campos = self.master.treeview.item(cliente, "values")
        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        frame = Frame(self)
        frame.pack(pady=10)

        modificar = Button(frame, text="Modificar", command=self.edit_client)
        modificar.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        self.validaciones = [1, 1]
        self.modificar = modificar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def edit_client(self):
        cliente = self.master.treeview.focus()
        self.master.treeview.item(cliente, values=(
            self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):
        valor = event.widget.get()
        valido = (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.configure({"bg": "limegreen" if valido else "crimson"})

        # Cambiar el estado del boton "crear" de acuerdo a las validaciones
        self.validaciones[index] = valido
        self.modificar.config(state=NORMAL if self.validaciones == [1,1] else DISABLED)


class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Clientes")
        self.build()
        self.center()

    def build(self):
        frame = Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame)
        treeview["columns"] = ("DNI", "Nombre", "Apellido")

        treeview.column("#0", width=0, stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)

        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        treeview["yscrollcommand"] = scrollbar.set

        for cliente in db.Clientes.lista:
            treeview.insert(
                parent="", index="end", iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido))

        treeview.pack()

        frame = Frame(self)
        frame.pack(pady=20)

        Button(frame, text="Crear", command=self.create).grid(column=0, row=0)
        Button(frame, text="Modificar", command=self.edit).grid(column=1, row=0)
        Button(frame, text="Eliminar", command=self.delete).grid(column=2, row=0)

        self.treeview = treeview

    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, "values")
            confirmar = askokcancel(
                title="Eliminar Cliente",
                message=f"¿Eliminar el cliente: {campos[1]} {campos[2]}?",
                icon=WARNING)
            if confirmar:
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0])

    def create(self):
        CreateClientWindow(self)

    def edit(self):
        if self.treeview.focus():
           EditClientWindow(self)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
