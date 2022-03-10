from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.db.models import Q
from .models import Post, Booking
from .forms import AvailabilityForm
from properties.booking_functions.availability import check_availability
from django.urls import reverse, reverse_lazy


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'properties/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'properties/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class BookingListView(ListView):
    model = Booking
    ordering = ['-date_booked']
    paginate_by = 5

    # implement logic that only show bookings for the author of the booking
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            bookings = Booking.objects.all().order_by('-date_booked')
            return bookings
        else:
            bookings = Booking.objects.filter(author=self.request.user).order_by('-date_booked')
            return bookings


class BookingDetailView(DetailView):
    model = Booking


# displays all posts from a user
class UserPostListView(ListView):
    model = Post
    template_name = 'properties/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    # template_name = 'properties/post_detail.html'

    # display detail page
    def get(self, request, *args, **kwargs):
        # category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        # accommodation_list = Post.objects.filter(category=category)
        post = self.kwargs['pk']
        accommodation_list = Post.objects.filter(id=post)

        if len(accommodation_list) > 0:
            accommodation = accommodation_list[0]
            accommodation_category = dict(accommodation.ACCOMMODATION_CATEGORIES).get(accommodation.category, None)
            accommodation_id = accommodation.id
            accommodation_author = accommodation.author
            accommodation_title = accommodation.title
            accommodation_content = accommodation.content
            accommodation_capacity = accommodation.capacity
            accommodation_date_posted = accommodation.date_posted
            context = {
                'accommodation_id': accommodation_id,
                'accommodation_author': accommodation_author,
                'accommodation_date_posted': accommodation_date_posted,
                'accommodation_title': accommodation_title,
                'accommodation_content': accommodation_content,
                'accommodation_capacity': accommodation_capacity,
                'accommodation_category': accommodation_category,
                'form': form,
            }
            return render(request, 'properties/post_detail.html', context)
        else:
            return HttpResponse('Accommodation does not exist')

    # make booking
    def post(self, request, *args, **kwargs):
        # category = self.kwargs.get('category', None)
        # accommodation_list = Post.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        post = self.kwargs['pk']
        accommodation_list = Post.objects.filter(id=post)

        data = None

        if form.is_valid():
            data = form.cleaned_data

        available_accommodation = []
        for accommodation in accommodation_list:
            if check_availability(accommodation, data['move_in'], data['move_out']):
                available_accommodation.append(accommodation)

        if len(available_accommodation) > 0:
            accommodation = available_accommodation[0]
            booking = Booking.objects.create(
                author=self.request.user,
                accommodation=accommodation,
                move_in=data['move_in'],
                move_out=data['move_out']
            )
            booking.save()
            messages.success(request, f'Booking Successful')
            return redirect('booking')
        else:
            messages.error(request, f'Please correct the error below')
            return HttpResponse(f'This accommodation is booked!'
                                'Please try booking an alternate date or alternate accommodation')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'capacity']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'category', 'capacity']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # only authors of the post can update it
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# Booking
class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Booking
    fields = ['accommodation', 'move_in', 'move_out']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # only authors of the post can update it
    def test_func(self):
        booking = self.get_object()
        if self.request.user == booking.author:
            return True
        return False


class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    # redirect to home page once a post has been deleted
    success_url = reverse_lazy('booking')

    # only authors of the post can delete it
    def test_func(self):
        booking = self.get_object()
        if self.request.user == booking.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # redirect to home page once a post has been deleted
    success_url = '/'

    # only authors of the post can delete it
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# displays all search results
class SearchResultListView(ListView):
    model = Post
    template_name = 'properties/search_results.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

    # searching for all fields in the Post model
    # Used a get request since it doesnt affect the state of the app
    # nothing in the database is changing
    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q')
        if not query:
            query = ''
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(date_posted__icontains=query) |
            Q(author__username__icontains=query)
        )
        return results


def about(request):
    return render(request, 'properties/about.html', {'title': 'About'})
