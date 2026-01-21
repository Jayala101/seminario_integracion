import React, { useCallback, useMemo, useState, } from "react";

type Props = {
    hours: number[];
    setHours: React.Dispatch<React.SetStateAction<number[]>>;
};

export function WorkDays({hours, setHours}: Props) {
    const days = ['lun','mar','mié','jue','vie'];

    const changeHour =(i:number,value:string)=>{
        const hour = Number(value) || 0;
        setHours((prev)=>
            prev.map((v,idx)=>(idx===i? hour : v))
        );
    };

    return (
        <section>
            {days.map((day, i) => (
                <div key={day}>
                    <label>{day.toUpperCase()}:</label>
                    <input
                        type="number"
                        value={hours[i]}
                        onChange={(e) => changeHour(i, e.target.value)}
                    />
                </div>
            ))}
        </section>
    );
}