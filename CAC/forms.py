from .models import DiabetesPrediction
from django import forms

input_style = "width:60%; margin:auto; padding: auto;  font-size: 20px;"

class DiabetesPredictionForm(forms.ModelForm):
    class Meta():
        model = DiabetesPrediction
        error_css_class = 'error'
        exclude = ('result','user')
        widgets = {
            'Pregnancies': forms.TextInput(attrs={'class': 'form-control','style':input_style, 'placeholder':'between 0-63 ...' }),
            'Glucose': forms.TextInput(attrs={'class':'form-control','style':input_style,'placeholder':'between 0-511...'}),
            'BloodPressure': forms.TextInput(attrs={'class': 'form-control','style':input_style,'placeholder':'between 0-255 ...'}),
            'SkinThickness': forms.TextInput(attrs={'class': 'form-control','style':input_style,'placeholder':'between 0-255...'}),
            'Insulin': forms.TextInput(attrs={'class': 'form-control','style':input_style,'placeholder':'between 0-1023 ...'}),
            'BMI': forms.TextInput(attrs={'class': 'form-control','style':input_style,'placeholder':'between 0-99.9 ...'}),
            'DiabetesPedigreeFunction': forms.TextInput(attrs={'class': 'form-control','style':input_style ,'placeholder':'between 0 - 2.047 ...'}),
            'Age': forms.TextInput(attrs={'class': 'form-control','style':input_style,'placeholder':'Age in years'}),
            'name': forms.TextInput(attrs={'class': 'form-control','style':input_style,'placeholder':'prediction name'}),

        }
    def clean_Pregnancies(self):
            Pregnancies = self.cleaned_data.get("Pregnancies")
            if Pregnancies > 63 or Pregnancies <0:
                raise forms.ValidationError("out of bounds")
            else:
                return Pregnancies
    def clean_Glucose(self):
            Pregnancies = self.cleaned_data.get("Glucose")
            if Pregnancies > 511 or Pregnancies <0:
                raise forms.ValidationError("Glucose out of bounds")
            else:
                return Pregnancies
    def clean_BloodPressure(self):
            Pregnancies = self.cleaned_data.get("BloodPressure")
            if Pregnancies > 255 or Pregnancies <0:
                raise forms.ValidationError("BloodPressure out of bounds")
            else:
                return Pregnancies
    def clean_SkinThickness(self):
            Pregnancies = self.cleaned_data.get("SkinThickness")
            if Pregnancies > 255 or Pregnancies <0:
                raise forms.ValidationError("SkinThickness out of bounds")
            else:
                return Pregnancies

    def clean_Insulin(self):
            Pregnancies = self.cleaned_data.get("Insulin")
            if Pregnancies > 1023 or Pregnancies <0:
                raise forms.ValidationError("Insulin out of bounds")
            else:
                return Pregnancies

    def clean_BMI(self):
            Pregnancies = self.cleaned_data.get("BMI")
            if Pregnancies > 99.9 or Pregnancies <0:
                raise forms.ValidationError("BMI out of bounds")
            else:
                return Pregnancies

    def clean_DiabetesPedigreeFunction(self):
            Pregnancies = self.cleaned_data.get("DiabetesPedigreeFunction")
            if Pregnancies > 2.047 or Pregnancies <0:
                raise forms.ValidationError("DiabetesPedigreeFunction out of bounds")
            else:
                return Pregnancies
    def clean_Age(self):
            Pregnancies = self.cleaned_data.get("Age")
            if Pregnancies > 120 or Pregnancies <0:
                raise forms.ValidationError("Age out of bounds")
            else:
                return Pregnancies

        
