import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.precios.models import HistorialPrecio

User = get_user_model()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def usuario(db):
    return User.objects.create_user(username="tester", password="pass1234")


@pytest.fixture
def client(api_client, usuario):
    api_client.force_authenticate(user=usuario)
    return api_client


@pytest.fixture
def precios(db):
    datos = [
        ("2026-01-15", "4.50"),
        ("2026-02-10", "5.00"),
        ("2026-03-20", "5.50"),
        ("2026-04-05", "6.00"),
        ("2026-06-01", "5.80"),
    ]
    return [
        HistorialPrecio.objects.create(fecha=fecha, precio_kg=precio)
        for fecha, precio in datos
    ]


# ---------------------------------------------------------------------------
# /api/precios/actual/
# ---------------------------------------------------------------------------


class TestPrecioActual:
    def test_devuelve_el_mas_reciente(self, client, precios):
        resp = client.get("/api/precios/actual/")
        assert resp.status_code == 200
        assert resp.data["fecha"] == "2026-06-01"

    def test_404_sin_registros(self, client, db):
        resp = client.get("/api/precios/actual/")
        assert resp.status_code == 404

    def test_requiere_autenticacion(self, api_client, precios):
        resp = api_client.get("/api/precios/actual/")
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# /api/precios/estadisticas/
# ---------------------------------------------------------------------------


class TestEstadisticas:
    def test_rango_valido(self, client, precios):
        resp = client.get(
            "/api/precios/estadisticas/?fecha_inicio=2026-01-01&fecha_fin=2026-04-30"
        )
        assert resp.status_code == 200
        data = resp.data
        assert data["total"] == 4
        assert data["maximo"]["fecha"] == "2026-04-05"
        assert data["minimo"]["fecha"] == "2026-01-15"
        assert data["promedio"] is not None

    def test_rango_vacio(self, client, precios):
        resp = client.get(
            "/api/precios/estadisticas/?fecha_inicio=2025-01-01&fecha_fin=2025-12-31"
        )
        assert resp.status_code == 200
        assert resp.data["total"] == 0
        assert resp.data["promedio"] is None
        assert resp.data["maximo"] is None
        assert resp.data["minimo"] is None

    def test_falta_fecha_fin(self, client, precios):
        resp = client.get("/api/precios/estadisticas/?fecha_inicio=2026-01-01")
        assert resp.status_code == 400

    def test_falta_fecha_inicio(self, client, precios):
        resp = client.get("/api/precios/estadisticas/?fecha_fin=2026-12-31")
        assert resp.status_code == 400

    def test_formato_fecha_invalido(self, client, precios):
        resp = client.get(
            "/api/precios/estadisticas/?fecha_inicio=01/01/2026&fecha_fin=2026-12-31"
        )
        assert resp.status_code == 400

    def test_rango_invertido(self, client, precios):
        resp = client.get(
            "/api/precios/estadisticas/?fecha_inicio=2026-12-31&fecha_fin=2026-01-01"
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# /api/precios/tendencia/
# ---------------------------------------------------------------------------


class TestTendencia:
    def test_retorna_12_meses(self, client, precios):
        resp = client.get("/api/precios/tendencia/?anio=2026")
        assert resp.status_code == 200
        assert len(resp.data) == 12

    def test_meses_con_datos(self, client, precios):
        resp = client.get("/api/precios/tendencia/?anio=2026")
        data = {item["mes"]: item["promedio"] for item in resp.data}
        assert data[1] is not None   # enero
        assert data[2] is not None   # febrero
        assert data[3] is not None   # marzo
        assert data[4] is not None   # abril
        assert data[6] is not None   # junio

    def test_meses_sin_datos_son_null(self, client, precios):
        resp = client.get("/api/precios/tendencia/?anio=2026")
        data = {item["mes"]: item["promedio"] for item in resp.data}
        assert data[5] is None    # mayo: sin datos
        assert data[7] is None    # julio: sin datos
        assert data[12] is None   # diciembre: sin datos

    def test_anio_sin_datos(self, client, precios):
        resp = client.get("/api/precios/tendencia/?anio=2020")
        assert resp.status_code == 200
        assert len(resp.data) == 12
        assert all(item["promedio"] is None for item in resp.data)

    def test_falta_anio(self, client, precios):
        resp = client.get("/api/precios/tendencia/")
        assert resp.status_code == 400

    def test_anio_no_numerico(self, client, precios):
        resp = client.get("/api/precios/tendencia/?anio=veintiseis")
        assert resp.status_code == 400

    def test_anio_fuera_de_rango(self, client, precios):
        resp = client.get("/api/precios/tendencia/?anio=1999")
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# /api/precios/comparar/
# ---------------------------------------------------------------------------


class TestComparar:
    BASE = (
        "/api/precios/comparar/"
        "?p1_inicio=2026-01-01&p1_fin=2026-02-28"
        "&p2_inicio=2026-03-01&p2_fin=2026-06-30"
    )

    def test_comparacion_valida(self, client, precios):
        resp = client.get(self.BASE)
        assert resp.status_code == 200
        data = resp.data
        assert data["periodo_1"]["total"] == 2
        assert data["periodo_2"]["total"] == 3
        assert data["diferencia_porcentual"] is not None

    def test_periodo_vacio(self, client, precios):
        resp = client.get(
            "/api/precios/comparar/"
            "?p1_inicio=2025-01-01&p1_fin=2025-12-31"
            "&p2_inicio=2026-01-01&p2_fin=2026-06-30"
        )
        assert resp.status_code == 200
        assert resp.data["periodo_1"]["total"] == 0
        assert resp.data["diferencia_porcentual"] is None

    def test_falta_parametro(self, client, precios):
        resp = client.get(
            "/api/precios/comparar/"
            "?p1_inicio=2026-01-01&p1_fin=2026-02-28&p2_inicio=2026-03-01"
        )
        assert resp.status_code == 400

    def test_formato_invalido(self, client, precios):
        resp = client.get(
            "/api/precios/comparar/"
            "?p1_inicio=2026/01/01&p1_fin=2026-02-28"
            "&p2_inicio=2026-03-01&p2_fin=2026-06-30"
        )
        assert resp.status_code == 400

    def test_rango_p1_invertido(self, client, precios):
        resp = client.get(
            "/api/precios/comparar/"
            "?p1_inicio=2026-06-01&p1_fin=2026-01-01"
            "&p2_inicio=2026-03-01&p2_fin=2026-06-30"
        )
        assert resp.status_code == 400

    def test_rango_p2_invertido(self, client, precios):
        resp = client.get(
            "/api/precios/comparar/"
            "?p1_inicio=2026-01-01&p1_fin=2026-02-28"
            "&p2_inicio=2026-06-30&p2_fin=2026-03-01"
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# GET /api/precios/ con filtros
# ---------------------------------------------------------------------------


class TestListFilter:
    def test_sin_filtro(self, client, precios):
        resp = client.get("/api/precios/")
        assert resp.status_code == 200
        assert resp.data["count"] == 5

    def test_filtro_fecha_inicio(self, client, precios):
        resp = client.get("/api/precios/?fecha_inicio=2026-03-01")
        assert resp.status_code == 200
        assert resp.data["count"] == 3  # marzo, abril, junio

    def test_filtro_rango(self, client, precios):
        resp = client.get(
            "/api/precios/?fecha_inicio=2026-02-01&fecha_fin=2026-04-30"
        )
        assert resp.status_code == 200
        assert resp.data["count"] == 3  # febrero, marzo, abril

    def test_fecha_mal_formateada(self, client, precios):
        resp = client.get("/api/precios/?fecha_inicio=bad-date")
        assert resp.status_code == 400

    def test_rango_invertido(self, client, precios):
        resp = client.get(
            "/api/precios/?fecha_inicio=2026-12-31&fecha_fin=2026-01-01"
        )
        assert resp.status_code == 400
