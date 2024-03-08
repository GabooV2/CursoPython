# Este va a ser el script principal que va a ser el ejecutable del proyecto
import sys
import ui
import menu

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        menu.iniciar()
    else:
        app = ui.MainWindow()
        app.mainloop()