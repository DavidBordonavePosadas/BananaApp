"use client";

import { useEffect, useState, type FormEvent } from "react";
import { parseApiError } from "@/lib/api/client";
import { actualizarParcela, crearParcela } from "@/lib/api/parcelas";
import type { Parcela } from "@/types";

interface Props {
  isOpen: boolean;
  parcela: Parcela | null;
  onClose: () => void;
  onSaved: () => void;
}

export function ParcelaFormPanel({ isOpen, parcela, onClose, onSaved }: Props) {
  const [nombre, setNombre] = useState("");
  const [areaHectareas, setAreaHectareas] = useState("");
  const [activa, setActiva] = useState(true);
  const [notas, setNotas] = useState("");
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [generalError, setGeneralError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!isOpen) return;
    setFieldErrors({});
    setGeneralError(null);
    if (parcela) {
      setNombre(parcela.nombre);
      setAreaHectareas(parcela.area_hectareas);
      setActiva(parcela.activa);
      setNotas(parcela.notas);
    } else {
      setNombre("");
      setAreaHectareas("");
      setActiva(true);
      setNotas("");
    }
  }, [isOpen, parcela]);

  if (!isOpen) return null;

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setIsSubmitting(true);
    setFieldErrors({});
    setGeneralError(null);

    try {
      const data = { nombre, area_hectareas: areaHectareas, activa, notas };
      if (parcela) {
        await actualizarParcela(parcela.id, data);
      } else {
        await crearParcela(data);
      }
      onSaved();
    } catch (err) {
      const parsed = parseApiError(err);
      const nextFieldErrors: Record<string, string> = {};
      let nextGeneralError: string | null = null;

      for (const [key, value] of Object.entries(parsed)) {
        const message = Array.isArray(value) ? value.join(" ") : String(value);
        if (key === "detail") {
          nextGeneralError = message;
        } else {
          nextFieldErrors[key] = message;
        }
      }

      setFieldErrors(nextFieldErrors);
      setGeneralError(
        nextGeneralError ??
          (Object.keys(nextFieldErrors).length === 0
            ? "No se pudo guardar el registro."
            : null)
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      <button
        type="button"
        aria-label="Cerrar"
        onClick={onClose}
        className="absolute inset-0 bg-black/30"
      />

      <form
        onSubmit={handleSubmit}
        className="relative flex h-full w-full max-w-md flex-col border-l border-neutral-200 bg-white p-6 shadow-xl dark:border-neutral-800 dark:bg-neutral-900"
      >
        <h2 className="text-lg font-semibold text-neutral-900 dark:text-neutral-50">
          {parcela ? "Editar parcela" : "Nueva parcela"}
        </h2>

        <div className="mt-6 flex-1 space-y-4 overflow-y-auto">
          {generalError && (
            <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950 dark:text-red-400">
              {generalError}
            </p>
          )}

          <div>
            <label
              htmlFor="nombre"
              className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300"
            >
              Nombre
            </label>
            <input
              id="nombre"
              type="text"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
              placeholder="Ej. Parcela Norte"
              className="w-full rounded-lg border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900 outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 dark:border-neutral-700 dark:bg-neutral-800 dark:text-neutral-100"
            />
            {fieldErrors.nombre && (
              <p className="mt-1 text-xs text-red-600 dark:text-red-400">
                {fieldErrors.nombre}
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="area_hectareas"
              className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300"
            >
              Área (hectáreas)
            </label>
            <input
              id="area_hectareas"
              type="number"
              step="0.01"
              min="0"
              value={areaHectareas}
              onChange={(e) => setAreaHectareas(e.target.value)}
              required
              placeholder="Ej. 5.50"
              className="w-full rounded-lg border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900 outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 dark:border-neutral-700 dark:bg-neutral-800 dark:text-neutral-100"
            />
            {fieldErrors.area_hectareas && (
              <p className="mt-1 text-xs text-red-600 dark:text-red-400">
                {fieldErrors.area_hectareas}
              </p>
            )}
          </div>

          <div className="flex items-center gap-3 rounded-lg border border-neutral-200 px-3 py-2.5 dark:border-neutral-700">
            <input
              id="activa"
              type="checkbox"
              checked={activa}
              onChange={(e) => setActiva(e.target.checked)}
              className="h-4 w-4 rounded border-neutral-300 accent-emerald-600"
            />
            <label
              htmlFor="activa"
              className="cursor-pointer text-sm font-medium text-neutral-700 dark:text-neutral-300"
            >
              Parcela activa
            </label>
          </div>

          <div>
            <label
              htmlFor="notas"
              className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300"
            >
              Notas
            </label>
            <textarea
              id="notas"
              value={notas}
              onChange={(e) => setNotas(e.target.value)}
              rows={4}
              className="w-full resize-none rounded-lg border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900 outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 dark:border-neutral-700 dark:bg-neutral-800 dark:text-neutral-100"
            />
            {fieldErrors.notas && (
              <p className="mt-1 text-xs text-red-600 dark:text-red-400">
                {fieldErrors.notas}
              </p>
            )}
          </div>
        </div>

        <div className="mt-6 flex justify-end gap-3">
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg border border-neutral-300 px-4 py-2 text-sm font-medium text-neutral-700 transition-colors hover:bg-neutral-100 dark:border-neutral-700 dark:text-neutral-300 dark:hover:bg-neutral-800"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSubmitting ? "Guardando..." : "Guardar"}
          </button>
        </div>
      </form>
    </div>
  );
}
