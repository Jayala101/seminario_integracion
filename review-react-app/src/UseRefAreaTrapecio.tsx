import { useRef } from "react";
import { useState } from "react";

export function UseRefAreaTrapecio() {

    const baseRef = useRef<HTMLInputElement | null>(null);
    const basemayorRef = useRef<HTMLInputElement | null>(null);
    const heightRef = useRef<HTMLInputElement | null>(null);
    const[area,setArea] = useState(0);
    const calculateArea=()=>{
        const base = Number(baseRef.current?.value || 0);
        const basemayor = Number(baseRef.current?.value || 0);
        const height = Number(heightRef.current?.value || 0);
        setArea(((base+basemayor)*height)/2)
    }

    return(
        <>
            <input
                ref = {baseRef}
                type = "number"
                placeholder="Base menor"
            />
            <input
                ref = {basemayorRef}
                type = "number"
                placeholder="Base mayor"
            />
            <input
                ref = {heightRef}
                type = "number"
                placeholder="Altura"
            />
            <button onClick={calculateArea}> Calcular area</button>
            <p>Area: {area}</p>
        </>
    )

}