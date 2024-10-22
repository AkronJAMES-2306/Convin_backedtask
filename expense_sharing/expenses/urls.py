from django.urls import path
from .views import UserCreateView, UserDetailView, ExpenseCreateView, ExpenseListView, download_balance_sheet, add_expense, individual_expenses, overall_expenses
urlpatterns = [
    path('user/', UserCreateView.as_view(), name='create-user'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('expense/', ExpenseCreateView.as_view(), name='create-expense'),
    path('expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('balance-sheet/', download_balance_sheet, name='download-balance-sheet'),
    path('add_expense/', add_expense, name='add_expense'),
    path('individual_expenses/', individual_expenses, name='individual_expenses'), 
    path('overall_expenses/', overall_expenses, name='overall_expenses'),
]


