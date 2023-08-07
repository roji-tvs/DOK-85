from rest_framework import permissions


class HasBookShopPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # if request.user.role == 'Superuser':
        #     return True
        return(request.user.id==1 and
            #    request.user.is_authenticated and
               request.user.username=="pool" and
               request.method in ['POST', 'PUT', 'GET'] and
               not request.method == 'DELETE')

class HasFlowerShopPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return(request.user.id==2 and
               request.user.is_authenticated and
               request.user.username=="rool" and 
               request.method in ['POST', 'PUT', 'GET'] and
               not request.method == 'DELETE')
class HasDishPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return(request.user.id==3 and 
               request.user.is_authenticated and
               request.user.username=="rrr" and
               request.method in ['POST', 'PUT', 'GET'] and
               not request.method == 'DELETE')

class HasElectronicsShopPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return( (request.user.id==4 or request.user.id==5) and
               request.user.is_authenticated and
               (request.user.username=="sss" or  request.user.username=='poky') and
               request.method in ['POST', 'PUT', 'GET'] and
               not request.method == 'DELETE' )