import pytest
from django.contrib.auth import get_user_model

from apps.cosechas.models import Cosecha
from apps.parcelas.models import Parcela

User = get_user_model()

COSECHAS_URL = "/api/cosechas/"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def parcela(db):
    return Parcela.objects.create(nombre="Parcela Test", area_hectareas="15.00", activa=True)


@pytest.fixture
def parcela2(db):
    return Parcela.objects.create(nombre="Parcela Dos", area_hectareas="8.00", activa=True)


@pytest.fixture
def cosecha(db, parcela, user):
    return Cosecha.objects.create(
        parcela=parcela,
        creado_por=user,
        fecha="2026-03-10",
        racimos_cortados=120,
        rejas_producidas=15,
        peso_kg="500.00",
        precio_kg="4.50",
        notas="",
    )


@pytest.fixture
def cosecha2(db, parcela2, user):
    return Cosecha.objects.create(
        parcela=parcela2,
        creado_por=user,
        fecha="2026-03-15",
        racimos_cortados=80,
        rejas_producidas=10,
        peso_kg="300.00",
        precio_kg="4.00",
        notas="",
    )


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_list_unauthenticated(api_client):
    response = api_client.get(COSECHAS_URL)
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_list(auth_client, cosecha):
    response = auth_client.get(COSECHAS_URL)
    assert response.status_code == 200
    ids = [c["id"] for c in response.data["results"]]
    assert cosecha.id in ids


@pytest.mark.django_db
def test_create(auth_client, parcela, user):
    data = {
        "parcela": parcela.id,
        "fecha": "2026-04-01",
        "racimos_cortados": 100,
        "rejas_producidas": 12,
        "peso_kg": "420.50",
        "precio_kg": "5.00",
        "notas": "",
    }
    response = auth_client.post(COSECHAS_URL, data)
    assert response.status_code == 201
    assert response.data["parcela"] == parcela.id
    assert response.data["creado_por"] == user.id
    assert float(response.data["total_estimado"]) == pytest.approx(420.50 * 5.00)


@pytest.mark.django_db
def test_creado_por_auto_assigned(auth_client, parcela, user):
    data = {
        "parcela": parcela.id,
        "fecha": "2026-05-01",
        "racimos_cortados": 50,
        "rejas_producidas": 6,
        "peso_kg": "200.00",
        "precio_kg": "4.00",
    }
    response = auth_client.post(COSECHAS_URL, data)
    assert response.status_code == 201
    cosecha_db = Cosecha.objects.get(id=response.data["id"])
    assert cosecha_db.creado_por_id == user.id


@pytest.mark.django_db
def test_retrieve(auth_client, cosecha):
    response = auth_client.get(f"{COSECHAS_URL}{cosecha.id}/")
    assert response.status_code == 200
    assert response.data["id"] == cosecha.id
    assert response.data["parcela_nombre"] == cosecha.parcela.nombre


@pytest.mark.django_db
def test_update_patch(auth_client, cosecha):
    response = auth_client.patch(f"{COSECHAS_URL}{cosecha.id}/", {"peso_kg": "600.00"})
    assert response.status_code == 200
    assert float(response.data["peso_kg"]) == 600.00


@pytest.mark.django_db
def test_delete(auth_client, cosecha):
    response = auth_client.delete(f"{COSECHAS_URL}{cosecha.id}/")
    assert response.status_code == 204
    assert not Cosecha.objects.filter(id=cosecha.id).exists()


@pytest.mark.django_db
def test_serializer_includes_total_estimado(auth_client, cosecha):
    response = auth_client.get(f"{COSECHAS_URL}{cosecha.id}/")
    assert "total_estimado" in response.data
    expected = float(cosecha.peso_kg) * float(cosecha.precio_kg)
    assert float(response.data["total_estimado"]) == pytest.approx(expected)


@pytest.mark.django_db
def test_serializer_includes_parcela_nombre(auth_client, cosecha):
    response = auth_client.get(f"{COSECHAS_URL}{cosecha.id}/")
    assert response.data["parcela_nombre"] == cosecha.parcela.nombre


@pytest.mark.django_db
def test_list_ordered_by_fecha_desc(auth_client, cosecha, cosecha2):
    response = auth_client.get(COSECHAS_URL)
    assert response.status_code == 200
    results = response.data["results"]
    fechas = [r["fecha"] for r in results]
    assert fechas == sorted(fechas, reverse=True)


# ---------------------------------------------------------------------------
# Filtros lista
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_filter_by_parcela(auth_client, cosecha, cosecha2):
    response = auth_client.get(f"{COSECHAS_URL}?parcela={cosecha.parcela_id}")
    assert response.status_code == 200
    ids = [c["id"] for c in response.data["results"]]
    assert cosecha.id in ids
    assert cosecha2.id not in ids


@pytest.mark.django_db
def test_filter_by_fecha_inicio(auth_client, cosecha, cosecha2):
    response = auth_client.get(f"{COSECHAS_URL}?fecha_inicio=2026-03-12")
    assert response.status_code == 200
    ids = [c["id"] for c in response.data["results"]]
    assert cosecha2.id in ids
    assert cosecha.id not in ids


@pytest.mark.django_db
def test_filter_by_fecha_fin(auth_client, cosecha, cosecha2):
    response = auth_client.get(f"{COSECHAS_URL}?fecha_fin=2026-03-12")
    assert response.status_code == 200
    ids = [c["id"] for c in response.data["results"]]
    assert cosecha.id in ids
    assert cosecha2.id not in ids


@pytest.mark.django_db
def test_filter_by_rango_fechas(auth_client, cosecha, cosecha2):
    response = auth_client.get(f"{COSECHAS_URL}?fecha_inicio=2026-03-10&fecha_fin=2026-03-10")
    assert response.status_code == 200
    ids = [c["id"] for c in response.data["results"]]
    assert cosecha.id in ids
    assert cosecha2.id not in ids


# ---------------------------------------------------------------------------
# Reporte: por-parcela
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_por_parcela(auth_client, cosecha, cosecha2):
    response = auth_client.get(
        f"{COSECHAS_URL}por-parcela/?fecha_inicio=2026-03-01&fecha_fin=2026-03-31"
    )
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 2
    primero = response.data[0]
    assert "parcela_id" in primero
    assert "parcela_nombre" in primero
    assert "total_peso" in primero
    assert "total_valor" in primero
    # Ordenado de mayor a menor peso
    pesos = [float(r["total_peso"]) for r in response.data]
    assert pesos == sorted(pesos, reverse=True)


@pytest.mark.django_db
def test_por_parcela_rango_vacio(auth_client, cosecha):
    response = auth_client.get(
        f"{COSECHAS_URL}por-parcela/?fecha_inicio=2020-01-01&fecha_fin=2020-01-31"
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_por_parcela_falta_fecha_inicio(auth_client):
    response = auth_client.get(f"{COSECHAS_URL}por-parcela/?fecha_fin=2026-03-31")
    assert response.status_code == 400
    assert "error" in response.data


@pytest.mark.django_db
def test_por_parcela_falta_fecha_fin(auth_client):
    response = auth_client.get(f"{COSECHAS_URL}por-parcela/?fecha_inicio=2026-03-01")
    assert response.status_code == 400


@pytest.mark.django_db
def test_por_parcela_fecha_invalida(auth_client):
    response = auth_client.get(
        f"{COSECHAS_URL}por-parcela/?fecha_inicio=no-es-fecha&fecha_fin=2026-03-31"
    )
    assert response.status_code == 400
    assert "error" in response.data


@pytest.mark.django_db
def test_por_parcela_fin_antes_inicio(auth_client):
    response = auth_client.get(
        f"{COSECHAS_URL}por-parcela/?fecha_inicio=2026-03-31&fecha_fin=2026-03-01"
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_por_parcela_unauthenticated(api_client):
    response = api_client.get(
        f"{COSECHAS_URL}por-parcela/?fecha_inicio=2026-03-01&fecha_fin=2026-03-31"
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Reporte: mensual
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_mensual(auth_client, cosecha, cosecha2):
    response = auth_client.get(f"{COSECHAS_URL}mensual/?anio=2026")
    assert response.status_code == 200
    assert len(response.data) == 12
    meses = [r["mes"] for r in response.data]
    assert meses == list(range(1, 13))


@pytest.mark.django_db
def test_mensual_meses_sin_datos_son_null(auth_client, cosecha):
    response = auth_client.get(f"{COSECHAS_URL}mensual/?anio=2026")
    assert response.status_code == 200
    datos_por_mes = {r["mes"]: r for r in response.data}
    # Marzo tiene datos (fecha 2026-03-10)
    assert datos_por_mes[3]["total_peso"] is not None
    # Enero no tiene datos
    assert datos_por_mes[1]["total_peso"] is None
    assert datos_por_mes[1]["total_valor"] is None


@pytest.mark.django_db
def test_mensual_anio_sin_datos(auth_client):
    response = auth_client.get(f"{COSECHAS_URL}mensual/?anio=2000")
    assert response.status_code == 200
    assert len(response.data) == 12
    assert all(r["total_peso"] is None for r in response.data)


@pytest.mark.django_db
def test_mensual_falta_anio(auth_client):
    response = auth_client.get(f"{COSECHAS_URL}mensual/")
    assert response.status_code == 400
    assert "error" in response.data


@pytest.mark.django_db
def test_mensual_anio_invalido(auth_client):
    response = auth_client.get(f"{COSECHAS_URL}mensual/?anio=abc")
    assert response.status_code == 400


@pytest.mark.django_db
def test_mensual_anio_fuera_de_rango(auth_client):
    response = auth_client.get(f"{COSECHAS_URL}mensual/?anio=1999")
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Reporte: semanal
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_semanal(auth_client, cosecha, cosecha2):
    response = auth_client.get(
        f"{COSECHAS_URL}semanal/?fecha_inicio=2026-03-01&fecha_fin=2026-03-31"
    )
    assert response.status_code == 200
    assert isinstance(response.data, list)
    for item in response.data:
        assert "semana" in item
        assert "total_peso" in item
        assert "total_valor" in item


@pytest.mark.django_db
def test_semanal_rango_vacio(auth_client):
    response = auth_client.get(
        f"{COSECHAS_URL}semanal/?fecha_inicio=2020-01-01&fecha_fin=2020-01-31"
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_semanal_falta_parametros(auth_client):
    response = auth_client.get(f"{COSECHAS_URL}semanal/")
    assert response.status_code == 400


@pytest.mark.django_db
def test_semanal_fecha_invalida(auth_client):
    response = auth_client.get(
        f"{COSECHAS_URL}semanal/?fecha_inicio=2026-03-01&fecha_fin=invalida"
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Reporte: resumen
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_resumen(auth_client, cosecha, cosecha2):
    response = auth_client.get(
        f"{COSECHAS_URL}resumen/?fecha_inicio=2026-03-01&fecha_fin=2026-03-31"
    )
    assert response.status_code == 200
    data = response.data
    assert "total_peso" in data
    assert "total_valor" in data
    assert "num_cosechas" in data
    assert "top_parcela" in data
    assert data["num_cosechas"] == 2
    expected_peso = float(cosecha.peso_kg) + float(cosecha2.peso_kg)
    assert float(data["total_peso"]) == pytest.approx(expected_peso)


@pytest.mark.django_db
def test_resumen_top_parcela(auth_client, cosecha, cosecha2):
    response = auth_client.get(
        f"{COSECHAS_URL}resumen/?fecha_inicio=2026-03-01&fecha_fin=2026-03-31"
    )
    assert response.status_code == 200
    top = response.data["top_parcela"]
    assert top is not None
    # cosecha tiene 500 kg vs cosecha2 con 300 kg
    assert top["parcela_id"] == cosecha.parcela_id
    assert top["parcela_nombre"] == cosecha.parcela.nombre


@pytest.mark.django_db
def test_resumen_rango_vacio(auth_client):
    response = auth_client.get(
        f"{COSECHAS_URL}resumen/?fecha_inicio=2020-01-01&fecha_fin=2020-01-31"
    )
    assert response.status_code == 200
    data = response.data
    assert data["num_cosechas"] == 0
    assert data["total_peso"] is None
    assert data["top_parcela"] is None


@pytest.mark.django_db
def test_resumen_falta_parametros(auth_client):
    response = auth_client.get(f"{COSECHAS_URL}resumen/")
    assert response.status_code == 400


@pytest.mark.django_db
def test_resumen_fecha_invalida(auth_client):
    response = auth_client.get(
        f"{COSECHAS_URL}resumen/?fecha_inicio=2026-13-01&fecha_fin=2026-03-31"
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_resumen_fin_antes_inicio(auth_client):
    response = auth_client.get(
        f"{COSECHAS_URL}resumen/?fecha_inicio=2026-03-31&fecha_fin=2026-03-01"
    )
    assert response.status_code == 400
