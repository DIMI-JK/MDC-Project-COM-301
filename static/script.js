// // debugging
// console.count("Revora script initialized");

// window.addEventListener("beforeunload", () => {
//     console.trace("Page is navigating or reloading");
// }); 
// //

// let storedProductUrl = "";

// const inputField = document.getElementById("productUrl");
// const analyzeBtn = document.getElementById("analyzeBtn");
// const resultsSection = document.getElementById("resultsSection");
// const resultStatus = document.getElementById("resultStatus");

// function isValidUrl(string) {
//     try {
//         const url = new URL(string);

//         return (
//             (url.protocol === "http:" || url.protocol === "https:") &&
//             url.hostname.length > 0
//         );
//     } catch (_) {
//         return false;
//     }
// }

// async function handleAnalysis() {
//     console.count("Analyze handler called"); //debugging 

//     if (isAnalyzing) {
//         console.warn("Analysis already in progress. Ignoring duplicate.");
//         return;
//     }

//     // Keep the rest of your existing function below.

//     const urlValue = inputField.value.trim();

//     if (!urlValue) {
//         alert("Please paste a product link first.");
//         return;
//     }

//     if (!isValidUrl(urlValue)) {
//         alert("Please enter a valid product URL.");
//         return;
//     }
    

//     // This interface currently supports Flipkart URLs.
//     const parsedUrl = new URL(urlValue);

//     if (
//         !parsedUrl.hostname.toLowerCase().endsWith("flipkart.com")
//     ) {
//         alert("Please enter a valid Flipkart product URL.");
//         return;
//     }

//     storedProductUrl = urlValue;

//     const originalBtnText = analyzeBtn.innerHTML;

//     analyzeBtn.disabled = true;
//     analyzeBtn.innerHTML = "<span>⏳</span><span>Analyzing...</span>";

//     resultStatus.textContent = "Scraping and analyzing reviews...";
//     resultsSection.hidden = true;

//     try {
//         // Flask scrapes reviews and runs the existing model.
//         const response = await fetch(
//             "http://127.0.0.1:5000/analyze",
//             {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json"
//                 },
//                 body: JSON.stringify({
//                     url: storedProductUrl
//                 })
//             }
//         );

//         const data = await response.json();

//         if (!response.ok || data.status !== "success") {
//             throw new Error(
//                 data.error || "Failed to analyze reviews."
//             );
//         }

//         const summary = data.summary || {};

//         const total = Number(data.total_reviews) || 0;
//         const evaluated = Number(summary.evaluated) || 0;
//         const genuine = Number(summary.genuine) || 0;
//         const fake = Number(summary.fake) || 0;
//         const skipped = Number(summary.skipped) || 0;

//         // Populate result cards.
//         document.getElementById("totalReviews").textContent = total;
//         document.getElementById("evaluatedReviews").textContent =
//             evaluated;
//         document.getElementById("genuineReviews").textContent = genuine;
//         document.getElementById("fakeReviews").textContent = fake;
//         document.getElementById("skippedReviews").textContent = skipped;

//         // Percentages are based on evaluated reviews.
//         const genuinePct = evaluated
//             ? (genuine / evaluated * 100)
//             : 0;

//         const fakePct = evaluated
//             ? (fake / evaluated * 100)
//             : 0;

//         document.getElementById("genuinePercentage").textContent =
//             genuinePct.toFixed(1) + "%";

//         document.getElementById("fakePercentage").textContent =
//             fakePct.toFixed(1) + "%";

//         // Draw actual prediction distribution.
//         drawPieChart(genuine, fake);

//         resultsSection.hidden = false;
//         resultStatus.textContent =
//             "Analysis complete. " + evaluated + " reviews evaluated.";

//         // Scroll to the result cards.
//         resultsSection.scrollIntoView({
//             behavior: "smooth",
//             block: "start"
//         });

//         console.log("Revora analysis:", data);

//     } catch (error) {
//         console.error("Analysis error:", error);
//         resultStatus.textContent = error.message;
//         alert(
//             error.message.includes("fetch")
//                 ? "Cannot connect to Flask. Make sure app.py is running on port 5000."
//                 : error.message
//         );
//     } finally {
//         analyzeBtn.disabled = false;
//         analyzeBtn.innerHTML = originalBtnText;
//     }
// }

// function drawPieChart(genuine, fake) {
//     const canvas = document.getElementById("reviewPieChart");
//     const ctx = canvas.getContext("2d");

//     const centerX = canvas.width / 2;
//     const centerY = canvas.height / 2;
//     const radius = 105;
//     const total = genuine + fake;

//     ctx.clearRect(0, 0, canvas.width, canvas.height);

//     if (total === 0) {
//         ctx.beginPath();
//         ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
//         ctx.fillStyle = "#E2E8F0";
//         ctx.fill();

//         ctx.fillStyle = "#64748B";
//         ctx.font = "16px Arial";
//         ctx.textAlign = "center";
//         ctx.textBaseline = "middle";
//         ctx.fillText("No evaluated reviews", centerX, centerY);

//         return;
//     }

//     const slices = [
//         { value: genuine, color: "#15976A" },
//         { value: fake, color: "#E24B61" }
//     ];

//     let startAngle = -Math.PI / 2;

//     slices.forEach(slice => {
//         if (slice.value === 0) return;

//         const endAngle =
//             startAngle + (slice.value / total) * Math.PI * 2;

//         ctx.beginPath();
//         ctx.moveTo(centerX, centerY);
//         ctx.arc(
//             centerX,
//             centerY,
//             radius,
//             startAngle,
//             endAngle
//         );
//         ctx.closePath();

//         ctx.fillStyle = slice.color;
//         ctx.fill();

//         // Thin white separator between the slices.
//         ctx.strokeStyle = "#FFFFFF";
//         ctx.lineWidth = 3;
//         ctx.stroke();

//         startAngle = endAngle;
//     });

//     // White center creates a clean doughnut-style chart.
//     ctx.beginPath();
//     ctx.arc(centerX, centerY, 55, 0, Math.PI * 2);
//     ctx.fillStyle = "#FFFFFF";
//     ctx.fill();

//     ctx.fillStyle = "#0F172A";
//     ctx.font = "bold 25px Arial";
//     ctx.textAlign = "center";
//     ctx.textBaseline = "middle";
//     ctx.fillText(String(total), centerX, centerY - 5);

//     ctx.fillStyle = "#64748B";
//     ctx.font = "12px Arial";
//     ctx.fillText("Evaluated", centerX, centerY + 17);
// }

// analyzeBtn.addEventListener("click", (event) => {
//     event.preventDefault();
//     handleAnalysis();
// });

console.count("Revora script initialized");
console.log("Page URL:", window.location.href);

// Diagnostic: identify unexpected page reloads or navigation.
window.addEventListener("beforeunload", () => {
    console.trace("Revora page is navigating or reloading");
});

let storedProductUrl = "";
let isAnalyzing = false;

const inputField = document.getElementById("productUrl");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultsSection = document.getElementById("resultsSection");
const resultStatus = document.getElementById("resultStatus");

// Validate URL syntax and protocol.
function isValidUrl(string) {
    try {
        const url = new URL(string);

        return (
            (url.protocol === "http:" || url.protocol === "https:") &&
            url.hostname.length > 0
        );
    } catch {
        return false;
    }
}

// Only allow actual Flipkart hostnames.
function isFlipkartUrl(string) {
    try {
        const url = new URL(string);
        const hostname = url.hostname.toLowerCase();

        return (
            (url.protocol === "http:" || url.protocol === "https:") &&
            (hostname === "flipkart.com" ||
                hostname.endsWith(".flipkart.com"))
        );
    } catch {
        return false;
    }
}

async function handleAnalysis(event) {
    // Prevent form submission and duplicate requests.
    if (event) {
        event.preventDefault();
    }

    if (isAnalyzing) {
        console.warn("Analysis already running. Duplicate request ignored.");
        return;
    }

    const urlValue = inputField.value.trim();

    if (!urlValue) {
        alert("Please paste a product link first.");
        inputField.focus();
        return;
    }

    if (!isValidUrl(urlValue)) {
        alert("Please enter a valid product URL.");
        inputField.focus();
        return;
    }

    if (!isFlipkartUrl(urlValue)) {
        alert("Please enter a valid Flipkart product URL.");
        inputField.focus();
        return;
    }

    storedProductUrl = urlValue;
    isAnalyzing = true;

    const originalBtnText = analyzeBtn.innerHTML;

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = "<span>⏳</span><span>Analyzing...</span>";

    resultStatus.textContent = "Scraping and analyzing reviews...";
    resultsSection.hidden = true;

    try {
        console.log("Starting analysis for:", storedProductUrl);

        // const response = await fetch(
        //     "http://127.0.0.1:5000/analyze",
        //     {
        //         method: "POST",
        //         headers: {
        //             "Content-Type": "application/json"
        //         },
        //         body: JSON.stringify({
        //             url: storedProductUrl
        //         })
        //     }
        // );

        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: storedProductUrl
            })
        });

        console.log("Response received:", response.status);

        let data;

        try {
            data = await response.json();
            console.log("Response data:", data);
        } catch (error) {
            throw new Error(
                "The server returned an invalid response. Check Flask."
            );
        }

        if (!response.ok || data.status !== "success") {
            throw new Error(
                data.error || `Analysis failed (HTTP ${response.status}).`
            );
        }

        const summary = data.summary || {};

        const total = Number(data.total_reviews) || 0;
        const evaluated = Number(summary.evaluated) || 0;
        const genuine = Number(summary.genuine) || 0;
        const fake = Number(summary.fake) || 0;
        const skipped = Number(summary.skipped) || 0;

        // Update dashboard cards.
        document.getElementById("totalReviews").textContent = total;
        document.getElementById("evaluatedReviews").textContent = evaluated;
        document.getElementById("genuineReviews").textContent = genuine;
        document.getElementById("fakeReviews").textContent = fake;
        document.getElementById("skippedReviews").textContent = skipped;

        // Calculate percentages using evaluated reviews.
        const genuinePct = evaluated > 0
            ? (genuine / evaluated) * 100
            : 0;

        const fakePct = evaluated > 0
            ? (fake / evaluated) * 100
            : 0;

        document.getElementById("genuinePercentage").textContent =
            genuinePct.toFixed(1) + "%";

        document.getElementById("fakePercentage").textContent =
            fakePct.toFixed(1) + "%";

        // Draw the prediction chart.
        drawPieChart(genuine, fake);

        // Show the completed results.
        resultsSection.hidden = false;

        resultStatus.textContent =
            `Analysis complete. ${evaluated} reviews evaluated.`;

        console.log("Revora analysis completed:", data);

        resultsSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {
        console.error("Analysis error:", error);

        resultStatus.textContent = error.message;

        if (
            error instanceof TypeError &&
            error.message.toLowerCase().includes("fetch")
        ) {
            alert(
                "Cannot connect to Flask. Make sure app.py is running on port 5000."
            );
        } else {
            alert(error.message);
        }

    } finally {
        isAnalyzing = false;
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = originalBtnText;
    }
}

function drawPieChart(genuine, fake) {
    const canvas = document.getElementById("reviewPieChart");

    if (!canvas) {
        console.error("Chart canvas #reviewPieChart was not found.");
        return;
    }

    const ctx = canvas.getContext("2d");

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 105;
    const total = genuine + fake;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (total === 0) {
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
        ctx.fillStyle = "#E2E8F0";
        ctx.fill();

        ctx.fillStyle = "#64748B";
        ctx.font = "16px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText("No evaluated reviews", centerX, centerY);

        return;
    }

    const slices = [
        { value: genuine, color: "#15976A" },
        { value: fake, color: "#E24B61" }
    ];

    let startAngle = -Math.PI / 2;

    slices.forEach(slice => {
        if (slice.value === 0) return;

        const endAngle =
            startAngle + (slice.value / total) * Math.PI * 2;

        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(
            centerX,
            centerY,
            radius,
            startAngle,
            endAngle
        );
        ctx.closePath();

        ctx.fillStyle = slice.color;
        ctx.fill();

        ctx.strokeStyle = "#FFFFFF";
        ctx.lineWidth = 3;
        ctx.stroke();

        startAngle = endAngle;
    });

    // Doughnut-style center.
    ctx.beginPath();
    ctx.arc(centerX, centerY, 55, 0, Math.PI * 2);
    ctx.fillStyle = "#FFFFFF";
    ctx.fill();

    ctx.fillStyle = "#0F172A";
    ctx.font = "bold 25px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(String(total), centerX, centerY - 5);

    ctx.fillStyle = "#64748B";
    ctx.font = "12px Arial";
    ctx.fillText("Evaluated", centerX, centerY + 17);
}

/* Register the button click handler */
analyzeBtn.addEventListener("click", handleAnalysis);

/* Support Enter in the URL input */
inputField.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        event.preventDefault();
        handleAnalysis(event);
    }
});

