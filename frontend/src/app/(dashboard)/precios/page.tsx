"use client";

import { useState } from "react";
import { ComparadorPeriodos } from "./ComparadorPeriodos";
import { PrecioFormPanel } from "./PrecioFormPanel";
import { PreciosTable } from "./PreciosTable";
import { StatsCards } from "./StatsCards";
import { TendenciaChart } from "./TendenciaChart";
import type { HistorialPrecio } from "@/types";

function todayIso(): string {
  return new Date().toISOString().slice(0, 10);
}

function isoOffset(daysAgo: number): string {
  const d = new Date();
  d.setDate(d.getDate() - daysAgo);
  return d.toISOString().slice(0, 10);
}

export default function PreciosPage() {
  const [draftInicio, setDraftInicio] = useState(isoOffset(89));
  const [draftFin, setDraftFin] = useState(todayIso());
  const [fechaInicio, setFechaInicio] = useState(draftInicio);
  const [fechaFin, setFechaFin] = useState(draftFin);

  const [refreshToken, setRefreshToken] = useState(0);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingPrecio, setEditingPrecio] = useState<HistorialPrecio | null>(
    null
  );

  function handleAplicarFiltro() {
    setFechaInicio(draftInicio);
    setFechaFin(draftFin);
  }

  function handleNuevo() {
    setEditingPrecio(null);
    setIsFormOpen(true);
  }

  function handleEditar(precio: HistorialPrecio) {
    setEditingPrecio(precio);
    setIsFormOpen(true);
  }

  function handleMutated() {
    setRefreshToken((token) => token + 1);
  }

  function handleSaved() {
    setIsFormOpen(false);
    handleMutated();
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-neutral-900 dark:text-neutral-50">
            Precios
          </h1>
          <p className="mt-1 text-sm text-neutral-500 dark:text-neutral-400">
            Historial de precios por kilogramo de plátano.
          </p>
        </div>
        <button
          type="button"
          onClick={handleNuevo}
          className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-emerald-700"
        >
          Nuevo precio
        </button>
      </div>

      <div className="flex flex-wrap items-end gap-3 rounded-2xl border border-neutral-200 bg-white p-4 dark:border-neutral-800 dark:bg-neutral-900">
        <div>
          <label
            htmlFor="filtro_inicio"
            className="mb-1 block text-xs font-medium text-neutral-500 dark:text-neutral-400"
          >
            Desde
          </label>
          <input
            id="filtro_inicio"
            type="date"
            value={draftInicio}
            onChange={(e) => setDraftInicio(e.target.value)}
            className="rounded-lg border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900 outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 dark:border-neutral-700 dark:bg-neutral-800 dark:text-neutral-100"
          />
        </div>
        <div>
          <label
            htmlFor="filtro_fin"
            className="mb-1 block text-xs font-medium text-neutral-500 dark:text-neutral-400"
          >
            Hasta
          </label>
          <input
            id="filtro_fin"
            type="date"
            value={draftFin}
            onChange={(e) => setDraftFin(e.target.value)}
            className="rounded-lg border border-neutral-300 bg-white px-3 py-2 text-sm text-neutral-900 outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 dark:border-neutral-700 dark:bg-neutral-800 dark:text-neutral-100"
          />
        </div>
        <button
          type="button"
          onClick={handleAplicarFiltro}
          className="rounded-lg border border-neutral-300 px-4 py-2 text-sm font-medium text-neutral-700 transition-colors hover:bg-neutral-100 dark:border-neutral-700 dark:text-neutral-300 dark:hover:bg-neutral-800"
        >
          Aplicar
        </button>
      </div>

      <StatsCards
        fechaInicio={fechaInicio}
        fechaFin={fechaFin}
        refreshToken={refreshToken}
      />

      <PreciosTable
        fechaInicio={fechaInicio}
        fechaFin={fechaFin}
        refreshToken={refreshToken}
        onEdit={handleEditar}
        onMutated={handleMutated}
      />

      <TendenciaChart />

      <ComparadorPeriodos />

      <PrecioFormPanel
        isOpen={isFormOpen}
        precio={editingPrecio}
        onClose={() => setIsFormOpen(false)}
        onSaved={handleSaved}
      />
    </div>
  );
}
