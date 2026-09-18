// =========================================================
// SHOP EASE - MAIN JAVASCRIPT
// =========================================================


// ---------------------------------------------------------
// CART QUANTITY
// ---------------------------------------------------------

function stepQty(btn, delta) {

    const form = btn.closest("form");

    if (!form) {
        return;
    }

    const input = form.querySelector(
        'input[name="quantity"]'
    );

    if (!input) {
        return;
    }

    const max = parseInt(
        input.max || "999",
        10
    );

    const current = parseInt(
        input.value || "1",
        10
    );

    const newValue = current + delta;

    input.value = Math.max(
        1,
        Math.min(
            max,
            newValue
        )
    );
}


// ---------------------------------------------------------
// AUTO REMOVE TOAST MESSAGES
// ---------------------------------------------------------

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const toasts = document.querySelectorAll(
            ".toast"
        );

        toasts.forEach(
            function (toast) {

                setTimeout(
                    function () {

                        toast.style.opacity = "0";

                        setTimeout(
                            function () {
                                toast.remove();
                            },
                            300
                        );

                    },
                    4200
                );

            }
        );

    }
);