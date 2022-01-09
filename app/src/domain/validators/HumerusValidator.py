from app.src.domain.validators.InputValidator import InputValidator
from app.src.domain.validators.ValidatorException import ValidatorException


class HumerusValidator(InputValidator):
    def __init__(self):
        super().__init__()

    def validate(self, *args):
        try:
            hml = float(args[0])
            heb = float(args[1])
            hhd = float(args[2])
            hmld = float(args[3])
        except ValueError:
            raise ValidatorException("Parametrii contin unul sau mai multe valori care nu sunt de tip rational!")
        values = [hml, heb, hhd, hmld]
        if any(values) < 0:
            raise ValidatorException("Parametrii contin un numar negativ!")
        self.validate_hml(hml, heb, hhd, hmld)
        self.validate_heb(hml, heb, hhd, hmld)
        self.validate_hhd(hml, heb, hhd, hmld)
        self.validate_hmld(hml, heb, hhd, hmld)

    @staticmethod
    def validate_hml(hml, heb, hhd, hmld):
        lower_values = [hhd, hmld, heb]
        if hml < max(lower_values):
            raise ValidatorException("Lungimea maxima a humerusului (HML) trebuie sa fie mai mare decat oricare dintre "
                                     "ceilalti parametrii!")

    @staticmethod
    def validate_heb(hml, heb, hhd, hmld):
        lower_values = [hmld, hhd]
        if heb < max(lower_values):
            raise ValidatorException("Latimea epicondilara a humerusului (HEB) nu poate fi mai mica decat diametrul capului "
                                     "(HHD) sau diametrul medio-lateral diafizar al humerusului (HMLD)!")
        greater_values = [hml]
        if heb > min(greater_values):
            raise ValidatorException("Latimea epicondilara a humerusului (HEB) nu poate fi mai mare ca lungimea maxima a humerusului"
                                     "(HML)!")

    @staticmethod
    def validate_hhd(hml, heb, hhd, hmld):
        greater_values = [hml, heb]
        if hhd > min(greater_values):
            raise ValidatorException("Diametrul capului humerusului (HHD) nu poate fi mai mare decat latimea epicondilara "
                                     "(HEB) sau lungimea maxima a humerusului (HML)!")
        lower_values = [hmld]
        if hhd < max(lower_values):
            raise ValidatorException("Diametrul capului humerusului (HHD) nu poate fi mai mic decat diametrul medio-lateral"
                                     " diafizar al humerusului (HMLD)!")

    @staticmethod
    def validate_hmld(hml, heb, hhd, hmld):
        greater_values = [hml,heb,hhd]
        if hmld > min(greater_values):
            raise ValidatorException("Diametrul medio-lateral diafizar al humerusului (HMLD) nu poate fi mai mare decat "
                                     "oricare dintre parametrii!")
