import { useCallback, useMemo, useState, } from "react";

export function UseCallBackResta() {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);

  const total = useCallback(()=>
  {
    console.log("Recalculando total");
    return a-b;
  }, [a, b]);
  return (
    <>
      <input
        value={a}
        placeholder="numero 1"
        onChange={(e) => setA(Number(e.target.value))}
      />
      <input
        value={b}
        placeholder="numero 2"
        onChange={(e) => setB(Number(e.target.value))}
      />
      <p>La suma total es: {total() || '0'}</p>
    </>
  );
}
