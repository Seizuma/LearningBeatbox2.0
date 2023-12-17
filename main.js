const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
let mainWindow;
let pythonProcess = null;


function createWindow() {
    mainWindow = new BrowserWindow({
        // ... vos options ...
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js') // Vous pouvez utiliser un script de préchargement pour plus de sécurité
        }
    });

    mainWindow.loadFile('public/index.html');

    // Charger le fichier index.html
    mainWindow.on('closed', function () {
        if (pythonProcess) {
            pythonProcess.kill();
        }
        mainWindow = null;
    });
}

ipcMain.on('start-python', () => {
    if (!pythonProcess) {
        pythonProcess = spawn('python', ['play.py']); // Lancez play.py qui doit inclure ou appeler mode_tutorial_a.py

        pythonProcess.stdout.on('data', (data) => {
            const output = data.toString().trim();
            // Supposons que mode_tutorial_a.py imprime des lignes commençant par "Detected:"
            // pour les sons qu'il détecte.
            if (output.startsWith("Detected:")) {
                mainWindow.webContents.send('python-data', output);
            }
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            console.log(`child process exited with code ${code}`);
            pythonProcess = null;
        });
    }
});


ipcMain.on('stop-python', () => {
    if (pythonProcess) {
        pythonProcess.kill();
        pythonProcess = null;
    }
});

// Cette méthode sera appelée quand Electron aura fini
// de s'initialiser et sera prêt à créer des fenêtres de navigation.
// Certaines APIs peuvent être utilisées uniquement après que cet événement se produit.
app.on('ready', createWindow);

// Quitter lorsque toutes les fenêtres sont fermées.
app.on('window-all-closed', function () {
    // Sur macOS, il est commun pour une application et sa barre de menu
    // de rester active jusqu'à ce que l'utilisateur quitte explicitement avec Cmd + Q
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', function () {
    // Sur macOS, il est commun de re-créer une fenêtre dans l'application quand
    // l'icône du dock est cliquée et qu'il n'y a pas d'autres fenêtres ouvertes.
    if (mainWindow === null) createWindow();
});
