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

export interface PrecioExtremo {
  precio_kg: string;
  fecha: string;
}

export interface EstadisticasPrecios {
  total: number;
  promedio: string | null;
  maximo: PrecioExtremo | null;
  minimo: PrecioExtremo | null;
}

export interface TendenciaMensualItem {
  mes: number;
  promedio: string | null;
}

export interface ComparacionPeriodos {
  periodo_1: EstadisticasPrecios;
  periodo_2: EstadisticasPrecios;
  diferencia_porcentual: string | null;
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

export interface Venta {
  id: number;
  cliente: number;
  fecha: string;
  peso_kg: string;
  precio_kg: string;
  total: number;
  notas: string;
  created_at: string;
  updated_at: string;
}

export interface TipoInsumo {
  id: number;
  nombre: string;
  activo: boolean;
}

export interface CompraInsumo {
  id: number;
  tipo_insumo: number;
  creado_por: number;
  fecha: string;
  cantidad: string | null;
  unidad: string;
  costo: string;
  proveedor: string;
  notas: string;
  created_at: string;
  updated_at: string;
}

export interface Nota {
  id: number;
  creado_por: number;
  fecha: string;
  titulo: string;
  contenido: string;
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
