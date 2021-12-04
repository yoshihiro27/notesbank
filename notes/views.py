from django.shortcuts import render,redirect,resolve_url
from django.http import HttpResponse
from django.urls import path
from django.contrib import admin
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post,Connection,Post1,Connection1
from django.urls import reverse_lazy
from django.views import View
from django.views import generic



# Create your views here.

class Home(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list.html'
    def get_queryset(self):
        return Post.objects.exclude(user=self.request.user).order_by('-created_at1'),
      
   
class MyPost(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super(MyPost, self).get_context_data(**kwargs)
        context.update({
            'object_list2': Post1.objects.filter(user=self.request.user).order_by('-created_at1'),
        })
        return context
    
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-created_at')







class DetailPost(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'detail.html'


class DetailPost1(LoginRequiredMixin, DetailView):
    model = Post1
    template_name = 'detail1.html'


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create.html'
    fields = ['title','content','grade','sub','file']
    success_url = reverse_lazy('notes:mypost')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class CreatePost1(LoginRequiredMixin, CreateView):
    model = Post1
    template_name = 'create1.html'
    fields = ['title1','content1','sub1','file']
    success_url = reverse_lazy('notes:mypost')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



def create_grade(request):
    return render(request,'create_grade.html')





    

class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'update.html'
    fields = ['title', 'content']

    def get_success_url(self,  **kwargs):
        pk = self.kwargs["pk"]
        return reverse_lazy('notes:detail', kwargs={"pk": pk})
   
    def test_func(self, **kwargs):
        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        return (post.user == self.request.user)


class UpdatePost1(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post1
    template_name = 'update1.html'
    fields = ['title1', 'content1']

    def get_success_url(self,  **kwargs):
        pk = self.kwargs["pk"]
        return reverse_lazy('notes:detail1', kwargs={"pk": pk})
   
    def test_func(self, **kwargs):
        pk = self.kwargs["pk"]
        post = Post1.objects.get(pk=pk)
        return (post.user == self.request.user)

        


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('notes:mypost')
    
    def test_func(self, **kwargs):
        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        return (post.user == self.request.user)


class DeletePost1(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post1
    template_name = 'delete1.html'
    success_url = reverse_lazy('notes:mypost')
    
    def test_func(self, **kwargs):
        pk = self.kwargs["pk"]
        post = Post1.objects.get(pk=pk)
        return (post.user == self.request.user)
        



class LikeBase(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        related_post = Post.objects.get(pk=pk)
       
        if self.request.user in related_post.like.all(): 
            obj = related_post.like.remove(self.request.user)
        else:                         
            obj = related_post.like.add(self.request.user)
        return obj


class LikeBase1(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        related_post1 = Post1.objects.get(pk=pk)
       
        if self.request.user in related_post1.like1.all(): 
            obj = related_post1.like1.remove(self.request.user)
        else:                         
            obj = related_post1.like1.add(self.request.user)
        return obj


class LikeHome(LikeBase):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return redirect('notes:mypost')

class LikeHome1(LikeBase1):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return redirect('notes:mypost')


class LikeDetail(LikeBase,View):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk'] 
        return redirect('notes:detail', pk)
        
class LikeDetail1(LikeBase,View):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk'] 
        return redirect('notes:detail1', pk) 


class FollowBase(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        target_user = Post.objects.get(pk=pk).user
       
        my_connection = Connection.objects.get_or_create(user=self.request.user)
       
        if target_user in my_connection[0].following.all():
            obj = my_connection[0].following.remove(target_user)
        else:
            obj = my_connection[0].following.add(target_user)
        return obj

class FollowBase1(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        target_user = Post1.objects.get(pk=pk).user
       
        my_connection = Connection1.objects.get_or_create(user=self.request.user)
       
        if target_user in my_connection[0].following.all():
            obj = my_connection[0].following.remove(target_user)
        else:
            obj = my_connection[0].following.add(target_user)
        return obj


class FollowHome(FollowBase):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return redirect('notes:home')

class FollowHome1(FollowBase1):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return redirect('notes:home')

class FollowDetail(FollowBase):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk'] 
        return redirect('notes:detail', pk)

class FollowDetail1(FollowBase1):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk'] 
        return redirect('notes:detail1', pk) 

class FollowList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'follow-list.html'

    def get_queryset(self):
        my_connection = Connection.objects.get_or_create(user=self.request.user)
        all_follow = my_connection[0].following.all()

        return Post.objects.filter(user__in=all_follow).order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context

    

class FollowList1(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'follow-list1.html'

    def get_queryset(self):
        my_connection = Connection1.objects.get_or_create(user=self.request.user)
        all_follow = my_connection[0].following.all()

        return Post1.objects.filter(user__in=all_follow).order_by('-created_at1')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['connection'] = Connection1.objects.get_or_create(user=self.request.user)
        return context



def FollowGrade(request):
    return render(request,'follow_grade.html')  


def note_like(request,pk):
    notes = Post.objects.get(pk=pk)
    notes.liked += 1 
    notes.save() 
    return redirect('notes:detail', pk)



class LiPost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(LiPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="1").order_by('-created_at1'),
        })
        return context


class OtherPost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(OtherPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="17").order_by('-created_at1'),
        })
        return context

class En1Post(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(En1Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="2").order_by('-created_at1'),
        })
        return context

class JaPost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(JaPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="3").order_by('-created_at1'),
        })
        return context

class TePost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(TePost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="4").order_by('-created_at1'),
        })
        return context

class WePost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(WePost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="5").order_by('-created_at1'),
        })
        return context

class MtPost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(MtPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="6").order_by('-created_at1'),
        })
        return context

class PhPost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(PhPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="7").order_by('-created_at1'),
        })
        return context

class EcPost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(EcPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="8").order_by('-created_at1'),
        })
        return context

class UnPost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(UnPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="9").order_by('-created_at1'),
        })
        return context

class RiPost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(RiPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="10").order_by('-created_at1'),
        })
        return context

class TcPost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(TcPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="11").order_by('-created_at1'),
        })
        return context

class MaPost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(MaPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="12").order_by('-created_at1'),
        })
        return context

class ArPost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(ArPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="13").order_by('-created_at1'),
        })
        return context

class ItPost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(ItPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub1="14").order_by('-created_at1'),
        })
        return context

class SePost(LoginRequiredMixin, ListView):
    model = Post1
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(SePost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post1.objects.filter(sub="15").order_by('-created_at1'),
        })
        return context





class Math2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Math2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="1").order_by('-created_at'),
        })
        return context



class Math3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Math3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="1").order_by('-created_at'),
        })
        return context


class Math4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Math4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="1").order_by('-created_at'),
        })
        return context

class Ph2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ph2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="2").order_by('-created_at'),
        })
        return context

class Ph3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ph3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="2").order_by('-created_at'),
        })
        return context


class Ph4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ph4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="2").order_by('-created_at'),
        })
        return context

class Sc2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Sc2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="3").order_by('-created_at'),
        })
        return context

class Sc3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Sc3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="3").order_by('-created_at'),
        })
        return context


class Sc4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Sc4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="3").order_by('-created_at'),
        })
        return context


class Ti2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ti2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="4").order_by('-created_at'),
        })
        return context

class Ti3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ti3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="4").order_by('-created_at'),
        })
        return context


class Ti4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(TiPost, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="4").order_by('-created_at'),
        })
        return context


class Me2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Me2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="5").order_by('-created_at'),
        })
        return context


class Me3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Me3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="5").order_by('-created_at'),
        })
        return context


class Me4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Me4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="5").order_by('-created_at'),
        })
        return context


class De2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(De2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="6").order_by('-created_at'),
        })
        return context

class De3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(De3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="6").order_by('-created_at'),
        })
        return context

class De4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(De4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="6").order_by('-created_at'),
        })
        return context


class Tu2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Tu2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="7").order_by('-created_at'),
        })
        return context

class Tu3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Tu3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="7").order_by('-created_at'),
        })
        return context


class Tu4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Tu4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="7").order_by('-created_at'),
        })
        return context


class Si2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Si2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="8").order_by('-created_at'),
        })
        return context

class Si3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Si3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="8").order_by('-created_at'),
        })
        return context


class Si4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Si4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="8").order_by('-created_at'),
        })
        return context


class Ke2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ke2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="9").order_by('-created_at'),
        })
        return context

class Ke3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ke3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="9").order_by('-created_at'),
        })
        return context


class Ke4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ke4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="9").order_by('-created_at'),
        })
        return context


class Ma2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ma2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="10").order_by('-created_at'),
        })
        return context


class Ma3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ma3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="10").order_by('-created_at'),
        })
        return context


class Ma4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ma4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="10").order_by('-created_at'),
        })
        return context


class Ou2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ou2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="11").order_by('-created_at'),
        })
        return context

class Ou3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ou3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="11").order_by('-created_at'),
        })
        return context


class Ou4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Ou4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="11").order_by('-created_at'),
        })
        return context


class Su2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Su2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="12").order_by('-created_at'),
        })
        return context


class Su3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Su3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="12").order_by('-created_at'),
        })
        return context

class Su4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Su4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="12").order_by('-created_at'),
        })
        return context


class Jo2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Jo2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="13").order_by('-created_at'),
        })
        return context

class Jo3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Jo3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="13").order_by('-created_at'),
        })
        return context

class Jo4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Jo4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="13").order_by('-created_at'),
        })
        return context

class Se2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Se2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="14").order_by('-created_at'),
        })
        return context

class Se3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Se3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="14").order_by('-created_at'),
        })
        return context

class Se4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Se4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="14").order_by('-created_at'),
        })
        return context


class Bu2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Bu2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="15").order_by('-created_at'),
        })
        return context

class Bu3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Bu3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="15").order_by('-created_at'),
        })
        return context

class Bu4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Bu4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="15").order_by('-created_at'),
        })
        return context

class Do2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Do2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="16").order_by('-created_at'),
        })
        return context

class Do3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Do3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="16").order_by('-created_at'),
        })
        return context

class Do4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Do4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="16").order_by('-created_at'),
        })
        return context

class Yu2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Yu2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="17").order_by('-created_at'),
        })
        return context

class Yu3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Yu3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="17").order_by('-created_at'),
        })
        return context

class Yu4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Yu4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="17").order_by('-created_at'),
        })
        return context

class En2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(En2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="18").order_by('-created_at'),
        })
        return context

class En3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(En3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="18").order_by('-created_at'),
        })
        return context

class En4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(En4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="18").order_by('-created_at'),
        })
        return context



class Sec2Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Sec2Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="1",sub="19").order_by('-created_at'),
        })
        return context

class Sec3Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Sec3Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="2",sub="19").order_by('-created_at'),
        })
        return context

class Sec4Post(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list_sel.html'

    def get_context_data(self, **kwargs):
        context = super(Sec4Post, self).get_context_data(**kwargs)
        context.update({
            'object_list': Post.objects.filter(grade="3",sub="19").order_by('-created_at'),
        })
        return context


def note_grade(request):
    return render(request,'note_grade.html')


def note_b1(request):
    return render(request,'note_b1.html')

def note_b2(request):
    return render(request,'note_b2.html')

def note_b3(request):
    return render(request,'note_b3.html')

def note_b4(request):
    return render(request,'note_b4.html')  
