from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import (
    Bid,
    Item,
    Category,
    SubCategory,
)


# =========================================================
# REGISTER FORM
# =========================================================

class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password',
                'autocomplete': 'new-password',
            }
        )
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password',
                'autocomplete': 'new-password',
            }
        )
    )

    class Meta:
        model = User

        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'First name',
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Last name',
                }
            ),

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Username',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email address',
                    'autocomplete': 'email',
                }
            ),
        }

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if not email:
            raise forms.ValidationError(
                'Email is required.'
            )

        email = email.strip().lower()

        if User.objects.filter(
            email__iexact=email
        ).exists():

            raise forms.ValidationError(
                'Email hii tayari imesajiliwa. '
                'Tumia email nyingine au ingia kwenye akaunti yako.'
            )

        return email

    def clean_username(self):

        username = self.cleaned_data.get('username')

        if not username:
            raise forms.ValidationError(
                'Username is required.'
            )

        username = username.strip()

        if User.objects.filter(
            username__iexact=username
        ).exists():

            raise forms.ValidationError(
                'Username hii tayari inatumika.'
            )

        return username

    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:

            if password1 != password2:

                raise forms.ValidationError(
                    'Passwords hazifanani.'
                )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data[
            'email'
        ].strip().lower()

        user.set_password(
            self.cleaned_data['password1']
        )

        if commit:
            user.save()

        return user


# =========================================================
# EMAIL LOGIN FORM
# =========================================================

class EmailLoginForm(AuthenticationForm):

    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'autocomplete': 'email',
            }
        )
    )

    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
                'autocomplete': 'current-password',
            }
        )
    )

    def clean(self):

        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:

            email = email.strip().lower()

            try:

                user_obj = User.objects.get(
                    email__iexact=email
                )

                username = user_obj.username

            except User.DoesNotExist:

                raise forms.ValidationError(
                    'Email au password si sahihi.'
                )

            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )

            if self.user_cache is None:

                raise forms.ValidationError(
                    'Email au password si sahihi.'
                )

            self.confirm_login_allowed(
                self.user_cache
            )

        return self.cleaned_data


# =========================================================
# BID FORM
# =========================================================

class BidForm(forms.ModelForm):

    class Meta:

        model = Bid

        fields = (
            'amount',
        )

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

    def clean_amount(self):

        amount = self.cleaned_data.get('amount')

        if amount is None:

            raise forms.ValidationError(
                'Please enter a bid amount.'
            )

        if amount <= 0:

            raise forms.ValidationError(
                'Bid amount must be greater than zero.'
            )

        return amount


# =========================================================
# ITEM FORM
# =========================================================

class ItemForm(forms.ModelForm):

    class Meta:

        model = Item

        fields = (
            'auction',
            'category',
            'subcategory',
            'name',
            'description',
            'starting_price',
            'image',
            'condition',
        )

        widgets = {

            'auction': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),

            'category': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'id_category',
                }
            ),

            'subcategory': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'id_subcategory',
                }
            ),

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Item name',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Item description',
                }
            ),

            'starting_price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'step': '0.01',
                    'placeholder': 'Starting price',
                }
            ),

            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*',
                }
            ),

            'condition': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: New, Used, Good',
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(
            *args,
            **kwargs
        )

        self.fields[
            'category'
        ].queryset = Category.objects.all().order_by(
            'name'
        )

        self.fields[
            'subcategory'
        ].queryset = SubCategory.objects.none()

        category_id = None

        if self.is_bound:

            category_id = self.data.get(
                'category'
            )

        elif self.instance.pk:

            category_id = self.instance.category_id

        if category_id:

            try:

                self.fields[
                    'subcategory'
                ].queryset = SubCategory.objects.filter(
                    category_id=category_id
                ).order_by(
                    'name'
                )

            except (
                ValueError,
                TypeError
            ):

                pass

    def clean_starting_price(self):

        price = self.cleaned_data.get(
            'starting_price'
        )

        if price is None:

            raise forms.ValidationError(
                'Starting price is required.'
            )

        if price <= 0:

            raise forms.ValidationError(
                'Starting price must be greater than zero.'
            )

        return price

    def clean(self):

        cleaned_data = super().clean()

        category = cleaned_data.get(
            'category'
        )

        subcategory = cleaned_data.get(
            'subcategory'
        )

        if subcategory and category:

            if subcategory.category_id != category.id:

                raise forms.ValidationError(
                    'SubCategory lazima itoke kwenye Category '
                    'uliyochagua.'
                )

        elif subcategory and not category:

            raise forms.ValidationError(
                'Chagua Category kwanza.'
            )

        return cleaned_data