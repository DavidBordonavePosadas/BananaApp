import { api } from "./client";
import type { Parcela, PaginatedResponse } from "@/types";

const BASE = "/api/parcelas";

export interface ParcelaInput {
  nombre: string;
  area_hectareas: string;
  activa?: boolean;
  notas?: string;
}

export interface ListarParcelasParams {
  activa?: boolean;
  page?: number;
}

export function listarParcelas(
  params: ListarParcelasParams = {}
): Promise<PaginatedResponse<Parcela>> {
  const usp = new URLSearchParams();
  if (params.activa !== undefined) usp.set("activa", String(params.activa));
  if (params.page !== undefined) usp.set("page", String(params.page));
  const qs = usp.toString();
  return api.get(`${BASE}/${qs ? `?${qs}` : ""}`);
}

export async function listarTodasParcelas(
  params: Omit<ListarParcelasParams, "page"> = {}
): Promise<Parcela[]> {
  const acumulado: Parcela[] = [];
  let page = 1;
  while (true) {
    const resp = await listarParcelas({ ...params, page });
    acumulado.push(...resp.results);
    if (!resp.next) break;
    page += 1;
  }
  return acumulado;
}

export function crearParcela(data: ParcelaInput): Promise<Parcela> {
  return api.post(`${BASE}/`, data);
}

export function actualizarParcela(id: number, data: ParcelaInput): Promise<Parcela> {
  return api.put(`${BASE}/${id}/`, data);
}

export function eliminarParcela(id: number): Promise<void> {
  return api.delete(`${BASE}/${id}/`);
}
