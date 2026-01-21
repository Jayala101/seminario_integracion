import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Register({
  onRegister,
}: {
  onRegister: (u: string, e: string, p: string) => Promise<void>;
}) {
  const nav = useNavigate();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    setLoading(true);
    try {
      await onRegister(username, email, password);
      nav("/app", { replace: true });
    } catch (e: any) {
      const data = e?.response?.data;
      if (data?.detail) setErr(data.detail);
      else if (data) setErr(JSON.stringify(data));
      else setErr("No se pudo registrar");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-120px)] flex items-center justify-center px-6">
      <div className="w-full max-w-md rounded-xl border border-slate-800 bg-slate-900/40 p-5">
        <h2 className="text-xl font-extrabold text-sky-400">Register</h2>

        {err && (
          <div className="mt-3 rounded-md border border-rose-900/60 bg-rose-950/40 px-3 py-2 text-rose-200 text-sm">
            {err}
          </div>
        )}

        <form onSubmit={onSubmit} className="mt-4 grid gap-3">
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="username"
            className="w-full rounded-md border border-slate-800 bg-slate-950 px-3 py-2 text-slate-200 outline-none focus:border-sky-500"
          />

          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="email"
            className="w-full rounded-md border border-slate-800 bg-slate-950 px-3 py-2 text-slate-200 outline-none focus:border-sky-500"
          />

          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="password"
            type="password"
            className="w-full rounded-md border border-slate-800 bg-slate-950 px-3 py-2 text-slate-200 outline-none focus:border-sky-500"
          />

          <button
            disabled={loading}
            className="w-full rounded-md border border-slate-800 bg-sky-950/40 px-3 py-2 font-extrabold text-sky-300 hover:bg-sky-950/60 disabled:opacity-60"
          >
            {loading ? "Registrando..." : "Crear cuenta"}
          </button>
        </form>

        <div className="mt-4 text-xs text-slate-400">
          ¿Ya tienes cuenta?{" "}
          <Link to="/login" className="text-sky-400 hover:text-sky-300">
            Login
          </Link>
        </div>
      </div>
    </div>
  );
}
