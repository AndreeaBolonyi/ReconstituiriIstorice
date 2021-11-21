from domain.validators.InputValidator import InputValidator
from domain.validators.ValidatorException import ValidatorException


class FemurValidator(InputValidator):
    def __init__(self, *args):
        super().__init__()

    def validate(self,*args):
        try:
            fml = float(args[0])
            feb = float(args[1])
            fhd = float(args[2])
            fmld = float(args[3])
        except ValueError:
            raise ValidatorException("Parametrii contin unul sau mai multe valori care nu sunt de tip rational")
        values = [fml, feb, fhd, fmld]
        if any(values) < 0:
            raise ValidatorException("Parametrii contin un numar negativ")
        self.validate_fml(fml, feb, fhd, fmld)
        self.validate_feb(fml, feb, fhd, fmld)
        self.validate_fhd(fml, feb, fhd, fmld)
        self.validate_fmld(fml, feb, fhd, fmld)

    @staticmethod
    def validate_fml(fml, feb, fhd, fmld):
        lower_values = [feb,fhd,fmld]
        if fml < any(lower_values):
            raise ValidatorException("Lungimea maxima a femurului nu poate fi mai mica decat oricare dintre ceilalti "
                                     "parametrii")

    @staticmethod
    def validate_feb(fml, feb, fhd, fmld):
        lower_values = [fhd,fmld]
        greater_values = [fml]

        if feb < any(lower_values):
            raise ValidatorException("Latimea medio-laterala epicondilara a femurului nu poate fi mai mica decat FHD "
                                     "sau FMLD")

        if feb > any(greater_values):
            raise ValidatorException("Latimea medio-laterala epicondilara a femurului nu poate fi mai mare decat FML")

    @staticmethod
    def validate_fhd(fml, feb, fhd, fmld):
        greater_values = [feb,fml]
        lower_values = [fmld]
        if fhd > any(greater_values):
            raise ValidatorException("Diametrul capului femurului nu poate fi mai mare decat FEB sau FML")
        if fhd < any(lower_values):
            raise ValidatorException("Diametrul capului femurului trebuie sa fie mai mare decat FMLD")

    @staticmethod
    def validate_fmld(fml, feb, fhd, fmld):
        greater_values = [fml,fhd,feb]

        if fmld > any(greater_values):
            raise ValidatorException("Diametrul medio-lateral diafizar al femurului nu poate fi mai mare decat "
                                     "oricare dintre valorile parametriilor")