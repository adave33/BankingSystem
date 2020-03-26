from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account_management.forms import BankAccountForm
from django.core.exceptions import PermissionDenied
from account_management.models import AccountRequests, Account
from user_management.models import User
from account_management.utility.manage_accounts import create_account_for_current_request
# Create your views here.


@login_required
def open_account(request):
    context = {}
    if request.POST:
        form = BankAccountForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user_id = request.user
            instance.save()
            context['request_received'] = True
    else:
        pending_requests = AccountRequests.objects.filter(
            user_id=request.user,
            status='NEW'
        ).count()
        if pending_requests > 0:
            context['pending_request'] = True
        form = BankAccountForm()
        context['bank_form'] = form
    return render(request, 'account_management/open_account.html', context)


@login_required
def view_accounts(request):
    if request.POST:
        User.objects.filter(user_id=request.user.user_id).update(
            primary_account=request.POST['account_num'])
    context = {}
    context['account_details'] = {
        'headers': ['Account number', 'Account type', 'Account balance', 'Action'],
        'accounts': []
    }
    user_accounts = Account.objects.filter(user_id=request.user)
    primary_account = User.objects.get(
        user_id=request.user.user_id).primary_account
    primary_account_id = primary_account.account_id if primary_account else None
    for acc in user_accounts:
        if acc.account_type == "CREDIT":
            primary_account_flag = -1
        elif acc.account_id == primary_account_id:
            primary_account_flag = 1
        else:
            primary_account_flag = 0
        context['account_details']['accounts'].append([
            acc.account_id,
            acc.account_type,
            acc.account_balance,
            primary_account_flag
        ])
    return render(request, 'account_management/view_accounts.html', context)


@login_required
def view_requests(request):
    if request.user.user_type != 'T2':
        raise PermissionDenied()
    context = {}
    if request.POST:
        if request.POST['status'] == 'APPROVE':
            user = User.objects.get(email=request.POST['email'])
            account = create_account_for_current_request(
                user, request.POST['account_type'])
            AccountRequests.objects.filter(user_id=user).update(
                status='APPROVED'
            )
            if user.primary_account is None and account.account_type != "CREDIT":
                User.objects.filter(email=request.POST['email']).update(
                    primary_account=account
                )
    context['account_requests'] = {
        'headers': ['First name', 'Last name', 'Email', 'Account type'],
        'body': []
    }
    pending_requests = AccountRequests.objects.filter(status='NEW')
    for pr in pending_requests:
        context['account_requests']['body'].append([
            pr.user_id.first_name,
            pr.user_id.last_name,
            pr.user_id.email,
            pr.account_type
        ])
    return render(request, 'account_management/view_requests.html', context)


@login_required
def deposit(request):
    context = {}
    if request.POST:
        pass
    else:
        context['user_accounts'] = {
            'headers': ['Account number', 'Account type', 'Account balance'],
            'data': []
        }
        context['select_account'] = True
        user_accounts = Account.objects.filter(
            user_id=request.user,
            account_type__in=["SAVINGS", "CHECKING"])
        for account in user_accounts:
            context['user_accounts']['data'].append([
                account.account_id,
                account.account_type,
                account.account_balance
            ])
    return render(request, 'account_management/deposit.html', context)


@login_required
def withdraw(request):
    context = {}
    return render(request, 'account_management/withdraw.html', context)
