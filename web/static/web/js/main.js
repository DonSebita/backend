document.addEventListener("DOMContentLoaded", function () {

    const rows = document.querySelectorAll(".programmer-row");

    rows.forEach(row => {

        row.addEventListener("dblclick", function () {

            const displayValues =
                row.querySelectorAll(".display-value");

            const inputs =
                row.querySelectorAll(".edit-input");

            const saveButton =
                row.querySelector(".btn-save");


            displayValues.forEach(element => {
                element.style.display = "none";
            });


            inputs.forEach(input => {
                input.style.display = "block";
            });


            if (saveButton) {
                saveButton.style.display = "inline-block";
            }

        });

    });

});