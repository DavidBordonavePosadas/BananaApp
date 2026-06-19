"use client";

import { useEffect, type ReactNode } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth/AuthContext";

const NAV_ITEMS = [
  { href: "/", label: "Dashboard" },
  { href: "/precios", label: "Precios" },
  { href: "/parcelas", label: "Parcelas" },
  { href: "/cosechas", label: "Cosechas" },
  { href: "/ventas", label: "Ventas" },
  { href: "/trabajadores", label: "Trabajadores" },
  { href: "/insumos", label: "Insumos" },
  { href: "/notas", label: "Notas" },
];

export default function DashboardLayout({
  children,
}: {
  children: ReactNode;
}) {
  const { user, isLoading, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isLoading && !user) {
      router.replace("/login");
    }
  }, [isLoading, user, router]);

  if (isLoading || !user) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-neutral-50 dark:bg-neutral-950">
        <p className="text-sm text-neutral-500 dark:text-neutral-400">
          Cargando...
        </p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-neutral-50 dark:bg-neutral-950">
      <aside className="hidden w-60 flex-col border-r border-neutral-200 bg-white px-4 py-6 dark:border-neutral-800 dark:bg-neutral-900 sm:flex">
        <div className="mb-8 px-2 text-lg font-semibold text-neutral-900 dark:text-neutral-50">
          BananaApp
        </div>
        <nav className="flex flex-1 flex-col gap-1">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400"
                    : "text-neutral-600 hover:bg-neutral-100 dark:text-neutral-300 dark:hover:bg-neutral-800"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </aside>

      <div className="flex flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-neutral-200 bg-white px-6 py-4 dark:border-neutral-800 dark:bg-neutral-900">
          <span className="text-sm font-medium text-neutral-500 dark:text-neutral-400 sm:hidden">
            BananaApp
          </span>
          <div className="ml-auto flex items-center gap-4">
            <span className="text-sm text-neutral-700 dark:text-neutral-300">
              {user.username}
            </span>
            <button
              type="button"
              onClick={() => logout()}
              className="rounded-lg border border-neutral-300 px-3 py-1.5 text-sm font-medium text-neutral-700 transition-colors hover:bg-neutral-100 dark:border-neutral-700 dark:text-neutral-300 dark:hover:bg-neutral-800"
            >
              Cerrar sesión
            </button>
          </div>
        </header>

        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
