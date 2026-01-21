import { Link, Outlet } from "react-router-dom";

export default function PublicLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-200">
      <header className="sticky top-0 z-10 border-b border-slate-800 bg-slate-950">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <div className="font-extrabold text-sky-400">Billing UI</div>
            <div className="text-xs text-slate-400">Área pública</div>
          </div>

          <nav className="flex gap-4 text-sm">
            <Link to="/" className="text-slate-200 hover:text-white">
              Inicio
            </Link>
            <Link to="/register" className="text-sky-400 hover:text-sky-300">
              Register
            </Link>
            <Link to="/login" className="text-sky-400 hover:text-sky-300">
              Login
            </Link>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <Outlet />
      </main>

      <footer className="border-t border-slate-800 text-slate-400">
        <div className="max-w-6xl mx-auto px-6 py-4 text-sm">
          Billing UI · React + Django REST · {new Date().getFullYear()}
        </div>
      </footer>
    </div>
  );
}
