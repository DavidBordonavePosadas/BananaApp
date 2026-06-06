export type Rol = "ADMIN" | "OPERADOR";

export interface Usuario {
  id: number;
  username: string;
  email: string;
  rol: Rol;
  is_active: boolean;
  date_joined: string;
}

export interface Parcela {
  id: number;
  nombre: string;
  area_hectareas: string;
  activa: boolean;
  notas: string;
  created_at: string;
  updated_at: string;
}

export interface Cosecha {
  id: number;
  parcela: number;
  creado_por: number;
  fecha: string;
  racimos_cortados: number;
  rejas_producidas: number;
  peso_kg: string;
  precio_kg: string;
  total_estimado: number;
  notas: string;
  created_at: string;
  updated_at: string;
}

export interface HistorialPrecio {
  id: number;
  fecha: string;
  precio_kg: string;
  notas: string;
  created_at: string;
}

export interface Trabajador {
  id: number;
  nombre: string;
  telefono: string;
  activo: boolean;
  notas: string;
  created_at: string;
  updated_at: string;
}

export interface Actividad {
  id: number;
  nombre: string;
}

export interface RegistroTrabajo {
  id: number;
  trabajador: number;
  parcela: number | null;
  actividad: number;
  fecha: string;
  pago: string;
  notas: string;
  created_at: string;
}

export interface Cliente {
  id: number;
  nombre: string;
  telefono: string;
  direccion: string;
  observaciones: string;
  activo: boolean;
  created_at: string;
  updated_at: string;
}

export type EstadoPago = "PENDIENTE" | "PARCIAL" | "PAGADO";

export interface Venta {
  id: number;
  cliente: number;
  fecha: string;
  peso_kg: string;
  precio_kg: string;
  monto_pagado: string;
  total: number;
  estado_pago: EstadoPago;
  notas: string;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface TokenPair {
  access: string;
  refresh: string;
}
