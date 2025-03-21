from django.contrib import admin

class MiAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Define el orden deseado de las aplicaciones y modelos
        orden_aplicaciones = [
            {'name': 'Registro', 'models': [
                {'name': 'Registro', 'admin_url': '/admin/app_label/registro/'},
                {'name': 'Garantia', 'admin_url': '/admin/app_label/garantia/'},
            ]},
            {'name': 'Cliente', 'models': [
                {'name': 'Cliente', 'admin_url': '/admin/app_label/cliente/'},
            ]},
            {'name': 'Empresa', 'models': [
                {'name': 'Empresa', 'admin_url': '/admin/app_label/empresa/'},
            ]},
            {'name': 'Triciclo', 'models': [
                {'name': 'Triciclo', 'admin_url': '/admin/app_label/triciclo/'},
            ]},
            {'name': 'Power Station', 'models': [
                {'name': 'Power Station', 'admin_url': '/admin/app_label/power_station/'},
            ]},
        ]
        return orden_aplicaciones

mi_admin_site = MiAdminSite(name='miadmin')