from domain.validators.InputValidator import InputValidator
from domain.validators.ValidatorException import ValidatorException


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
            raise ValidatorException("Parametrii contin unul sau mai multe valori care nu sunt de tip rational")
        values = [hml, heb, hhd, hmld]
        if any(values) < 0:
            raise ValidatorException("Parametrii contin un numar negativ")
        self.validate_hml(hml, heb, hhd, hmld)
        self.validate_heb(hml, heb, hhd, hmld)
        self.validate_hhd(hml, heb, hhd, hmld)
        self.validate_hmld(hml, heb, hhd, hmld)

    @staticmethod
    def validate_hml(hml, heb, hhd, hmld):
        lower_values = [hhd, hmld, heb]
        if hml < any(lower_values):
            raise ValidatorException("Lungimea maxima a humerusului trebuie sa fie mai mare decat oricare dintre "
                                     "ceilalti parametrii")

    @staticmethod
    def validate_heb(hml, heb, hhd, hmld):
        if heb < hhd:
            raise ValidatorException("Latimea epicondilara a humerusului nu poate fi mai mica decat diametrul capului "
                                     "humerusului")
        greater_values = [hml, hmld]
        if heb > any(greater_values):
            raise ValidatorException("Latimea epicondilara a humerusului nu poate fi mai mare ca HML sau HMLD")

    @staticmethod
    def validate_hhd(hml, heb, hhd, hmld):
        greater_values = [hml, heb, hmld]
        if hhd > any(greater_values):
            raise ValidatorException("Diametrul capului humerusului nu poate fi mai mare decat oricare dintre "
                                     "ceilalti parametrii")

    @staticmethod
    def validate_hmld(hml, heb, hhd, hmld):
        pass
