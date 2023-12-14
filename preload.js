// preload.js

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    startPython: () => ipcRenderer.send('start-python'),
    stopPython: () => ipcRenderer.send('stop-python'),
    onPythonData: (callback) => ipcRenderer.on('python-data', (event, data) => callback(data))
});
