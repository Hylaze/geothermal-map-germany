const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const imageFolder = path.join(__dirname, 'images'); // Adjust folder path as needed

app.use('/images', express.static(imageFolder)); // Serve images statically

app.get('/get-images', (req, res) => {
    fs.readdir(imageFolder, (err, files) => {
        if (err) {
            return res.status(500).send('Unable to scan folder');
        }
        // Filter for image files (you can add more extensions if needed)
        const imageFiles = files.filter(file => /\.(jpg|jpeg|png|gif)$/i.test(file));
        res.json(imageFiles);
    });
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
