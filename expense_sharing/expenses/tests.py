from django.test import TestCase
from .models import User, Expense
from .forms import UserForm, ExpenseForm

class UserModelTest(TestCase):

    def setUp(self):
        self.valid_user_data = {
            'email': 'arvindtest1@gmail.com',
            'name': 'ut1',
            'mobile_number': '1234567890'
        }
        
        self.invalid_user_data = {
            'email': 'arvindtest2@gmail.com',
            'name': 'ut2invalid',
            'mobile_number': 'invalidnumber'  
        }

    def test_create_user_with_valid_data(self):
        form = UserForm(data=self.valid_user_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, self.valid_user_data['email'])

    def test_create_user_with_duplicate_email(self):
        User.objects.create(**self.valid_user_data)
        form = UserForm(data=self.valid_user_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Email already exists', form.errors['email'])

    def test_create_user_with_invalid_mobile_number(self):
        form = UserForm(data=self.invalid_user_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Mobile number must be a 10-digit number.', form.errors['mobile_number'])

class ExpenseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@example.com', name='User', mobile_number='1234567890')
        self.valid_expense_data = {
            'amount': 5000,
            'participants': [self.user.id],  
        }
        self.invalid_expense_data = {
            'amount': -1000,  
            'participants': [],
        }
    def test_add_expense_with_valid_data(self):
        form = ExpenseForm(data=self.valid_expense_data)
        self.assertTrue(form.is_valid())
        expense = form.save(commit=False)
        expense.user = self.user  
        expense.save()
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(expense.amount, self.valid_expense_data['amount'])
    
    def test_add_expense_with_invalid_amount(self):
        form = ExpenseForm(data=self.invalid_expense_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Amount must be a positive number.', form.errors['amount'])

    def test_add_expense_with_no_participants(self):
        form = ExpenseForm(data=self.invalid_expense_data)
        self.assertFalse(form.is_valid())
        self.assertIn('At least one participant is required.', form.errors['participants'])

class PercentageSplitValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@example.com', name='User', mobile_number='1234567890')
        self.valid_expense_data = {
            'amount': 1000,
            'participants': [self.user.id],
            'percentages': [50]  
        }
        
        self.invalid_percentage_data = {
            'amount': 1000,
            'participants': [self.user.id],
            'percentages': [50, 60]  
        }

    def test_valid_percentage_split(self):
        form = ExpenseForm(data=self.valid_expense_data)
        self.assertTrue(form.is_valid())

    def test_invalid_percentage_split(self):
        form = ExpenseForm(data=self.invalid_percentage_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Percentages must add up to 100%.", form.errors)
