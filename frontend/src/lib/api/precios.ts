import { api } from "./client";
import type {
  ComparacionPeriodos,
  EstadisticasPrecios,
  HistorialPrecio,
  PaginatedResponse,
  TendenciaMensualItem,
} from "@/types";

const BASE = "/api/precios";

function buildQuery(
  params: Partial<Record<string, string | number | undefined>>
): string {
  const usp = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== "") usp.set(key, String(value));
  }
  const qs = usp.toString();
  return qs ? `?${qs}` : "";
}

export interface ListarPreciosParams {
  fecha_inicio?: string;
  fecha_fin?: string;
  page?: number;
}

export interface PrecioInput {
  fecha: string;
  precio_kg: string;
  notas?: string;
}

export function listarPrecios(
  params: ListarPreciosParams = {}
): Promise<PaginatedResponse<HistorialPrecio>> {
  return api.get(
    `${BASE}/${buildQuery({
      fecha_inicio: params.fecha_inicio,
      fecha_fin: params.fecha_fin,
      page: params.page,
    })}`
  );
}

/** Sigue la paginación completa para no truncar la tabla al filtrar por rango de fecha. */
export async function listarTodosPrecios(
  params: Omit<ListarPreciosParams, "page"> = {}
): Promise<HistorialPrecio[]> {
  const acumulado: HistorialPrecio[] = [];
  let page = 1;
  while (true) {
    const resp = await listarPrecios({ ...params, page });
    acumulado.push(...resp.results);
    if (!resp.next) break;
    page += 1;
  }
  return acumulado;
}

export function crearPrecio(data: PrecioInput): Promise<HistorialPrecio> {
  return api.post(`${BASE}/`, data);
}

export function actualizarPrecio(
  id: number,
  data: PrecioInput
): Promise<HistorialPrecio> {
  return api.put(`${BASE}/${id}/`, data);
}

export function eliminarPrecio(id: number): Promise<void> {
  return api.delete(`${BASE}/${id}/`);
}

export function obtenerPrecioActual(): Promise<HistorialPrecio> {
  return api.get(`${BASE}/actual/`);
}

export function obtenerEstadisticas(
  fechaInicio: string,
  fechaFin: string
): Promise<EstadisticasPrecios> {
  return api.get(
    `${BASE}/estadisticas/${buildQuery({
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin,
    })}`
  );
}

export function obtenerTendenciaMensual(
  anio: number
): Promise<TendenciaMensualItem[]> {
  return api.get(`${BASE}/tendencia/${buildQuery({ anio })}`);
}

export interface CompararPeriodosParams {
  p1Inicio: string;
  p1Fin: string;
  p2Inicio: string;
  p2Fin: string;
}

export function compararPeriodos(
  params: CompararPeriodosParams
): Promise<ComparacionPeriodos> {
  return api.get(
    `${BASE}/comparar/${buildQuery({
      p1_inicio: params.p1Inicio,
      p1_fin: params.p1Fin,
      p2_inicio: params.p2Inicio,
      p2_fin: params.p2Fin,
    })}`
  );
}
