import { Link, Outlet, useNavigate } from "react-router-dom";

export default function PrivateLayout({ onLogout }: { onLogout: () => void }) {
  const nav = useNavigate();

  const handleLogout = () => {
    onLogout();
    nav("/");
  };

  return (
    <div className="min-h-screen grid grid-cols-1 md:grid-cols-[260px_1fr] bg-slate-950 text-slate-200">
      <aside className="border-r border-slate-800 bg-slate-900/40 p-4">
        <div className="mb-3">
          <div className="font-extrabold text-sky-400">Billing UI</div>
          <div className="text-xs text-slate-400">Área privada</div>
        </div>

        <div className="grid gap-2">
          <Link
            to="/app"
            className="rounded-md border border-slate-800 bg-slate-950 px-3 py-2 text-sm hover:border-sky-500"
          >
            Dashboard
          </Link>
          <Link
            to="/"
            className="rounded-md border border-slate-800 bg-slate-950 px-3 py-2 text-sm text-slate-400 hover:text-slate-200"
          >
            Ir al público
          </Link>
        </div>

        <button
          onClick={handleLogout}
          className="mt-4 w-full rounded-md border border-slate-800 bg-rose-950/40 px-3 py-2 text-sm font-bold text-rose-300 hover:bg-rose-950/60"
        >
          Salir
        </button>
      </aside>

      <div className="flex flex-col">
        <header className="border-b border-slate-800 bg-slate-950 px-6 py-4">
          <div className="font-bold">Panel</div>
          <div className="text-xs text-slate-400">Solo autenticados</div>
        </header>

        <main className="p-6 flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
