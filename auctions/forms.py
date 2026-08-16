"auctions/forms.py"

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import Bid


# =========================================================
# BID FORM
# =========================================================

class BidForm(forms.ModelForm):

    class Meta:
        model = Bid

        fields = [
            'amount',
        ]

        widgets = {
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your bid amount',
                    'min': '0',
                    'step': '0.01',
                }
            ),
        }

        labels = {
            'amount': 'Your Bid Amount (TZS)',
        }


# =========================================================
# REGISTER FORM
# =========================================================

class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Create your password',
                'autocomplete': 'new-password',
            }
        )
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password',
                'autocomplete': 'new-password',
            }
        )
    )

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'email',
        ]

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
        }

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your first name',
                    'autocomplete': 'given-name',
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your last name',
                    'autocomplete': 'family-name',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter your email address',
                    'autocomplete': 'email',
                }
            ),
        }

    # =====================================================
    # EMAIL VALIDATION
    # =====================================================

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if not email:
            raise forms.ValidationError(
                'Tafadhali weka email yako.'
            )

        # Remove spaces and make email lowercase
        email = email.strip().lower()

        # Check whether this exact email already exists
        existing_user = User.objects.filter(
            email__iexact=email
        ).first()

        if existing_user:

            raise forms.ValidationError(
                'Email hii tayari imesajiliwa. '
                'Tafadhali tumia email nyingine.'
            )

        return email

    # =====================================================
    # PASSWORD CONFIRMATION
    # =====================================================

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:

            if password1 != password2:

                raise forms.ValidationError(
                    'Passwords hazifanani.'
                )

        return password2

    # =====================================================
    # SAVE USER
    # =====================================================

    def save(self, commit=True):

        user = super().save(commit=False)

        email = self.cleaned_data['email']

        # =================================================
        # AUTOMATIC USERNAME
        # =================================================

        base_username = email.split('@')[0]

        username = base_username

        counter = 1

        while User.objects.filter(
            username=username
        ).exists():

            username = f'{base_username}{counter}'

            counter += 1

        user.username = username

        # =================================================
        # PASSWORD
        # =================================================

        user.set_password(
            self.cleaned_data['password1']
        )

        # =================================================
        # SAVE USER
        # =================================================

        if commit:
            user.save()

        return user


# =========================================================
# LOGIN USING EMAIL
# =========================================================

class EmailLoginForm(forms.Form):

    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email address',
                'autocomplete': 'email',
            }
        )
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password',
                'autocomplete': 'current-password',
            }
        )
    )

    def __init__(self, request=None, *args, **kwargs):

        self.request = request
        self.user_cache = None

        super().__init__(*args, **kwargs)

    # =====================================================
    # LOGIN VALIDATION
    # =====================================================

    def clean(self):

        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not email or not password:
            return cleaned_data

        email = email.strip().lower()

        try:

            user = User.objects.get(
                email__iexact=email
            )

        except User.DoesNotExist:

            raise forms.ValidationError(
                'Email au password si sahihi.'
            )

        if not user.check_password(password):

            raise forms.ValidationError(
                'Email au password si sahihi.'
            )

        if not user.is_active:

            raise forms.ValidationError(
                'Akaunti hii haijawezeshwa.'
            )

        self.user_cache = user

        return cleaned_data

    # =====================================================
    # GET USER
    # =====================================================

    def get_user(self):

        return self.user_cache