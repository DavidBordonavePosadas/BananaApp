import pytest
from django.contrib.auth import get_user_model

from apps.parcelas.models import Parcela

User = get_user_model()

PARCELAS_URL = "/api/parcelas/"


@pytest.fixture
def parcela(db):
    return Parcela.objects.create(nombre="Parcela Norte", area_hectareas="10.50", activa=True)


@pytest.fixture
def parcela_inactiva(db):
    return Parcela.objects.create(nombre="Parcela Sur", area_hectareas="5.00", activa=False)


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_list_unauthenticated(api_client):
    response = api_client.get(PARCELAS_URL)
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_list(auth_client, parcela):
    response = auth_client.get(PARCELAS_URL)
    assert response.status_code == 200
    ids = [p["id"] for p in response.data["results"]]
    assert parcela.id in ids


@pytest.mark.django_db
def test_create(auth_client):
    data = {"nombre": "Parcela Nueva", "area_hectareas": "3.75", "activa": True, "notas": ""}
    response = auth_client.post(PARCELAS_URL, data)
    assert response.status_code == 201
    assert response.data["nombre"] == "Parcela Nueva"
    assert Parcela.objects.filter(nombre="Parcela Nueva").exists()


@pytest.mark.django_db
def test_retrieve(auth_client, parcela):
    response = auth_client.get(f"{PARCELAS_URL}{parcela.id}/")
    assert response.status_code == 200
    assert response.data["id"] == parcela.id
    assert response.data["nombre"] == parcela.nombre


@pytest.mark.django_db
def test_update_patch(auth_client, parcela):
    response = auth_client.patch(f"{PARCELAS_URL}{parcela.id}/", {"nombre": "Parcela Modificada"})
    assert response.status_code == 200
    assert response.data["nombre"] == "Parcela Modificada"


@pytest.mark.django_db
def test_update_put(auth_client, parcela):
    data = {"nombre": "Parcela Completa", "area_hectareas": "8.00", "activa": False, "notas": "Texto"}
    response = auth_client.put(f"{PARCELAS_URL}{parcela.id}/", data)
    assert response.status_code == 200
    assert response.data["activa"] is False


@pytest.mark.django_db
def test_delete(auth_client, parcela):
    response = auth_client.delete(f"{PARCELAS_URL}{parcela.id}/")
    assert response.status_code == 204
    assert not Parcela.objects.filter(id=parcela.id).exists()


@pytest.mark.django_db
def test_retrieve_not_found(auth_client):
    response = auth_client.get(f"{PARCELAS_URL}9999/")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Serializer explicit fields
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_serializer_fields(auth_client, parcela):
    response = auth_client.get(f"{PARCELAS_URL}{parcela.id}/")
    expected = {"id", "nombre", "area_hectareas", "activa", "notas", "created_at", "updated_at"}
    assert set(response.data.keys()) == expected


# ---------------------------------------------------------------------------
# Filtros
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_filter_activa_true(auth_client, parcela, parcela_inactiva):
    response = auth_client.get(f"{PARCELAS_URL}?activa=true")
    assert response.status_code == 200
    results = response.data["results"]
    assert all(p["activa"] for p in results)
    ids = [p["id"] for p in results]
    assert parcela.id in ids
    assert parcela_inactiva.id not in ids


@pytest.mark.django_db
def test_filter_activa_false(auth_client, parcela, parcela_inactiva):
    response = auth_client.get(f"{PARCELAS_URL}?activa=false")
    assert response.status_code == 200
    results = response.data["results"]
    assert all(not p["activa"] for p in results)
    ids = [p["id"] for p in results]
    assert parcela_inactiva.id in ids
    assert parcela.id not in ids


@pytest.mark.django_db
def test_filter_activa_case_insensitive(auth_client, parcela, parcela_inactiva):
    response = auth_client.get(f"{PARCELAS_URL}?activa=True")
    assert response.status_code == 200
    ids = [p["id"] for p in response.data["results"]]
    assert parcela.id in ids


@pytest.mark.django_db
def test_filter_activa_absent_returns_all(auth_client, parcela, parcela_inactiva):
    response = auth_client.get(PARCELAS_URL)
    assert response.status_code == 200
    ids = [p["id"] for p in response.data["results"]]
    assert parcela.id in ids
    assert parcela_inactiva.id in ids


# ---------------------------------------------------------------------------
# Validaciones de creación
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_create_duplicate_nombre(auth_client, parcela):
    data = {"nombre": parcela.nombre, "area_hectareas": "1.00"}
    response = auth_client.post(PARCELAS_URL, data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_missing_required_fields(auth_client):
    response = auth_client.post(PARCELAS_URL, {})
    assert response.status_code == 400
