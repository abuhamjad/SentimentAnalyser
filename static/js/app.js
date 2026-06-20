const textarea = document.getElementById("textInput");
const wordCount = document.getElementById("wordCount");

const analyseBtn = document.getElementById("analyseBtn");
const clearBtn = document.getElementById("clearBtn");

textarea.addEventListener("input", () => {

    const text = textarea.value;

    const words =
        text.trim() === ""
        ? 0
        : text.trim().split(/\s+/).length;

    wordCount.textContent =
        `${words} words`;

    if(text.trim() !== ""){

        analyseBtn.disabled = false;
        analyseBtn.classList.add("active");

        clearBtn.classList.remove("hidden");

    }else{

        analyseBtn.disabled = true;
        analyseBtn.classList.remove("active");

        clearBtn.classList.add("hidden");
    }
});

clearBtn.addEventListener("click", () => {

    textarea.value = "";

    wordCount.textContent = "0 words";

    analyseBtn.disabled = true;
    analyseBtn.classList.remove("active");

    clearBtn.classList.add("hidden");

    textarea.focus();

});

document
.querySelectorAll(".example-btn")
.forEach(button => {

    button.addEventListener("click", () => {

        textarea.value =
            button.dataset.text;

        textarea.dispatchEvent(
            new Event("input")
        );

    });

});