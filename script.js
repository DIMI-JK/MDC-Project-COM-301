let storedProductUrl = "";

const inputField = document.getElementById('productUrl');
const analyzeBtn = document.getElementById('analyzeBtn');

function isValidUrl(string) {
    try {
        const url = new URL(string);
        return url.protocol === "http:" || url.protocol === "https:";
    } catch (_) {
        return false;
    }
}

function handleAnalysis() {
    const urlValue = inputField.value.trim();

    if (!urlValue) {
        alert("Please paste a valid link first.");
        return;
    }

    if (!isValidUrl(urlValue)) {
        alert("Please enter a valid URL (e.g., https://www.flipkart.com/...)");
        return;
    }

    storedProductUrl = urlValue;
    console.log("Stored Product URL:", storedProductUrl);
    alert("URL successfully saved:\n" + storedProductUrl);
}

analyzeBtn.addEventListener('click', handleAnalysis);

inputField.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        handleAnalysis();
    }
});