from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,DetailView,FormView,TemplateView
from django.contrib.auth import authenticate,login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .models import *
from .forms import *

class HomeView(TemplateView):
    template_name = 'home.html'

class RegisterView(CreateView):
    form_class =RegistrationForm
    template_name = 'register.html'
    def form_valid(self,form):
        user = form.save()
        login(self.request, user)
        return redirect('account')

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('account_detail')
    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        password = form.cleaned_data['password']
        user = authenticate(self.request,username=phone_number,password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return redirect('login')

class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'account.html'
    success_url = reverse_lazy('account_detail')
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AccountDetailView(DetailView):
    model = Account
    template_name = 'account_detail.html'
    context_object_name = 'account'
    def get_object(self):
        return get_object_or_404(Account,user=self.request.user)

class CardListView(ListView):
    model = Card
    template_name = 'cards.html'
    context_object_name = 'cards'
    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

class CardDetailView(DetailView):
    model = Card
    template_name = 'card_detail.html'
    context_object_name = 'card'
    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

class CardCreateView(CreateView):
    model = Card
    form_class = CardForm
    template_name = 'card_create.html'
    success_url = reverse_lazy('cards')
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransferView(FormView):
    form_class = TransferForm
    template_name = 'transfer.html'
    success_url = reverse_lazy('history')
    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        card_number = form.cleaned_data['card_number']
        source_card_number = form.cleaned_data['source_card_number']
        source = form.cleaned_data['source']
        destination = form.cleaned_data['destination']
        amount = form.cleaned_data['amount']
        if amount <= 0:
            return redirect('transfer')
        source_card = None
        destination_card = None
        if source == 'account':
            source_balance = get_object_or_404(Account,user=self.request.user)
        else:
            source_card = get_object_or_404(Card,user=self.request.user,card_number=source_card_number)
            source_balance = source_card
        if source_balance.balance < amount:
            return redirect('transfer')
        if destination == 'account':
            receiver = get_object_or_404(User,phone_number=phone_number)
            destination_balance = get_object_or_404(Account,user=receiver)
        else:
            destination_card = get_object_or_404(Card,card_number=card_number)
            receiver = destination_card.user
            destination_balance = destination_card
        source_balance.balance -= amount
        destination_balance.balance += amount
        source_balance.save()
        destination_balance.save()
        Transaction.objects.create(sender=self.request.user,receiver=receiver,source=source,source_card=source_card,destination=destination,destination_card=destination_card,amount=amount)
        return super().form_valid(form)

class HistoryView(ListView):
    model = Transaction
    template_name = 'history.html'
    context_object_name = 'transactions'
    def get_queryset(self):
        filter = self.request.GET.get('filter')
        if filter == 'sent':
            transactions = Transaction.objects.filter(sender=self.request.user)
        elif filter == 'received':
            transactions = Transaction.objects.filter(receiver=self.request.user)
        else:
            transactions = Transaction.objects.filter(sender = self.request.user) | Transaction.objects.filter(receiver = self.request.user)
        return transactions

class CardHistoryView(ListView):
    model = Transaction
    template_name = 'card_history.html'
    context_object_name = 'transactions'
    def get_queryset(self):
        card_id = self.request.GET.get('id')
        card = get_object_or_404(Card,user=self.request.user,id=card_id)
        filter = self.request.GET.get('filter')
        if filter == 'sent':
            transactions = Transaction.objects.filter(source_card=card)
        elif filter == 'received':
            transactions = Transaction.objects.filter(destination_card=card)
        else:
            transactions = Transaction.objects.filter(source_card=card) | Transaction.objects.filter(destination_card=card)
        return transactions

class CheckPhoneView(FormView):
    form_class = CheckPhoneForm
    template_name = 'check_phone.html'
    def form_valid(self,form):
        phone = form.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone).first()
        if user:
            account = Account.objects.filter(user=user).first()
            return render(self.request,'check_phone_result.html',{'account':account})
        return render(self.request,'check_phone_result.html',{'error':'User not found'})

class CheckCardView(FormView):
    form_class = CheckCardForm
    template_name = 'check_card.html'
    def form_valid(self,form):
        card_number = form.cleaned_data['card_number']
        card = Card.objects.filter(card_number=card_number).first()
        if card:
            account = Account.objects.filter(user=card.user).first()
            return render(self.request,'check_card_result.html',{'account':account})
        return render(self.request,'check_card_result.html',{'error':'Card not found'})