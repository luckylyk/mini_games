
class MineSweeperController():

    def __init__(self, model, view, size, number_of_bombs):
        self.model = model
        self.model.set_size(size)
        self.model.set_bomb_number(number_of_bombs)
        self.model.initialize()
        self.model.start()

        self.view = view
        self.view.set_model(self.model)
        self.view.openIndexRequested.connect(self.model.open_index)
        self.view.setNextMarkRequested.connect(self.model.set_next_mark)

    def show(self):
        self.view.show()
