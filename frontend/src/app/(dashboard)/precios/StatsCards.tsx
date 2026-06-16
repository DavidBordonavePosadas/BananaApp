"use client";

import { useEffect, useState } from "react";
import { ApiError, parseApiError } from "@/lib/api/client";
import { obtenerEstadisticas, obtenerPrecioActual } from "@/lib/api/precios";
import { formatCurrency, formatDate } from "@/lib/format";
import type { EstadisticasPrecios, HistorialPrecio } from "@/types";

interface Props {
  fechaInicio: string;
  fechaFin: string;
  refreshToken: number;
}

export function StatsCards({ fechaInicio, fechaFin, refreshToken }: Props) {
  const [actual, setActual] = useState<HistorialPrecio | null>(null);
  const [stats, setStats] = useState<EstadisticasPrecios | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setIsLoading(true);
    setError(null);

    async function load() {
      try {
        const [actualResult, statsResult] = await Promise.all([
          obtenerPrecioActual().catch((err) => {
            if (err instanceof ApiError && err.status === 404) return null;
            throw err;
          }),
          obtenerEstadisticas(fechaInicio, fechaFin),
        ]);
        if (!active) return;
        setActual(actualResult);
        setStats(statsResult);
      } catch (err) {
        if (!active) return;
        const parsed = parseApiError(err);
        setError(
          typeof parsed.detail === "string"
            ? parsed.detail
            : "No se pudieron cargar las estadísticas."
        );
      } finally {
        if (active) setIsLoading(false);
      }
    }

    load();
    return () => {
      active = false;
    };
  }, [fechaInicio, fechaFin, refreshToken]);

  if (error) {
    return (
      <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950 dark:text-red-400">
        {error}
      </div>
    );
  }

  const cards = [
    {
      label: "Precio actual",
      value: actual ? formatCurrency(actual.precio_kg) : "—",
      hint: actual ? formatDate(actual.fecha) : "Sin registros",
    },
    {
      label: "Promedio del periodo",
      value: stats?.promedio ? formatCurrency(stats.promedio) : "—",
      hint: stats
        ? `${stats.total} registro${stats.total === 1 ? "" : "s"}`
        : "",
    },
    {
      label: "Máximo del periodo",
      value: stats?.maximo ? formatCurrency(stats.maximo.precio_kg) : "—",
      hint: stats?.maximo ? formatDate(stats.maximo.fecha) : "Sin datos",
    },
    {
      label: "Mínimo del periodo",
      value: stats?.minimo ? formatCurrency(stats.minimo.precio_kg) : "—",
      hint: stats?.minimo ? formatDate(stats.minimo.fecha) : "Sin datos",
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {cards.map((card) => (
        <div
          key={card.label}
          className="rounded-2xl border border-neutral-200 bg-white p-5 dark:border-neutral-800 dark:bg-neutral-900"
        >
          <p className="text-sm font-medium text-neutral-500 dark:text-neutral-400">
            {card.label}
          </p>
          {isLoading ? (
            <div className="mt-2 h-8 w-24 animate-pulse rounded bg-neutral-200 dark:bg-neutral-800" />
          ) : (
            <p className="mt-1 text-3xl font-semibold text-neutral-900 dark:text-neutral-50">
              {card.value}
            </p>
          )}
          {!isLoading && (
            <p className="mt-1 text-xs text-neutral-400 dark:text-neutral-500">
              {card.hint}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
