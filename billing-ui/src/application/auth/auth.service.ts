import { publicHttp } from "../../infrastructure/http/httpClients";
import type {
  AuthTokens,
  LoginPayload,
  RegisterPayload,
} from "../../domain/auth/auth.types";

export const authService = {
  async login(payload: LoginPayload): Promise<AuthTokens> {
    const res = await publicHttp.post<AuthTokens>("/auth/login/", payload);
    return res.data;
  },

  async register(payload: RegisterPayload): Promise<void> {
    await publicHttp.post("/auth/register/", payload);
  },
};
