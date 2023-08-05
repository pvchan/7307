from django.shortcuts import redirect
from store.models.user import UserRole, CustomUser

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Print the user ID for debugging
        print("Logged-in user ID:", request.user.id)

        # Fetch the user roles
        user_roles = UserRole.objects.filter(user_id=request.user.id)

        # Print the user roles for debugging
        print("User roles retrieved:", [f"{role.user.username} - {role.role}" for role in user_roles])

        if any(role.role.name == 'admin' for role in user_roles):
            return view_func(request, *args, **kwargs)
        else:
            print("User is not an admin.")
            return redirect('/error')
    return wrapper
