"use client";

import { useEffect, useState, type FormEvent } from "react";
import { parseApiError } from "@/lib/api/client";
import { actualizarPrecio, crearPrecio } from "@/lib/api/precios";
import type { HistorialPrecio } from "@/types";

interface Props {
  isOpen: boolean;
  precio: HistorialPrecio | null;
  onClose: () => void;
  onSaved: () => void;
}

function todayIso(): string {
  return new Date().toISOString().slice(0, 10);
}

export function PrecioFormPanel({ isOpen, precio, onClose, onSaved }: Props) {
  const [fecha, setFecha] = useState(todayIso());
  const [precioKg, setPrecioKg] = useState("");
  const [notas, setNotas] = useState("");
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [generalError, setGeneralError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!isOpen) return;
    setFieldErrors({});
    setGeneralError(null);
    if (precio) {
      setFecha(precio.fecha);
      setPrecioKg(precio.precio_kg);
      setNotas(precio.notas);
    } else {
      setFecha(todayIso());
      setPrecioKg("");
      setNotas("");
    }
  }, [isOpen, precio]);

  if (!isOpen) return null;

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setIsSubmitting(true);
    setFieldErrors({});
    setGeneralError(null);

    try {
      const data = { fecha, precio_kg: precioKg, notas };
      if (precio) {
        await actualizarPrecio(precio.id, data);
      } else {
        await crearPrecio(data);
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
          {precio ? "Editar precio" : "Nuevo precio"}
        </h2>

        <div className="mt-6 flex-1 space-y-4 overflow-y-auto">
          {generalError && (
            <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950 dark:text-red-400">
              {generalError}
            </p>
          )}

          <div>
            <label
              htmlFor="fecha"
              className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300"
            >
              Fecha
            </label>
            <input
              id="fecha"
              type="date"
              value={fecha}
              onChange={(e) => setFecha(e.target.value)}
              required
              className="w-full rounded-lg border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900 outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 dark:border-neutral-700 dark:bg-neutral-800 dark:text-neutral-100"
            />
            {fieldErrors.fecha && (
              <p className="mt-1 text-xs text-red-600 dark:text-red-400">
                {fieldErrors.fecha}
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="precio_kg"
              className="mb-1 block text-sm font-medium text-neutral-700 dark:text-neutral-300"
            >
              Precio por kg (MXN)
            </label>
            <input
              id="precio_kg"
              type="number"
              step="0.01"
              min="0"
              value={precioKg}
              onChange={(e) => setPrecioKg(e.target.value)}
              required
              className="w-full rounded-lg border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900 outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 dark:border-neutral-700 dark:bg-neutral-800 dark:text-neutral-100"
            />
            {fieldErrors.precio_kg && (
              <p className="mt-1 text-xs text-red-600 dark:text-red-400">
                {fieldErrors.precio_kg}
              </p>
            )}
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
