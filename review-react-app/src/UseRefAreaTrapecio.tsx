import { useRef } from "react";
import { useState } from "react";

export function UseRefAreaTrapecio() {
    const baseMayorRef = useRef<HTMLInputElement | null>(null);
    const baseMenorRef = useRef<HTMLInputElement | null>(null);
    const alturaRef = useRef<HTMLInputElement | null>(null);

    const [area, setArea] = useState(0);

    const calcular=()=>{
        const baseMayor = Number(baseMayorRef.current?.value || 0);
        const baseMenor = Number(baseMenorRef.current?.value || 0);
        const altura = Number(alturaRef.current?.value|| 0);
        setArea(((baseMayor + baseMenor) / 2) * altura);
    }

    return (
    <>
      <input
        ref={baseMayorRef}
        type="number"
        placeholder="Base mayor"
      />
      <input
        ref={baseMenorRef}
        type="number"
        placeholder="Base menor"
      />
      <input
        ref={alturaRef}
        type="number"
        placeholder="Altura"
      />
      <button onClick={calcular}>Calcular área</button>
      <p>Area: {area}</p>
    </>
    );
}