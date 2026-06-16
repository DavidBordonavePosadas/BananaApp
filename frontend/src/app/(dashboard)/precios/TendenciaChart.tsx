"use client";

import { useEffect, useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { parseApiError } from "@/lib/api/client";
import { obtenerTendenciaMensual } from "@/lib/api/precios";
import { formatCurrency, MESES_ABREV } from "@/lib/format";
import type { TendenciaMensualItem } from "@/types";

interface ChartPoint {
  mes: string;
  promedio: number | null;
}

function currentYear(): number {
  return new Date().getFullYear();
}

export function TendenciaChart() {
  const [anio, setAnio] = useState(currentYear());
  const [data, setData] = useState<TendenciaMensualItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setIsLoading(true);
    setError(null);

    obtenerTendenciaMensual(anio)
      .then((result) => {
        if (!active) return;
        setData(result);
      })
      .catch((err) => {
        if (!active) return;
        const parsed = parseApiError(err);
        setError(
          typeof parsed.detail === "string"
            ? parsed.detail
            : "No se pudo cargar la tendencia."
        );
      })
      .finally(() => {
        if (active) setIsLoading(false);
      });

    return () => {
      active = false;
    };
  }, [anio]);

  const chartData: ChartPoint[] = data.map((item) => ({
    mes: MESES_ABREV[item.mes - 1],
    promedio: item.promedio !== null ? parseFloat(item.promedio) : null,
  }));

  const hasData = chartData.some((point) => point.promedio !== null);
  const years = Array.from({ length: 6 }, (_, i) => currentYear() - i);

  return (
    <div className="rounded-2xl border border-neutral-200 bg-white p-5 dark:border-neutral-800 dark:bg-neutral-900">
      <div className="flex items-center justify-between">
        <h2 className="text-base font-semibold text-neutral-900 dark:text-neutral-50">
          Tendencia mensual
        </h2>
        <select
          value={anio}
          onChange={(e) => setAnio(Number(e.target.value))}
          className="rounded-lg border border-neutral-300 bg-white px-3 py-1.5 text-sm text-neutral-700 outline-none focus:border-emerald-500 dark:border-neutral-700 dark:bg-neutral-800 dark:text-neutral-300"
        >
          {years.map((y) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>
      </div>

      <div className="mt-4 h-72">
        {isLoading ? (
          <div className="flex h-full items-center justify-center text-sm text-neutral-400 dark:text-neutral-500">
            Cargando...
          </div>
        ) : error ? (
          <div className="flex h-full items-center justify-center text-sm text-red-600 dark:text-red-400">
            {error}
          </div>
        ) : !hasData ? (
          <div className="flex h-full items-center justify-center text-sm text-neutral-400 dark:text-neutral-500">
            Sin datos para {anio}.
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{ top: 8, right: 16, bottom: 0, left: 0 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="mes" tick={{ fontSize: 12, fill: "#6b7280" }} />
              <YAxis
                tick={{ fontSize: 12, fill: "#6b7280" }}
                domain={["auto", "auto"]}
              />
              <Tooltip
                formatter={(value) => formatCurrency(value as number)}
                contentStyle={{ borderRadius: 8, fontSize: 12 }}
              />
              <Line
                type="monotone"
                dataKey="promedio"
                stroke="#059669"
                strokeWidth={2}
                connectNulls={false}
                dot={{ r: 3 }}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
