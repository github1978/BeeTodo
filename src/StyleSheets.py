import utils
from PyQt5.Qt import *


class StyleSheets(object):

    @staticmethod
    def getCSS(cssfilename):
        return utils.FileUtil().readFile(utils.getExePath()+"/css/" + cssfilename + ".css")

    @staticmethod
    def getShadowEffect():
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setOffset(-5, 5)
        shadow_effect.setColor(Qt.red)
        shadow_effect.setBlurRadius(8)
