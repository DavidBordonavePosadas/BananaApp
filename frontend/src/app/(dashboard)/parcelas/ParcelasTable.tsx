"use client";

import { useEffect, useState } from "react";
import { ApiError, parseApiError } from "@/lib/api/client";
import { eliminarParcela, listarTodasParcelas } from "@/lib/api/parcelas";
import type { Parcela } from "@/types";

interface Props {
  filtroActiva: boolean | undefined;
  refreshToken: number;
  onEdit: (parcela: Parcela) => void;
  onMutated: () => void;
}

export function ParcelasTable({
  filtroActiva,
  refreshToken,
  onEdit,
  onMutated,
}: Props) {
  const [parcelas, setParcelas] = useState<Parcela[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  useEffect(() => {
    let active = true;
    setIsLoading(true);
    setError(null);

    listarTodasParcelas({ activa: filtroActiva })
      .then((results) => {
        if (!active) return;
        setParcelas(results);
      })
      .catch((err) => {
        if (!active) return;
        const parsed = parseApiError(err);
        setError(
          typeof parsed.detail === "string"
            ? parsed.detail
            : "No se pudo cargar la lista de parcelas."
        );
      })
      .finally(() => {
        if (active) setIsLoading(false);
      });

    return () => {
      active = false;
    };
  }, [filtroActiva, refreshToken]);

  async function handleDelete(parcela: Parcela) {
    const confirmed = window.confirm(
      `¿Eliminar la parcela "${parcela.nombre}"? Esta acción no se puede deshacer.`
    );
    if (!confirmed) return;

    setDeletingId(parcela.id);
    try {
      await eliminarParcela(parcela.id);
      onMutated();
    } catch (err) {
      const isProtected = err instanceof ApiError && err.status === 409;
      const parsed = parseApiError(err);
      window.alert(
        isProtected
          ? "No se puede eliminar: la parcela tiene cosechas o registros de trabajo asociados."
          : typeof parsed.detail === "string"
            ? parsed.detail
            : "No se pudo eliminar la parcela."
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
            <th className="px-4 py-3 font-medium">Nombre</th>
            <th className="px-4 py-3 font-medium">Área</th>
            <th className="px-4 py-3 font-medium">Estado</th>
            <th className="px-4 py-3 font-medium">Notas</th>
            <th className="px-4 py-3 font-medium text-right">Acciones</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-neutral-100 dark:divide-neutral-800">
          {isLoading &&
            Array.from({ length: 4 }).map((_, i) => (
              <tr key={i}>
                <td className="px-4 py-3" colSpan={5}>
                  <div className="h-4 w-full animate-pulse rounded bg-neutral-200 dark:bg-neutral-800" />
                </td>
              </tr>
            ))}

          {!isLoading && error && (
            <tr>
              <td
                colSpan={5}
                className="px-4 py-8 text-center text-sm text-red-600 dark:text-red-400"
              >
                {error}
              </td>
            </tr>
          )}

          {!isLoading && !error && parcelas.length === 0 && (
            <tr>
              <td
                colSpan={5}
                className="px-4 py-8 text-center text-sm text-neutral-400 dark:text-neutral-500"
              >
                Sin parcelas registradas.
              </td>
            </tr>
          )}

          {!isLoading &&
            !error &&
            parcelas.map((parcela) => (
              <tr
                key={parcela.id}
                className="text-neutral-700 dark:text-neutral-300"
              >
                <td className="px-4 py-3 font-medium text-neutral-900 dark:text-neutral-50">
                  {parcela.nombre}
                </td>
                <td className="px-4 py-3">
                  {parseFloat(parcela.area_hectareas).toFixed(2)} ha
                </td>
                <td className="px-4 py-3">
                  <span
                    className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${
                      parcela.activa
                        ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400"
                        : "bg-neutral-100 text-neutral-500 dark:bg-neutral-800 dark:text-neutral-400"
                    }`}
                  >
                    {parcela.activa ? "Activa" : "Inactiva"}
                  </span>
                </td>
                <td className="max-w-xs truncate px-4 py-3 text-neutral-500 dark:text-neutral-400">
                  {parcela.notas || "—"}
                </td>
                <td className="px-4 py-3 text-right">
                  <div className="flex justify-end gap-2">
                    <button
                      type="button"
                      onClick={() => onEdit(parcela)}
                      className="rounded-lg px-2 py-1 text-xs font-medium text-emerald-700 transition-colors hover:bg-emerald-50 dark:text-emerald-400 dark:hover:bg-emerald-500/10"
                    >
                      Editar
                    </button>
                    <button
                      type="button"
                      onClick={() => handleDelete(parcela)}
                      disabled={deletingId === parcela.id}
                      className="rounded-lg px-2 py-1 text-xs font-medium text-red-600 transition-colors hover:bg-red-50 disabled:opacity-50 dark:text-red-400 dark:hover:bg-red-500/10"
                    >
                      {deletingId === parcela.id ? "Eliminando..." : "Eliminar"}
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
