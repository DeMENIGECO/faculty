// DFF 1

// Funzionalità 1
// Crea sessione
function createSession() {
    const sessionId = 'session_' + new Date().getTime()
    const name = prompt("Inserisci il nome della sessione: ", "My Session")
    if (name) {
        localStorage.setItem('session', sessionId)
        localStorage.setItem('sessionName', name)
    }
    else {
        alert("Nessun nome inserito, sessione non creata.")
    }
}


// Funzionalità 2
// Verifica sessione

function checkSession() {
    const session = localStorage.getItem('session')
    if (!session) {
        alert("Sessione non trovata, ne stiamo creando una per te!")
        createSession()
    }
    else {
        const name = localStorage.getItem('sessionName')
        alert("Sessione trovata: " + name)
    }
}

// Funzionalità 3
// Elimina sessione

function deleteSession() {
    const confirmDelete = confirm("Sei sicuro di voler eliminare questa sessione? Questa azione è irreversibile.")
    if (confirmDelete) {
        localStorage.removeItem('session')
        localStorage.removeItem('sessionName')
        alert("Sessione eliminata.")
    }
    else {
        alert("Eliminazione annullata.")
    }
}