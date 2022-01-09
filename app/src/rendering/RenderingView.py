from direct.showbase.ShowBase import ShowBase


class RenderingView(ShowBase):
    def __init__(self,modelName):
        ShowBase.__init__(self)
        self.scene = self.loader.loadModel("app/assets/models/"+modelName+".obj")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.1, 0.1, 0.1)
        self.scene.setPos(-8, 100, 0)