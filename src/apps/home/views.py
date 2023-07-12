from typing import Optional
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import TemplateView

def home_view(request):
    return render(request, "pages/home.html", {})

def blog_view(request):
    return render(request, "pages/blog.html",{})


class blogview(UserPassesTestMixin, TemplateView):
    template_name = "pages/blog.html"
    permission_required = "user.can_view_user"

    def test_func(self) -> bool | None:
        return self.request.user.has_perm(self.permission_required)


# class contact_view(UserPassesTestMixin, TemplateView):
    # permission_required = "user.can_view_user"

    # def test_func(self) -> bool | None:
    #     return self.request.user.has_perm(self.permission_required)
class contact_view(TemplateView):
    template_name = "pages/contact.html"

