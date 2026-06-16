"use client";

import { useEffect, useState } from "react";
import { parseApiError } from "@/lib/api/client";
import { compararPeriodos } from "@/lib/api/precios";
import { formatCurrency } from "@/lib/format";
import type { ComparacionPeriodos, EstadisticasPrecios } from "@/types";

function todayIso(): string {
  return new Date().toISOString().slice(0, 10);
}

function isoOffset(daysAgo: number): string {
  const d = new Date();
  d.setDate(d.getDate() - daysAgo);
  return d.toISOString().slice(0, 10);
}

function PeriodoInputs({
  titulo,
  inicio,
  fin,
  onInicio,
  onFin,
}: {
  titulo: string;
  inicio: string;
  fin: string;
  onInicio: (value: string) => void;
  onFin: (value: string) => void;
}) {
  return (
    <div className="rounded-xl border border-neutral-200 p-4 dark:border-neutral-800">
      <p className="text-sm font-medium text-neutral-700 dark:text-neutral-300">
        {titulo}
      </p>
      <div className="mt-2 flex gap-2">
        <input
          type="date"
          value={inicio}
          onChange={(e) => onInicio(e.target.value)}
          className="w-full rounded-lg border border-neutral-300 bg-white px-2 py-1.5 text-sm text-neutral-900 outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 dark:border-neutral-700 dark:bg-neutral-800 dark:text-neutral-100"
        />
        <input
          type="date"
          value={fin}
          onChange={(e) => onFin(e.target.value)}
          className="w-full rounded-lg border border-neutral-300 bg-white px-2 py-1.5 text-sm text-neutral-900 outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 dark:border-neutral-700 dark:bg-neutral-800 dark:text-neutral-100"
        />
      </div>
    </div>
  );
}

function PeriodoStatsCard({
  titulo,
  stats,
}: {
  titulo: string;
  stats: EstadisticasPrecios;
}) {
  return (
    <div className="rounded-xl border border-neutral-200 p-4 dark:border-neutral-800">
      <p className="text-sm font-medium text-neutral-700 dark:text-neutral-300">
        {titulo}
      </p>
      {stats.total === 0 ? (
        <p className="mt-2 text-sm text-neutral-400 dark:text-neutral-500">
          Sin datos en este periodo.
        </p>
      ) : (
        <dl className="mt-2 space-y-1 text-sm">
          <div className="flex justify-between">
            <dt className="text-neutral-500 dark:text-neutral-400">Promedio</dt>
            <dd className="font-medium text-neutral-900 dark:text-neutral-50">
              {formatCurrency(stats.promedio)}
            </dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-neutral-500 dark:text-neutral-400">Máximo</dt>
            <dd className="font-medium text-neutral-900 dark:text-neutral-50">
              {stats.maximo ? formatCurrency(stats.maximo.precio_kg) : "—"}
            </dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-neutral-500 dark:text-neutral-400">Mínimo</dt>
            <dd className="font-medium text-neutral-900 dark:text-neutral-50">
              {stats.minimo ? formatCurrency(stats.minimo.precio_kg) : "—"}
            </dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-neutral-500 dark:text-neutral-400">Registros</dt>
            <dd className="font-medium text-neutral-900 dark:text-neutral-50">
              {stats.total}
            </dd>
          </div>
        </dl>
      )}
    </div>
  );
}

export function ComparadorPeriodos() {
  const [p1Inicio, setP1Inicio] = useState(isoOffset(29));
  const [p1Fin, setP1Fin] = useState(todayIso());
  const [p2Inicio, setP2Inicio] = useState(isoOffset(59));
  const [p2Fin, setP2Fin] = useState(isoOffset(30));

  const [resultado, setResultado] = useState<ComparacionPeriodos | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleComparar() {
    setIsLoading(true);
    setError(null);
    try {
      const data = await compararPeriodos({ p1Inicio, p1Fin, p2Inicio, p2Fin });
      setResultado(data);
    } catch (err) {
      const parsed = parseApiError(err);
      setError(
        typeof parsed.detail === "string"
          ? parsed.detail
          : "No se pudo comparar los periodos."
      );
      setResultado(null);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    handleComparar();
    // Solo se ejecuta una vez al montar; comparaciones posteriores las dispara el botón.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const diferencia =
    resultado?.diferencia_porcentual != null
      ? parseFloat(resultado.diferencia_porcentual)
      : null;

  return (
    <div className="rounded-2xl border border-neutral-200 bg-white p-5 dark:border-neutral-800 dark:bg-neutral-900">
      <h2 className="text-base font-semibold text-neutral-900 dark:text-neutral-50">
        Comparar periodos
      </h2>

      <div className="mt-4 grid gap-4 sm:grid-cols-2">
        <PeriodoInputs
          titulo="Periodo 1"
          inicio={p1Inicio}
          fin={p1Fin}
          onInicio={setP1Inicio}
          onFin={setP1Fin}
        />
        <PeriodoInputs
          titulo="Periodo 2"
          inicio={p2Inicio}
          fin={p2Fin}
          onInicio={setP2Inicio}
          onFin={setP2Fin}
        />
      </div>

      <div className="mt-4 flex justify-end">
        <button
          type="button"
          onClick={handleComparar}
          disabled={isLoading}
          className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isLoading ? "Comparando..." : "Comparar"}
        </button>
      </div>

      {error && (
        <p className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950 dark:text-red-400">
          {error}
        </p>
      )}

      {resultado && !error && (
        <>
          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            <PeriodoStatsCard titulo="Periodo 1" stats={resultado.periodo_1} />
            <PeriodoStatsCard titulo="Periodo 2" stats={resultado.periodo_2} />
          </div>

          <div className="mt-4 rounded-xl bg-neutral-50 p-4 text-center dark:bg-neutral-950">
            <p className="text-sm text-neutral-500 dark:text-neutral-400">
              Diferencia entre promedios (Periodo 1 vs Periodo 2)
            </p>
            {diferencia === null ? (
              <p className="mt-1 text-lg font-semibold text-neutral-400 dark:text-neutral-500">
                No disponible
              </p>
            ) : (
              <p
                className={`mt-1 text-2xl font-semibold ${
                  diferencia >= 0
                    ? "text-emerald-600 dark:text-emerald-400"
                    : "text-red-600 dark:text-red-400"
                }`}
              >
                {diferencia >= 0 ? "+" : ""}
                {diferencia.toFixed(2)}%
              </p>
            )}
          </div>
        </>
      )}
    </div>
  );
}
