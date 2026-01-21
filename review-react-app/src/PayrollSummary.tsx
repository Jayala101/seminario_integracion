import React, { useCallback, useMemo, useState, } from "react";

type Props = {
    totalHours: number;
    extraHours: number;
    pay: number;
};

export function PayrollSummary({totalHours, extraHours, pay}: Props) {

    return (
        <section>
            <h2>Resumen</h2>
            <p>Total horas: {totalHours}</p>
            <p>Horas extra: {extraHours}</p>
            <p>Pago total: {pay.toFixed(2)}</p>
        </section>
    );
}