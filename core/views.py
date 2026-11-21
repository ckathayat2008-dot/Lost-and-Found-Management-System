
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date

from .models import Item


# HOME PAGE
def home(request):
    return render(request, 'home.html')


# USER REGISTRATION
def register(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not email or not password:
            messages.error(request, "Please fill in all fields.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful!")
        return redirect('login')

    return render(request, 'register.html')


# USER LOGIN
def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, "Invalid username or password!")

    return render(request, 'login.html')


# USER LOGOUT
@login_required(login_url='login')
def user_logout(request):

    if request.method == 'POST':
        logout(request)

    return redirect('home')


# COMMON ITEM REPORT FUNCTION
@login_required(login_url='login')
def report_item(request, item_type):

    if item_type not in ['Lost', 'Found']:
        return redirect('home')

    if request.method == 'POST':

        item_name = request.POST.get('item_name', '').strip()
        category = request.POST.get('category')
        description = request.POST.get('description', '').strip()
        location = request.POST.get('location', '').strip()
        incident_date = request.POST.get('date_lost_found')
        contact_number = request.POST.get('contact_number', '').strip()

        try:
            parsed_date = date.fromisoformat(incident_date)
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid date.")
            return redirect(request.path)

        valid_categories = [
            choice[0] for choice in Item.CATEGORY_CHOICES
        ]

        if not all([
            item_name,
            category,
            description,
            location,
            contact_number
        ]):
            messages.error(request, "Please fill in all fields.")
            return redirect(request.path)

        if category not in valid_categories:
            messages.error(request, "Please select a valid category.")
            return redirect(request.path)

        Item.objects.create(
            item_type=item_type,
            item_name=item_name,
            category=category,
            description=description,
            location=location,
            date_lost_found=parsed_date,
            contact_number=contact_number,
            reported_by=request.user
        )

        messages.success(
            request,
            f"{item_type} item reported successfully!"
        )

        return redirect('item_list')

    context = {
        'item_type': item_type,
        'categories': Item.CATEGORY_CHOICES,
    }

    return render(request, 'report_item.html', context)


def report_lost(request):
    return report_item(request, 'Lost')


def report_found(request):
    return report_item(request, 'Found')


# DISPLAY ALL ITEMS WITH SEARCH AND FILTERS
def item_list(request):

    items = Item.objects.filter(status='Active').order_by('-created_at')

    search_query = request.GET.get('q', '').strip()
    selected_type = request.GET.get('type', '').strip()
    selected_category = request.GET.get('category', '').strip()

    if search_query:
        items = items.filter(
            Q(item_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    if selected_type in ['Lost', 'Found']:
        items = items.filter(item_type=selected_type)

    valid_categories = [
        choice[0] for choice in Item.CATEGORY_CHOICES
    ]

    if selected_category in valid_categories:
        items = items.filter(category=selected_category)

    return render(request, 'item_list.html', {
        'items': items,
        'search_query': search_query,
        'selected_type': selected_type,
        'selected_category': selected_category,
        'categories': Item.CATEGORY_CHOICES,
    })


# ITEM DETAILS
def item_detail(request, pk):

    item = get_object_or_404(Item, pk=pk)

    return render(request, 'item_detail.html', {
        'item': item
    })


# USER DASHBOARD
@login_required(login_url='login')
def dashboard(request):

    my_items = Item.objects.filter(
        reported_by=request.user
    ).order_by('-created_at')

    return render(request, 'dashboard.html', {
        'my_items': my_items,
        'total_items': my_items.count(),
        'lost_count': my_items.filter(item_type='Lost').count(),
        'found_count': my_items.filter(item_type='Found').count(),
    })


# EDIT ITEM
@login_required(login_url='login')
def edit_item(request, pk):

    item = get_object_or_404(
        Item,
        pk=pk,
        reported_by=request.user
    )

    if request.method == 'POST':

        item_name = request.POST.get('item_name', '').strip()
        category = request.POST.get('category')
        description = request.POST.get('description', '').strip()
        location = request.POST.get('location', '').strip()
        incident_date = request.POST.get('date_lost_found')
        contact_number = request.POST.get('contact_number', '').strip()

        valid_categories = [
            choice[0] for choice in Item.CATEGORY_CHOICES
        ]

        try:
            parsed_date = date.fromisoformat(incident_date)
        except (ValueError, TypeError):
            messages.error(request, "Enter a valid date.")
            return redirect('edit_item', pk=item.pk)

        if not all([
            item_name,
            category,
            description,
            location,
            contact_number
        ]):
            messages.error(request, "Please fill in all fields.")
            return redirect('edit_item', pk=item.pk)

        if category not in valid_categories:
            messages.error(request, "Invalid category selected.")
            return redirect('edit_item', pk=item.pk)

        item.item_name = item_name
        item.category = category
        item.description = description
        item.location = location
        item.date_lost_found = parsed_date
        item.contact_number = contact_number

        item.save()

        messages.success(request, "Item updated successfully!")

        return redirect('dashboard')

    return render(request, 'edit_item.html', {
        'item': item,
        'categories': Item.CATEGORY_CHOICES,
    })


# DELETE ITEM
@login_required(login_url='login')
def delete_item(request, pk):

    item = get_object_or_404(
        Item,
        pk=pk,
        reported_by=request.user
    )

    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item deleted successfully!")
        return redirect('dashboard')

    return render(request, 'confirm_delete.html', {
        'item': item
    })
