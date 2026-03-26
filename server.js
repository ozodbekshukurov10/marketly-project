const express = require('express');
const fs = require('fs'); // Fayl bilan ishlash uchun kutubxona
const path = require('path');
const app = express();
const PORT = 3000;

// 1. Sozlamalar
app.use(express.json()); // JSON ma'lumotlarni qabul qilish uchun
app.use(express.static(__dirname)); // HTML, CSS fayllarni ko'rsatish uchun

// 2. Sahifalarni yuborish
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// 3. Ma'lumotlarni saqlash (Boshlash sahifasidan keladigan so'rov)
app.post('/save-data', (req, res) => {
    const { email, role } = req.body;
    
    // Saqlanadigan matn formati
    const logEntry = `Vaqt: ${new Date().toLocaleString()} | Email: ${email} | Rol: ${role}\n`;
    
    console.log("📥 Yangi ma'lumot keldi:", logEntry);

    // Ma'lumotni 'users.txt' fayliga qo'shib yozish
    fs.appendFile('users.txt', logEntry, (err) => {
        if (err) {
            console.error("❌ Faylga yozishda xato:", err);
            return res.status(500).send({ status: "Xatolik" });
        }
        res.send({ status: "Muvaffaqiyatli saqlandi ✅" });
    });
});

// server.js faylining oxiriga (app.listen dan tepaga) qo'shing:
app.post('/save-profile', (req, res) => {
    const data = req.body;
    const log = `[YANGI FOYDALANUVCHI] | Ism: ${data.firstname} ${data.lastname} | Yosh: ${data.age} | Tel: ${data.phone} | Email: ${data.email} | Rol: ${data.role}\n`;
    
    console.log("📂 To'liq ma'lumot saqlandi:", log);
    
    fs.appendFile('users.txt', log, (err) => {
        if (err) return res.status(500).send({status: "Error"});
        res.send({status: "Success"});
    });
});

app.post('/save-final-user', (req, res) => {
    const d = req.body;
    const log = `[YAKUNIY QAYD] | Rol: ${d.role} | Ism: ${d.firstname} ${d.lastname} | Yosh: ${d.age} | Tel: ${d.phone} | Vaqt: ${new Date().toLocaleString()}\n`;
    
    fs.appendFile('users.txt', log, (err) => {
        if (err) return res.status(500).send({status: "Xato"});
        console.log("📂 Yangi to'liq foydalanuvchi saqlandi!");
        res.send({status: "OK"});
    });
});

app.post('/save-final-user', (req, res) => {
    const d = req.body;
    const log = `[YAKUNIY QAYD] | Rol: ${d.role} | Ism: ${d.firstname} ${d.lastname} | Tel: ${d.phone}\n`;
    
    fs.appendFile('users.txt', log, (err) => {
        if (err) return res.status(500).send({status: "Xato"});
        
        // Rolga qarab qaysi sahifaga o'tishni belgilaymiz
        let targetPage = "/xaridor.html"; // Standart holatda
        if (d.role === "Tadbirkor") {
            targetPage = "/tadbirkor.html";
        }

        console.log(`📂 Foydalanuvchi saqlandi va ${targetPage} ga yo'naltirildi.`);
        
        // Frontend'ga manzilni yuboramiz
        res.send({ status: "OK", redirectUrl: targetPage });
    });
});


// 4. Serverni yoqish
app.listen(PORT, () => {
    console.log(` Marketly serveri yoqildi: http://localhost:${PORT}`);
});

