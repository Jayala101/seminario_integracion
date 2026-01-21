import { useState } from "react";

export function UseStateSuma() {
    const [numero1, setNumero1] = useState(0);
    const [numero2, setNumero2] = useState(0);

    const sum = Number(numero1)+Number(numero2);
    return <>
        <input
            value={numero1}
            placeholder="Escriba numero 1"
            onChange={(e)=>setNumero1(Number(e.target.value))}
        />
        <input
            value={numero2}
            placeholder="Escriba numero 2"
            onChange={(e)=>setNumero2(Number(e.target.value))}
        />
        <p>La suma es : {sum || '0'}</p>
    </>
}