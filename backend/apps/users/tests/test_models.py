import pytest

from apps.users.models import Usuario


@pytest.mark.django_db
def test_usuario_default_rol():
    user = Usuario.objects.create_user(username="operador1", password="pass123")
    assert user.rol == Usuario.Rol.OPERADOR


@pytest.mark.django_db
def test_usuario_admin_rol():
    user = Usuario.objects.create_user(
        username="admin1", password="pass123", rol=Usuario.Rol.ADMIN
    )
    assert user.rol == Usuario.Rol.ADMIN
