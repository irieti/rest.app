from django import forms


class PaymentForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2)
    currency = forms.ChoiceField(
        choices=[("EUR", "EUR")], initial="EUR", widget=forms.HiddenInput()
    )


class ClientForm(forms.Form):
    CHOICES = [
        ("no", "No / Não"),
        ("mail", "Yes, by e-mail / Sim, por e-mail"),
        ("print", "Yes, printed / Sim, impresso"),
    ]

    name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(attrs={"class": "form-input"}),
        label="Name / Nome (required)",
    )
    surname = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={"class": "form-input"}),
        label="Surname / Sobrenome (required)",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-input"}),
        label="Email (required)",
    )
    invoice = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "radio-input"}),
        label="Please tick if you would like to receive your invoice by email / Carregue no botão para receber a fatura por e-mail",
        required=False,
    )
