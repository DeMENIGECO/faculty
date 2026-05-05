function copyToClipboard() {
    navigator.clipboard.writeText('Insiders versione 1.0.0 – 5 Maggio 2026')
        .then(() => {
            alert("Testo copiato!");
        })
        .catch(err => {
            alert("Errore nella copia");
            console.error(err);
        });
}