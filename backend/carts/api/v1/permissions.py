from rest_framework.permissions import BasePermission



class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        user=request.user
        if user.is_authenticated:
            return obj.cart.user==user
        else:
            session=request.session.session_key
            if not session:
                request.session.create()
                session = request.session.session_key
            return obj.cart.session==session