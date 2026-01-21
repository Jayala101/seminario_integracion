import { useMemo, useState } from "react";

export function UseMemoTotal() {
  const [price, setprice] = useState(0);
  const [Qty, setQty] = useState(0);

  const total = useMemo(()=>
  {
    console.log("Recalculando total");
    return price*Qty;
  }, [price, Qty]);
  return (
    <>
      <input
        value={price}
        placeholder="precio"
        onChange={(e) => setprice(Number(e.target.value))}
      />
      <input
        value={Qty}
        placeholder="cantidad"
        onChange={(e) => setQty(Number(e.target.value))}
      />
      <p>La suma total es: {total || "0"}</p>
    </>
  );
}
