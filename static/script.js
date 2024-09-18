document.getElementById("upload-form").onsubmit = async function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });
    const result = await response.json();

    if (result.error) {
        alert(result.error);
    } else {
        alert(result.message);
        document.getElementById("slider-container").style.display = "block";
        const img = new Image();
        img.src = URL.createObjectURL(event.target[0].files[0]); // Correctly reference the file input
        img.onload = function() {
            document.getElementById("x-slider").max = img.width; // Update max for X
            document.getElementById("y-slider").max = img.height; // Update max for Y
        };
    }
};

document.getElementById("x-slider").oninput = function() {
    document.getElementById("x-coordinate").textContent = `X: ${this.value}`;
};

document.getElementById("y-slider").oninput = function() {
    document.getElementById("y-coordinate").textContent = `Y: ${this.value}`;
};

document.getElementById("generate-button").onclick = async function() {
    const startingPointX = document.getElementById("x-slider").value;
    const startingPointY = document.getElementById("y-slider").value;

    const response = await fetch("/generate", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            starting_point_x: startingPointX,
            starting_point_y: startingPointY
        })
    });
    const result = await response.json();

    const plotImage = document.getElementById("plot");
    const errorMessage = document.getElementById("error");

    if (result.error) {
        errorMessage.textContent = result.error;
        plotImage.style.display = "none";
    } else {
        plotImage.src = `data:image/png;base64,${result.plot_url}`;
        plotImage.style.display = "block";
        errorMessage.textContent = "";
    }
};
