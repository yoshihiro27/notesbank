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


def note_li(request):
    notes = Post1.objects.filter(sub1="1").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})    




def note_en1(request):
    notes = Post1.objects.filter(sub1="2").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})

def note_ja(request):
    notes = Post1.objects.filter(sub1="4").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})


def note_te(request):
    notes = Post1.objects.filter(sub1="5").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})


def note_we(request):
    notes = Post1.objects.filter(sub1="6").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})


def note_mt(request):
    notes = Post1.objects.filter(sub1="7").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})


def note_ph(request):
    notes = Post1.objects.filter(sub1="8").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})


def note_ec(request):
    notes = Post1.objects.filter(sub1="9").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})


def note_un(request):
    notes = Post1.objects.filter(sub1="10").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})


def note_ri(request):
    notes = Post1.objects.filter(sub1="11").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})


def note_tc(request):
    notes = Post1.objects.filter(sub1="12").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})


def note_ma(request):
    notes = Post1.objects.filter(sub1="13").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})


def note_ar(request):
    notes = Post1.objects.filter(sub1="14").order_by('-created_at1')
    return render(request,'list_sel1.html', {'notes': notes})



def note_it(request):
    notes = Post1.objects.filter(sub1="14").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})

def note_se(request):
    notes = Post1.objects.filter(sub1="15").order_by('-created_at1'),
    return render(request,'list_sel1.html', {'notes': notes})



def note_math2(request):
    notes = Post.objects.filter(grade="1",sub="1").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_math3(request):
    notes = Post.objects.filter(grade="2",sub="1").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_math4(request):
    notes = Post.objects.filter(grade="3",sub="1").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})



def note_ph2(request):
    notes = Post.objects.filter(grade="1",sub="2").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ph3(request):
    notes = Post.objects.filter(grade="2",sub="2").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ph4(request):
    notes = Post.objects.filter(grade="3",sub="2").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_sc2(request):
    notes = Post.objects.filter(grade="1",sub="3").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_sc3(request):
    notes = Post.objects.filter(grade="2",sub="3").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_sc4(request):
    notes = Post.objects.filter(grade="3",sub="3").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ti2(request):
    notes = Post.objects.filter(grade="1",sub="4").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ti3(request):
    notes = Post.objects.filter(grade="2",sub="4").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ti4(request):
    notes = Post.objects.filter(grade="3",sub="4").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_me2(request):
    notes = Post.objects.filter(grade="1",sub="5").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_me3(request):
    notes = Post.objects.filter(grade="2",sub="5").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_me4(request):
    notes = Post.objects.filter(grade="3",sub="5").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_de2(request):
    notes = Post.objects.filter(grade="1",sub="6").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_de3(request):
    notes = Post.objects.filter(grade="2",sub="6").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_de4(request):
    notes = Post.objects.filter(grade="3",sub="6").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_tu2(request):
    notes = Post.objects.filter(grade="1",sub="7").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_tu3(request):
    notes = Post.objects.filter(grade="2",sub="7").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_tu4(request):
    notes = Post.objects.filter(grade="3",sub="7").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_si2(request):
    notes = Post.objects.filter(grade="1",sub="8").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_si3(request):
    notes = Post.objects.filter(grade="2",sub="8").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_si4(request):
    notes = Post.objects.filter(grade="3",sub="8").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ke2(request):
    notes = Post.objects.filter(grade="1",sub="9").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ke3(request):
    notes = Post.objects.filter(grade="2",sub="9").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ke4(request):
    notes = Post.objects.filter(grade="3",sub="9").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ma2(request):
    notes = Post.objects.filter(grade="1",sub="10").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ma3(request):
    notes = Post.objects.filter(grade="2",sub="10").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ma4(request):
    notes = Post.objects.filter(grade="3",sub="10").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ou2(request):
    notes = Post.objects.filter(grade="1",sub="11").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ou3(request):
    notes = Post.objects.filter(grade="2",sub="11").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_ou4(request):
    notes = Post.objects.filter(grade="3",sub="11").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_su2(request):
    notes = Post.objects.filter(grade="1",sub="12").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})

def note_su3(request):
    notes = Post.objects.filter(grade="2",sub="12").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_su4(request):
    notes = Post.objects.filter(grade="3",sub="12").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_jo2(request):
    notes = Post.objects.filter(grade="1",sub="13").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_jo3(request):
    notes = Post.objects.filter(grade="2",sub="13").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_jo4(request):
    notes = Post.objects.filter(grade="3",sub="13").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_se2(request):
    notes = Post.objects.filter(grade="1",sub="14").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_se3(request):
    notes = Post.objects.filter(grade="2",sub="14").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_se4(request):
    notes = Post.objects.filter(grade="3",sub="14").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_bu2(request):
    notes = Post.objects.filter(grade="1",sub="15").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_bu3(request):
    notes = Post.objects.filter(grade="2",sub="15").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_bu4(request):
    notes = Post.objects.filter(grade="3",sub="15").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_do2(request):
    notes = Post.objects.filter(grade="1",sub="16").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_do3(request):
    notes = Post.objects.filter(grade="2",sub="16").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_do4(request):
    notes = Post.objects.filter(grade="3",sub="16").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_yu2(request):
    notes = Post.objects.filter(grade="1",sub="17").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_yu3(request):
    notes = Post.objects.filter(grade="2",sub="17").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_yu4(request):
    notes = Post.objects.filter(grade="3",sub="17").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_en2(request):
    notes = Post.objects.filter(grade="1",sub="18").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_en3(request):
    notes = Post.objects.filter(grade="2",sub="18").order_by('-created_at'),
    return render(request,'list_sel.html', {'notes': notes})


def note_en4(request):
    notes = Post.objects.filter(grade="3",sub="18").order_by('-created_at')
    return render(request,'list_sel.html', {'notes': notes})


def note_sec2(request):
    notes = Post.objects.filter(grade="1",sub="19").order_by('-created_at')
    return render(request,'list_sel.html', {'notes': notes})


def note_sec3(request):
    notes = Post.objects.filter(grade="2",sub="19").order_by('-created_at')
    return render(request,'list_sel.html', {'notes': notes})


def note_sec4(request):
    notes = Post.objects.filter(grade="3",sub="19").order_by('-created_at')
    return render(request,'list_sel.html', {'notes': notes})


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
