const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
let mainWindow;
let pythonProcess = null;

function createWindow() {
    mainWindow = new BrowserWindow({
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        }
    });

    mainWindow.loadFile('public/index.html');

    mainWindow.on('closed', function () {
        if (pythonProcess) {
            pythonProcess.kill();
        }
        mainWindow = null;
    });
}

ipcMain.on('start-python', () => {
    if (!pythonProcess) {
        pythonProcess = spawn('python', ['-u', 'play.py']);


        pythonProcess.stdout.on('data', (data) => {
            const output = data.toString().trim();
            const lines = output.split('\n'); // Sépare les différentes lignes pour traiter chaque sortie individuellement
            lines.forEach(line => {
                if (line.startsWith("Detected:")) {
                    const soundName = line.substring(10).trim(); // Obtenez le nom après 'Detected: '
                    mainWindow.webContents.send('python-data', soundName);
                }
            });
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

app.on('ready', createWindow);

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', function () {
    if (mainWindow === null) {
        createWindow();
    }
});
