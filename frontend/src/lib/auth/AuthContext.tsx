"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import {
  api,
  getRefreshToken,
  refreshAccessToken,
  setAccessToken,
  setRefreshToken,
} from "@/lib/api/client";
import type { TokenPair, Usuario } from "@/types";

interface AuthContextValue {
  user: Usuario | null;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<Usuario | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    (async () => {
      const refresh = getRefreshToken();
      if (!refresh) {
        setIsLoading(false);
        return;
      }
      const newAccess = await refreshAccessToken();
      if (!newAccess) {
        setIsLoading(false);
        return;
      }
      try {
        const me = await api.get<Usuario>("/api/auth/me/");
        setUser(me);
      } catch {
        setAccessToken(null);
        setRefreshToken(null);
      } finally {
        setIsLoading(false);
      }
    })();
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    const tokens = await api.post<TokenPair>("/api/token/", {
      username,
      password,
    });
    setAccessToken(tokens.access);
    setRefreshToken(tokens.refresh);
    const me = await api.get<Usuario>("/api/auth/me/");
    setUser(me);
  }, []);

  const logout = useCallback(async () => {
    const refresh = getRefreshToken();
    try {
      if (refresh) {
        await api.post("/api/auth/logout/", { refresh });
      }
    } catch {
      // El token ya puede estar vencido o invalidado; continuamos limpiando sesión local.
    } finally {
      setAccessToken(null);
      setRefreshToken(null);
      setUser(null);
      router.push("/login");
    }
  }, [router]);

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth debe usarse dentro de un AuthProvider");
  }
  return ctx;
}
