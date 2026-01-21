import { useMemo, useState } from "react";
import { authService } from "./auth.service";
import { tokenStorage } from "../../infrastructure/storage/tokenStorage";
import type { RegisterPayload } from "../../domain/auth/auth.types";

export function useAuth() {
  const [access, setAccess] = useState<string | null>(tokenStorage.getAccess());

  const isAuthenticated = useMemo(() => !!access, [access]);

  const login = async (username: string, password: string) => {
    const tokens = await authService.login({ username, password });
    tokenStorage.set(tokens.access, tokens.refresh);
    setAccess(tokens.access);
  };

  const register = async (payload: RegisterPayload) => {
    await authService.register(payload);
    await login(payload.username, payload.password);
  };

  const logout = () => {
    tokenStorage.clear();
    setAccess(null);
  };

  return { isAuthenticated, access, login, register, logout };
}
