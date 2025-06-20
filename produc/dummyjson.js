import axios from 'axios';


export default {
  async get() {
    let products = [];
    const response = await axios.get("https://dummyjson.com/products?limit=999999999");
    let items = response.data.products;

    for (let i = 0; i < items.length; i++) {
      let product = {
        'name': items[i].title,
        'price': items[i].price,
        'cost': Math.round(items[i].price * 0.5 * 100) / 100, // Assuming cost is 80% of price
        'category': items[i].category,
        'description': items[i].description,
        'imageUrls': items[i].images,
        'stock': items[i].stock,
        'reference': items[i].sku
      }
      products.push(product);
    }
    return products;
  }
}