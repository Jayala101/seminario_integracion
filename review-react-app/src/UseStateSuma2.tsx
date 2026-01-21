// se inicia con numeros y se convierte en el input a number
import { useState } from "react";

export function UseStateSuma2() {
  const [numero1, setNumero1] = useState(0);
  const [numero2, setNumero2] = useState(0);

  const suma = numero1 + numero2;
  return (
    <>
    <p>Suma 2</p>
      <input
        value={numero1}
        placeholder="Escribe un número"
        onChange={(e) => setNumero1(Number(e.target.value))}
      />
      <input
        value={numero2}
        placeholder="Escribe otro número"
        onChange={(e) => setNumero2(Number(e.target.value))}
      />
      <p>La suma es: {suma || "0"}</p>
    </>
  );
}
