from rest_framework import permissions

class IsAdminOrManager(permissions.BasePermission):
    """
    Allows access to Admin users OR users in the 'Managers' group.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        
        if request.user.is_staff or request.user.is_superuser:
            return True
            
        
        return request.user.groups.filter(name='Managers').exists()