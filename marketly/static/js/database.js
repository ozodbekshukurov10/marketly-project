window.productsData = [
  {
    id: 1,
    title: "Zamonaviy Ofis",
    price: "2,000,000",
    img: "https://picsum.photos/seed/office/640/480",
    backupImg: "https://loremflickr.com/640/480/office",
  },
  {
    id: 2,
    title: "Marketing Xizmati",
    price: "Bepul",
    img: "https://picsum.photos/seed/marketing/640/480",
    backupImg: "https://loremflickr.com/640/480/marketing",
  },
  {
    id: 3,
    title: "iPhone 15 Pro",
    price: "12,000,000",
    img: "https://picsum.photos/seed/iphone/640/480",
    backupImg: "https://loremflickr.com/640/480/phone",
  },
  {
    id: 4,
    title: "Macbook Air M2",
    price: "14,500,000",
    img: "https://picsum.photos/seed/macbook/640/480",
    backupImg: "https://loremflickr.com/640/480/laptop",
  },
  {
    id: 5,
    title: "Kreativ Dizayn",
    price: "500,000",
    img: "https://picsum.photos/seed/design/640/480",
    backupImg: "https://loremflickr.com/640/480/design",
  },
  {
    id: 6,
    title: "SMM Kursi",
    price: "1,200,000",
    img: "https://picsum.photos/seed/course/640/480",
    backupImg: "https://loremflickr.com/640/480/study",
  },
];

window.handleImageError = function handleImageError(imgElement, backupUrl) {
  imgElement.onerror = null;
  imgElement.src = backupUrl;
};
