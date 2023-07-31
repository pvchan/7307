from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models.user import CustomUser, UserRole, Role

class ViewUsers(View):
    def get(self, request):
        roles = Role.objects.all()  # Fetch all roles
        return render(request, 'viewusers.html', {'roles': roles})


class EditUser(View):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        roles = Role.objects.all()
        return render(request, 'edituser.html', {'user': user, 'roles': roles})

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)

        role_id = request.POST.get('role')
        if role_id:
            user_role = UserRole.objects.get(user=user)
            user_role.role = Role.objects.get(id=role_id)
            user_role.save()

        user.save()
        return redirect('viewusers')
