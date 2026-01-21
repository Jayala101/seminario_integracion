import { BrowserRouter, Route, Routes } from "react-router-dom";
import { useAuth } from "./application/auth/useAuth";

import PublicLayout from "./presentation/layouts/PublicLayout";
import RequireAuth from "./presentation/routing/RequireAuth";
import PrivateLayout from "./presentation/layouts/PrivateLayout";

import Home from "./presentation/pages/public/Home";
import Login from "./presentation/pages/public/Login";
import Register from "./presentation/pages/public/Register";
import Dashboard from "./presentation/pages/private/Dashboard";

export default function App() {
  const auth = useAuth();

  return (
    <BrowserRouter>
      <Routes>
        <Route element={<PublicLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login onLogin={auth.login} />} />
          <Route
            path="/register"
            element={
              <Register
                onRegister={(u: string, e: string, p: string) =>
                  auth.register({ username: u, email: e, password: p })
                }
              />
            }
          />
        </Route>

        <Route
          path="/app"
          element={
            <RequireAuth isAuthenticated={auth.isAuthenticated}>
              <PrivateLayout onLogout={auth.logout} />
            </RequireAuth>
          }
        >
          <Route index element={<Dashboard />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
