
class Controller():
    def __init__(self, view, model):
        self.view = view
        self.model = model

        #self.view.set_controller(self)
    
    def update_list(self):
        Films = self.model.load(r"Python_Projekt\Ohne_Firebase\Films.txt")
        self.view.List_Produkts(Films)

    def start(self):
        self.view.mainloop()