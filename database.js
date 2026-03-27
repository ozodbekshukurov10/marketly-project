// database.js ga yangi maydonlar qo'shing
const productsData = [
    { 
        id: 1, 
        title: "iPhone 15 Pro", 
        price: "12,000,000", 
        category: "Elektronika",
        specs: { ekran: "6.1 inch OLED", batareya: "3274 mAh", kamera: "48 MP" },
        img: "https://picsum.photos"
    },
    { 
        id: 2, 
        title: "Samsung S23 Ultra", 
        price: "11,500,000", 
        category: "Elektronika",
        specs: { ekran: "6.8 inch AMOLED", batareya: "5000 mAh", kamera: "200 MP" },
        img: "https://picsum.photos"
    }
];



// database.js
const productsData = [
    { 
        id: 1, 
        title: "Zamonaviy Ofis", 
        price: "2,000,000", 
        img: "https://picsum.photos",
        backupImg: "https://loremflickr.com"
    },
    { 
        id: 2, 
        title: "Marketing Xizmati", 
        price: "Bepul", 
        img: "https://picsum.photos",
        backupImg: "https://loremflickr.com"
    },
    { 
        id: 3, 
        title: "iPhone 15 Pro", 
        price: "12,000,000", 
        img: "https://picsum.photos",
        backupImg: "https://loremflickr.com"
    },
    { 
        id: 4, 
        title: "Macbook Air M2", 
        price: "14,500,000", 
        img: "https://picsum.photos",
        backupImg: "https://loremflickr.com"
    },
    { 
        id: 5, 
        title: "Kreativ Dizayn", 
        price: "500,000", 
        img: "https://picsum.photos",
        backupImg: "https://loremflickr.com"
    },
    { 
        id: 6, 
        title: "SMM Kursi", 
        price: "1,200,000", 
        img: "https://picsum.photos",
        backupImg: "https://loremflickr.com"
    }
];

// Rasmni tekshirish funksiyasi (agar asosiy rasm ishlamasa, zaxirasini qo'yadi)
function handleImageError(imgElement, backupUrl) {
    imgElement.onerror = null; // Cheksiz siklni to'xtatish
    imgElement.src = backupUrl;
}

