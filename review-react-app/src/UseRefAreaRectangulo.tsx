import { useRef } from "react";
import { useState } from "react";

export function UseRefAreaRectangulo() {

    const baseRef = useRef<HTMLInputElement | null>(null);
    const heightRef = useRef<HTMLInputElement | null>(null);
    const[area,setArea] = useState(0);
    const calculateArea=()=>{
        const base = Number(baseRef.current?.value || 0);
        const height = Number(heightRef.current?.value || 0);
        setArea(base*height)
    }

    return(
        <>
            <input
                ref = {baseRef}
                type = "number"
                placeholder="Base"
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