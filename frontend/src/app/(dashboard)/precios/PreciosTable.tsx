"use client";

import { useEffect, useState } from "react";
import { parseApiError } from "@/lib/api/client";
import { eliminarPrecio, listarTodosPrecios } from "@/lib/api/precios";
import { formatCurrency, formatDate } from "@/lib/format";
import type { HistorialPrecio } from "@/types";

interface Props {
  fechaInicio: string;
  fechaFin: string;
  refreshToken: number;
  onEdit: (precio: HistorialPrecio) => void;
  onMutated: () => void;
}

export function PreciosTable({
  fechaInicio,
  fechaFin,
  refreshToken,
  onEdit,
  onMutated,
}: Props) {
  const [precios, setPrecios] = useState<HistorialPrecio[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  useEffect(() => {
    let active = true;
    setIsLoading(true);
    setError(null);

    listarTodosPrecios({ fecha_inicio: fechaInicio, fecha_fin: fechaFin })
      .then((results) => {
        if (!active) return;
        setPrecios(results);
      })
      .catch((err) => {
        if (!active) return;
        const parsed = parseApiError(err);
        setError(
          typeof parsed.detail === "string"
            ? parsed.detail
            : "No se pudo cargar la lista de precios."
        );
      })
      .finally(() => {
        if (active) setIsLoading(false);
      });

    return () => {
      active = false;
    };
  }, [fechaInicio, fechaFin, refreshToken]);

  async function handleDelete(precio: HistorialPrecio) {
    const confirmed = window.confirm(
      `¿Eliminar el precio del ${formatDate(precio.fecha)}? Esta acción no se puede deshacer.`
    );
    if (!confirmed) return;

    setDeletingId(precio.id);
    try {
      await eliminarPrecio(precio.id);
      onMutated();
    } catch (err) {
      const parsed = parseApiError(err);
      window.alert(
        typeof parsed.detail === "string"
          ? parsed.detail
          : "No se pudo eliminar el registro."
      );
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-neutral-200 bg-white dark:border-neutral-800 dark:bg-neutral-900">
      <table className="w-full text-sm">
        <thead className="border-b border-neutral-200 bg-neutral-50 text-left text-neutral-500 dark:border-neutral-800 dark:bg-neutral-950 dark:text-neutral-400">
          <tr>
            <th className="px-4 py-3 font-medium">Fecha</th>
            <th className="px-4 py-3 font-medium">Precio/kg</th>
            <th className="px-4 py-3 font-medium">Notas</th>
            <th className="px-4 py-3 font-medium text-right">Acciones</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-neutral-100 dark:divide-neutral-800">
          {isLoading &&
            Array.from({ length: 4 }).map((_, i) => (
              <tr key={i}>
                <td className="px-4 py-3" colSpan={4}>
                  <div className="h-4 w-full animate-pulse rounded bg-neutral-200 dark:bg-neutral-800" />
                </td>
              </tr>
            ))}

          {!isLoading && error && (
            <tr>
              <td
                colSpan={4}
                className="px-4 py-8 text-center text-sm text-red-600 dark:text-red-400"
              >
                {error}
              </td>
            </tr>
          )}

          {!isLoading && !error && precios.length === 0 && (
            <tr>
              <td
                colSpan={4}
                className="px-4 py-8 text-center text-sm text-neutral-400 dark:text-neutral-500"
              >
                Sin registros en el periodo seleccionado.
              </td>
            </tr>
          )}

          {!isLoading &&
            !error &&
            precios.map((precio) => (
              <tr key={precio.id} className="text-neutral-700 dark:text-neutral-300">
                <td className="px-4 py-3">{formatDate(precio.fecha)}</td>
                <td className="px-4 py-3 font-medium text-neutral-900 dark:text-neutral-50">
                  {formatCurrency(precio.precio_kg)}
                </td>
                <td className="max-w-xs truncate px-4 py-3 text-neutral-500 dark:text-neutral-400">
                  {precio.notas || "—"}
                </td>
                <td className="px-4 py-3 text-right">
                  <div className="flex justify-end gap-2">
                    <button
                      type="button"
                      onClick={() => onEdit(precio)}
                      className="rounded-lg px-2 py-1 text-xs font-medium text-emerald-700 transition-colors hover:bg-emerald-50 dark:text-emerald-400 dark:hover:bg-emerald-500/10"
                    >
                      Editar
                    </button>
                    <button
                      type="button"
                      onClick={() => handleDelete(precio)}
                      disabled={deletingId === precio.id}
                      className="rounded-lg px-2 py-1 text-xs font-medium text-red-600 transition-colors hover:bg-red-50 disabled:opacity-50 dark:text-red-400 dark:hover:bg-red-500/10"
                    >
                      {deletingId === precio.id ? "Eliminando..." : "Eliminar"}
                    </button>
                  </div>
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
}
