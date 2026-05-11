function copyToClipboard() {
    navigator.clipboard.writeText('Version 1.0.4 – May 11, 2026')
        .then(() => {
            alert("Text copied!");
        })
        .catch(err => {
            alert("Error copying text");
            console.error(err);
        });
}