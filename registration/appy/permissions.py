from rest_framework.permissions import BasePermission

class CanChangeBookshopPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'can_change_bookshop' permission
        return request.user.has_perm('appy.can_change_bookshop')

class CanChangeFlowershopPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'can_change_flower' permission
        return request.user.has_perm('appy.can_change_flowershop')
class CanChangeDishPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'can_change_dish' permission
        return request.user.has_perm('appy.can_change_dish')
    
class CanChangeElectronicsshopPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'can_change_electronicsshop' permission
        return request.user.has_perm('appy.can_change_electronicsshop')
    

class IsAdminOrRegularUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in [1, 2]  # Allow admin and regular user

    