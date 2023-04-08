import { useState, useEffect } from "react";

import React from 'react'

export default function StickyComponent(props: any) {


    const [isSticky, setIsSticky] = useState(false);
    const [topOffset, setTopOffset] = useState<number | null>(0);

    useEffect(() => {
        function handleScroll() {
            const top = window.pageYOffset || document.documentElement.scrollTop;
            if (topOffset) {

                setIsSticky(top >= topOffset);
            }

        }

        const paginationElement = document.getElementById("pagination");
        if (paginationElement) {
            setTopOffset(paginationElement.offsetTop);
        }
        window.addEventListener("scroll", handleScroll);
        return () => {
            window.removeEventListener("scroll", handleScroll);
        };
    }, [topOffset]);

    return (
        <div>
            <div id="pagination" className={(isSticky ? 'sticky' : "")}>
                {props.children[0]}
            </div>
            <div>
                {props.children[1]}
            </div>
        </div >
    )
}
