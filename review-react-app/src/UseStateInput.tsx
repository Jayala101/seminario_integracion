import { useState } from "react";

export function UseStateInput() {
  const [texto, setTexto] = useState("");

  return (
    <>
      <input
        value={texto}
        placeholder="Escribe un texto"
        onChange={(e) => setTexto(e.target.value)}
      />
      <p>{texto || "..."}</p>
    </>
  );
}
