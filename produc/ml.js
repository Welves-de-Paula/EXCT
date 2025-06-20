import axios from 'axios';


export default {
  async get() {
    let products = [];
    const response = await axios.get("https://fakestoreapi.com/products");
    // let items = response.data;

    // for (let i = 0; i < items.length; i++) {
    //   let product = {
    //     // "id": 5,


    //     'name': items[i].title,
    //     'price': items[i].price,
    //     'cost': Math.round(items[i].price * 0.5 * 100) / 100, // Assuming cost is 80% of price
    //     'category': items[i].category,
    //     'description': items[i].description,
    //     'imageUrls': [items[i].image],
    //     'stock': items[i].id + Math.floor(Math.random() * 100), // Random stock for demonstration
    //     'reference': `FAK-${items[i].id}` // Example reference format
    //   }
    //   products.push(product);
    // }
    // return products;
  }
}

https://www.mercadolivre.com.br/smartphone-motorola-moto-g15-256gb-12gb-4gb-ram8gb-ram-boost-e-camera-50mp-com-ai-e-night-vision-bateria-de-5200-mah-tela-fhd-67-com-superbrilho-nfc-grafite/p/MLB44665473?pdp_filters=item_id%3AMLB5237338738&pdp_filters=official_store%3A1656#polycard_client%3Drecommendations_recoview-selleritems-eshops%26reco_backend%3Dsame-seller-odin%26wid%3DMLB5237338738%26reco_client%3Drecoview-selleritems-eshops%26reco_item_pos%3D0%26reco_backend_type%3Dlow_level%26reco_id%3D04d069c3-e0e7-4969-a5c3-3b6d84f59ee1%26sid%3Drecos%26tracking_id%3Dff58910a-d966-4fd5-8453-3733406d66b4%26source%3Deshops%26seller_id%3D326016487%26category_id%3DMLB1055


