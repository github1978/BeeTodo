import utils
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor


class StyleSheets(object):

    @staticmethod
    def getCSS(cssfilename):
        return utils.FileUtil().readFile(utils.getExePath() + "/css/" + cssfilename + ".css")

    @staticmethod
    def getShadowEffect():
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setOffset(-2, 3)
        shadow_effect.setColor(QColor(43, 43, 43))
        shadow_effect.setBlurRadius(6)
        return shadow_effect
