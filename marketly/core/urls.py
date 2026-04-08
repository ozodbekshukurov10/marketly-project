from django.urls import path

from . import views


urlpatterns = [
    path('', views.page_view, {'template_name': 'index.html'}, name='home'),
    path('index.html', views.page_view, {'template_name': 'index.html'}, name='index'),
    path('login.html', views.page_view, {'template_name': 'login.html'}, name='login'),
    path('admin-panel.html', views.page_view, {'template_name': 'admin-panel.html'}, name='admin-panel'),
    path('admin-security.html', views.page_view, {'template_name': 'admin-security.html'}, name='admin-security'),
    path('manager-panel.html', views.page_view, {'template_name': 'manager-panel.html'}, name='manager-panel'),
    path('boshlash.html', views.page_view, {'template_name': 'boshlash.html'}, name='boshlash'),
    path('profile.html', views.page_view, {'template_name': 'profile.html'}, name='profile'),
    path('role-select.html', views.page_view, {'template_name': 'role-select.html'}, name='role-select'),
    path('tadbirkor.html', views.page_view, {'template_name': 'tadbirkor.html'}, name='tadbirkor'),
    path('xaridor.html', views.page_view, {'template_name': 'xaridor.html'}, name='xaridor'),
    path('feed.html', views.page_view, {'template_name': 'feed.html'}, name='feed'),
    path('kabinet.html', views.page_view, {'template_name': 'kabinet.html'}, name='kabinet'),
    path('mahsulotlar.html', views.page_view, {'template_name': 'mahsulotlar.html'}, name='mahsulotlar'),
    path('xizmatlar.html', views.page_view, {'template_name': 'xizmatlar.html'}, name='xizmatlar'),
    path('boglanish.html', views.page_view, {'template_name': 'boglanish.html'}, name='boglanish'),
    path('batafsil_malumot.html', views.page_view, {'template_name': 'batafsil_malumot.html'}, name='batafsil'),
    path('save-data', views.save_data, name='save-data'),
    path('save-profile', views.save_profile, name='save-profile'),
    path('save-final-user', views.save_final_user, name='save-final-user'),
    path('add-product', views.add_product, name='add-product'),
    path('api/get-products', views.get_products, name='get-products'),
    path('api/orders', views.create_order, name='create-order'),
    path('api/user-orders', views.user_orders, name='user-orders'),
    path('api/save-compare', views.save_compare, name='save-compare'),
    path('api/admin/login', views.admin_login, name='admin-login'),
    path('api/admin/session', views.admin_session, name='admin-session'),
    path('api/admin/logout', views.admin_logout, name='admin-logout'),
    path('api/admin/dashboard', views.admin_dashboard, name='admin-dashboard'),
    path('api/admin/security/toggle', views.admin_security_toggle, name='admin-security-toggle'),
    path('api/admin/security/overview', views.admin_security_overview, name='admin-security-overview'),
    path('api/admin/manager-dashboard', views.manager_dashboard, name='manager-dashboard'),
]
