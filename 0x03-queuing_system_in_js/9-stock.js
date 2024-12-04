import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;

// Set up Redis client
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// List of products
const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

// Get product by id
function getItemById(id) {
  return listProducts.find(item => item.id === id);
}

// Route: List all products
app.get('/list_products', (req, res) => {
  const products = listProducts.map(product => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
  }));
  res.json(products);
});

// Route: Get product details by ID
app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const product = getItemById(Number(itemId));

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  try {
    const reservedStock = await getAsync(`item.${itemId}`);
    const currentQuantity = product.stock - (reservedStock ? parseInt(reservedStock, 10) : 0);

    res.json({
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
      currentQuantity,
    });
  } catch (err) {
    console.error('Redis error:', err);
    res.status(500).json({ status: 'Internal server error' });
  }
});

// Route: Reserve product
app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const product = getItemById(Number(itemId));

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  try {
    const reservedStock = await getAsync(`item.${itemId}`);
    const currentStock = product.stock - (reservedStock ? parseInt(reservedStock, 10) : 0);

    if (currentStock <= 0) {
      return res.status(400).json({ status: 'Not enough stock available', itemId: product.id });
    }

    // Reserve stock
    await setAsync(`item.${itemId}`, (reservedStock ? parseInt(reservedStock, 10) : 0) + 1);

    res.json({ status: 'Reservation confirmed', itemId: product.id });
  } catch (err) {
    console.error('Redis error:', err);
    res.status(500).json({ status: 'Internal server error' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
