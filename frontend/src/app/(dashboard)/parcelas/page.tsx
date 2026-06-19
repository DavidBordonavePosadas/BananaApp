"use client";

import { useState } from "react";
import { ParcelaFormPanel } from "./ParcelaFormPanel";
import { ParcelasTable } from "./ParcelasTable";
import type { Parcela } from "@/types";

type FiltroActiva = boolean | undefined;

const FILTROS: { label: string; value: FiltroActiva }[] = [
  { label: "Todas", value: undefined },
  { label: "Activas", value: true },
  { label: "Inactivas", value: false },
];

export default function ParcelasPage() {
  const [filtroActiva, setFiltroActiva] = useState<FiltroActiva>(undefined);
  const [refreshToken, setRefreshToken] = useState(0);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingParcela, setEditingParcela] = useState<Parcela | null>(null);

  function handleNueva() {
    setEditingParcela(null);
    setIsFormOpen(true);
  }

  function handleEditar(parcela: Parcela) {
    setEditingParcela(parcela);
    setIsFormOpen(true);
  }

  function handleSaved() {
    setIsFormOpen(false);
    setRefreshToken((t) => t + 1);
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-neutral-900 dark:text-neutral-50">
            Parcelas
          </h1>
          <p className="mt-1 text-sm text-neutral-500 dark:text-neutral-400">
            Catálogo de parcelas de producción.
          </p>
        </div>
        <button
          type="button"
          onClick={handleNueva}
          className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-emerald-700"
        >
          Nueva parcela
        </button>
      </div>

      <div className="flex w-fit items-center gap-1 rounded-xl border border-neutral-200 bg-white p-1 dark:border-neutral-800 dark:bg-neutral-900">
        {FILTROS.map(({ label, value }) => (
          <button
            key={label}
            type="button"
            onClick={() => setFiltroActiva(value)}
            className={`rounded-lg px-4 py-1.5 text-sm font-medium transition-colors ${
              filtroActiva === value
                ? "bg-emerald-600 text-white"
                : "text-neutral-600 hover:bg-neutral-100 dark:text-neutral-300 dark:hover:bg-neutral-800"
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      <ParcelasTable
        filtroActiva={filtroActiva}
        refreshToken={refreshToken}
        onEdit={handleEditar}
        onMutated={() => setRefreshToken((t) => t + 1)}
      />

      <ParcelaFormPanel
        isOpen={isFormOpen}
        parcela={editingParcela}
        onClose={() => setIsFormOpen(false)}
        onSaved={handleSaved}
      />
    </div>
  );
}
