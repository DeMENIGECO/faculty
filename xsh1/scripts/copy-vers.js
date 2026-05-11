function copyToClipboard() {
    navigator.clipboard.writeText('Versione 1.0.4 – 11 Maggio 2026')
        .then(() => {
            alert("Testo copiato!");
        })
        .catch(err => {
            alert("Errore nella copia");
            console.error(err);
        });
}