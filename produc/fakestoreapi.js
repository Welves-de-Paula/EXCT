import axios from 'axios';


export default {
  async get() {
    let products = [];
    const response = await axios.get("https://fakestoreapi.com/products");
    let items = response.data;

    for (let i = 0; i < items.length; i++) {
      let product = {
        // "id": 5,
        // "title": "John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet",
        // "price": 695,
        // "description": "From our Legends Collection, the Naga was inspired by the mythical water dragon that protects the ocean's pearl. Wear facing inward to be bestowed with love and abundance, or outward for protection.",
        // "category": "jewelery",
        // "image": "https://fakestoreapi.com/img/71pWzhdJNwL._AC_UL640_QL65_ML3_.jpg",


        'name': items[i].title,
        'price': items[i].price,
        'cost': Math.round(items[i].price * 0.5 * 100) / 100, // Assuming cost is 80% of price
        'category': items[i].category,
        'description': items[i].description,
        'imageUrls': [items[i].image],
        'stock': items[i].id + Math.floor(Math.random() * 100), // Random stock for demonstration
        'reference': `FAK-${items[i].id}` // Example reference format
      }
      products.push(product);
    }
    return products;
  }
}