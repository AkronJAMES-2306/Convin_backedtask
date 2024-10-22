from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User, Expense
from .serializers import UserSerializer, ExpenseSerializer
import csv
from django.http import HttpResponse, JsonResponse
from .forms import UserForm, ExpenseForm
from django.core.exceptions import ValidationError

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

class ExpenseCreateView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

class ExpenseListView(generics.ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

def download_balance_sheet(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balancesheet.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Description', 'Amount', 'Split Method', 'Created By', 'Participants'])
    
    expenses = Expense.objects.all()
    for expense in expenses:
        writer.writerow([
            expense.description,
            expense.amount,
            expense.split_method,
            expense.created_by.username,  # Assuming you want the username
            ', '.join([p.username for p in expense.participants.all()])
        ])
    
    return response

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "User created successfully."}, status=201)
        return JsonResponse({"errors": form.errors}, status=400)
    return JsonResponse({"error": "Method not allowed."}, status=405)

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        try:
            form.full_clean()  
            form.save()  
            return JsonResponse({"message": "Expense added successfully."}, status=201)
        except ValidationError as e:
            return JsonResponse({"errors": e.messages}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Method not allowed."}, status=405)

#@login_required
def individual_expenses(request):
    user_expenses = Expense.objects.filter(created_by=request.user).values(
        'description', 'amount', 'split_method', 'created_at'
    )
    return JsonResponse(list(user_expenses), safe=False)

#@login_required
def overall_expenses(request):
    overall_expenses = Expense.objects.all().values(
        'description', 'amount', 'split_method', 'created_by', 'created_at'
    )
    return JsonResponse(list(overall_expenses), safe=False)
