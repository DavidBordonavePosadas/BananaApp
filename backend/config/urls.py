from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import LogoutView, MeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/me/", MeView.as_view(), name="auth_me"),
    path("api/auth/logout/", LogoutView.as_view(), name="auth_logout"),
    path("api/parcelas/", include("apps.parcelas.urls")),
    path("api/cosechas/", include("apps.cosechas.urls")),
    path("api/precios/", include("apps.precios.urls")),
    path("api/trabajadores/", include("apps.trabajadores.urls")),
    path("api/clientes/", include("apps.clientes.urls")),
    path("api/ventas/", include("apps.ventas.urls")),
    path("api/insumos/", include("apps.insumos.urls")),
    path("api/notas/", include("apps.notas.urls")),
]
