const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3000;

// 1. SOZLAMALAR (MIDDLEWARE)
app.use(express.json()); 
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

// 2. SAHIFALARNI YUBORISH
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// 3. QADAMBA-QADAM MA'LUMOTLARNI SAQLASH

// Email va rolni vaqtincha saqlash
app.post('/save-data', (req, res) => {
    const { email, role } = req.body;
    const logEntry = `[BOSHLANG'ICH] | Vaqt: ${new Date().toLocaleString()} | Email: ${email} | Rol: ${role}\n`;
    
    fs.appendFile('users.txt', logEntry, (err) => {
        if (err) return res.status(500).send({ status: "Xato" });
        res.send({ status: "Muvaffaqiyatli saqlandi ✅" });
    });
});

// Shaxsiy ma'lumotlarni saqlash (Profil sahifasidan)
app.post('/save-profile', (req, res) => {
    const d = req.body;
    const log = `[PROFIL] | Ism: ${d.firstname} ${d.lastname} | Yosh: ${d.age} | Tel: ${d.phone} | Email: ${d.email} | Rol: ${d.role}\n`;
    
    fs.appendFile('users.txt', log, (err) => {
        if (err) return res.status(500).send({status: "Error"});
        res.send({status: "Success"});
    });
});

// YAKUNIY RO'YXATDAN O'TISH VA YO'NALTIRISH
app.post('/save-final-user', (req, res) => {
    const d = req.body;
    const log = `[YAKUNIY QAYD] | Rol: ${d.role} | Ism: ${d.firstname} ${d.lastname} | Tel: ${d.phone} | Vaqt: ${new Date().toLocaleString()}\n`;
    
    fs.appendFile('users.txt', log, (err) => {
        if (err) return res.status(500).send({status: "Xato"});
        
        // Rolga qarab yo'naltirish
        let targetPage = "/xaridor.html";
        if (d.role === "Tadbirkor") {
            targetPage = "/tadbirkor.html";
        }

        console.log(`📂 Foydalanuvchi saqlandi va ${targetPage} ga yuborildi.`);
        res.send({ status: "OK", redirectUrl: targetPage });
    });
});

// 4. TADBIRKOR MAHSULOT QO'SHISHI
app.post('/add-product', (req, res) => {
    const { productName, price, description } = req.body;
    const productLog = `[YANGI MAHSULOT] | Nomi: ${productName} | Narxi: ${price} UZS | Tavsif: ${description} | Vaqt: ${new Date().toLocaleString()}\n`;

    console.log(" Yangi mahsulot keldi:", productName);

    fs.appendFile('products.txt', productLog, (err) => {
        if (err) return res.status(500).send({status: "Error"});
        res.send({status: "OK"});
    });
});

// Mahsulotlarni JSON faylda saqlash (o'qish oson bo'lishi uchun)
app.post('/add-product', (req, res) => {
    const newProduct = req.body;
    
    fs.readFile('products.json', (err, data) => {
        let products = [];
        if (!err && data.length > 0) products = JSON.parse(data);
        
        products.push(newProduct);
        
        fs.writeFile('products.json', JSON.stringify(products), (err) => {
            if (err) return res.status(500).send("Xato");
            res.send({ status: "OK" });
        });
    });
});

// E'lonlarni qaytarish
app.get('/api/get-products', (req, res) => {
    fs.readFile('products.json', (err, data) => {
        if (err || data.length === 0) return res.json([]);
        res.json(JSON.parse(data));
    });
});

function submitAd() {
    // ... fetch kodlari ...
    // E'lon berilgandan keyin feed sahifasiga o'tish
    window.location.href = "feed.html";
}

// server.js ga qo'shing
app.get('/api/user-orders', (req, res) => {
    // Bu yerda foydalanuvchi buyurtmalari ro'yxatini qaytarishingiz mumkin
    res.json([
        { id: 101, date: "2024-05-10", total: "2,000,000 UZS", status: "Yetkazib berildi" }
    ]);
});

app.post('/api/save-compare', (req, res) => {
    const compareData = req.body;
    // Faylga yoki DB'ga saqlash mantig'i
    fs.appendFileSync('compare_logs.txt', `Solishtirildi: ${JSON.stringify(compareData)}\n`);
    res.send({ status: "OK" });
});


// 5. SERVERNI YOQISH
app.listen(PORT, () => {
    console.log(` Marketly serveri yoqildi: http://localhost:${PORT}`);
});
