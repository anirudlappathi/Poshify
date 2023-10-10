const express = require('express');
const multer = require('multer');
const path = require('path');
const app = express();
const port = 3000;

// Set storage engine
const storage = multer.diskStorage({
    destination: './uploads/',
    filename: function (req, file, cb) {
        cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
    }
});

// Initialize upload
const upload = multer({
    storage: storage
}).single('image');

app.use(express.static('public'));

app.post('/upload', (req, res) => {
    upload(req, res, (err) => {
        if (err) {
            res.json({ message: 'Error uploading file.' });
        } else {
            res.json({ message: 'File uploaded successfully.' });
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});