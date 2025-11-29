#!/bin/bash

# Script para poblar el menú de Pardos Chicken con imágenes
# API Gateway URL
API_URL="https://c9sut9oprg.execute-api.us-east-1.amazonaws.com"
TENANT_ID="pardos-chicken"

echo "🍗 Poblando menú de Pardos Chicken con imágenes..."
echo "======================================"

# POLLOS
echo "Agregando Pollos..."

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pollo Entero",
    "price": 62.90,
    "category": "Pollos",
    "description": "Pollo a la brasa entero con papas y ensalada",
    "image_url": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=500&q=80"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "1/2 Pollo",
    "price": 35.90,
    "category": "Pollos",
    "description": "Medio pollo a la brasa con papas y ensalada",
    "image_url": "https://images.unsplash.com/photo-1594221708779-94832f4320d1?w=500&q=80"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "1/4 Pollo",
    "price": 21.90,
    "category": "Pollos",
    "description": "Cuarto de pollo a la brasa con papas y ensalada",
    "image_url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=500&q=80"
  }'

# PARRILLAS
echo "Agregando Parrillas..."

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Parrilla Personal",
    "price": 42.90,
    "category": "Parrillas",
    "description": "Anticuchos, chorizo, mollejitas y papas",
    "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&q=80"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Parrilla Familiar",
    "price": 89.90,
    "category": "Parrillas",
    "description": "Parrilla para 2-3 personas con variedad de carnes",
    "image_url": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=500&q=80"
  }'

# ENTRADAS
echo "Agregando Entradas..."

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Anticuchos (3 unid)",
    "price": 18.90,
    "category": "Entradas",
    "description": "Anticuchos de corazón con papa y choclo",
    "image_url": "https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=500&q=80"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chorizo Parrillero",
    "price": 16.90,
    "category": "Entradas",
    "description": "Chorizo argentino con papa dorada",
    "image_url": "https://images.unsplash.com/photo-1612392166886-ee7b99725fdf?w=500&q=80"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mollejitas",
    "price": 15.90,
    "category": "Entradas",
    "description": "Mollejas a la parrilla con limón",
    "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=500&q=80"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tequeños (6 unid)",
    "price": 12.90,
    "category": "Entradas",
    "description": "Tequeños de queso con salsa golf",
    "image_url": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&q=80"
  }'

# ENSALADAS
echo "Agregando Ensaladas..."

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ensalada César",
    "price": 24.90,
    "category": "Ensaladas",
    "description": "Lechuga, pollo, crutones y aderezo césar",
    "image_url": "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=500&q=80"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ensalada Palta Reina",
    "price": 22.90,
    "category": "Ensaladas",
    "description": "Palta rellena con pollo y verduras",
    "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500&q=80"
  }'

# BEBIDAS
echo "Agregando Bebidas..."

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Inca Kola 1.5L",
    "price": 8.90,
    "category": "Bebidas",
    "description": "Gaseosa Inca Kola de 1.5 litros",
    "image_url": "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=500&q=80"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Coca Cola 1.5L",
    "price": 8.90,
    "category": "Bebidas",
    "description": "Gaseosa Coca Cola de 1.5 litros",
    "image_url": "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=500&q=80"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chicha Morada 1L",
    "price": 7.90,
    "category": "Bebidas",
    "description": "Chicha morada natural de 1 litro",
    "image_url": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=500&q=80"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Limonada Frozen",
    "price": 9.90,
    "category": "Bebidas",
    "description": "Limonada frozen de 500ml",
    "image_url": "https://images.unsplash.com/photo-1523677011781-c91d1bbe1f33?w=500&q=80"
  }'

# POSTRES
echo "Agregando Postres..."

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Suspiro Limeño",
    "price": 12.90,
    "category": "Postres",
    "description": "Postre tradicional peruano",
    "image_url": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=500&q=80"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Picarones con Miel",
    "price": 11.90,
    "category": "Postres",
    "description": "6 picarones con miel de chancaca",
    "image_url": "https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?w=500&q=80"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Brownie con Helado",
    "price": 14.90,
    "category": "Postres",
    "description": "Brownie de chocolate con helado de vainilla",
    "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500&q=80"
  }'

echo ""
echo "✅ Menú poblado exitosamente con imágenes!"
echo "Total de productos agregados: 18"
echo ""
echo "Categorías:"
echo "- Pollos: 3 productos"
echo "- Parrillas: 2 productos"
echo "- Entradas: 4 productos"
echo "- Ensaladas: 2 productos"
echo "- Bebidas: 4 productos"
echo "- Postres: 3 productos"
echo ""
echo "Todas las imágenes están hospedadas en Unsplash"
