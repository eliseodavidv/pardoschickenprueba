#!/bin/bash

# Script para poblar el menú de Pardos Chicken
# API Gateway URL
API_URL="https://c9sut9oprg.execute-api.us-east-1.amazonaws.com"
TENANT_ID="pardos-chicken"

echo "🍗 Poblando menú de Pardos Chicken..."
echo "======================================"

# POLLOS
echo "Agregando Pollos..."

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pollo Entero",
    "price": 62.90,
    "category": "Pollos",
    "description": "Pollo a la brasa entero con papas y ensalada"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "1/2 Pollo",
    "price": 35.90,
    "category": "Pollos",
    "description": "Medio pollo a la brasa con papas y ensalada"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "1/4 Pollo",
    "price": 21.90,
    "category": "Pollos",
    "description": "Cuarto de pollo a la brasa con papas y ensalada"
  }'

# PARRILLAS
echo "Agregando Parrillas..."

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Parrilla Personal",
    "price": 42.90,
    "category": "Parrillas",
    "description": "Anticuchos, chorizo, mollejitas y papas"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Parrilla Familiar",
    "price": 89.90,
    "category": "Parrillas",
    "description": "Parrilla para 2-3 personas con variedad de carnes"
  }'

# ENTRADAS
echo "Agregando Entradas..."

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Anticuchos (3 unid)",
    "price": 18.90,
    "category": "Entradas",
    "description": "Anticuchos de corazón con papa y choclo"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chorizo Parrillero",
    "price": 16.90,
    "category": "Entradas",
    "description": "Chorizo argentino con papa dorada"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mollejitas",
    "price": 15.90,
    "category": "Entradas",
    "description": "Mollejas a la parrilla con limón"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tequeños (6 unid)",
    "price": 12.90,
    "category": "Entradas",
    "description": "Tequeños de queso con salsa golf"
  }'

# ENSALADAS
echo "Agregando Ensaladas..."

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ensalada César",
    "price": 24.90,
    "category": "Ensaladas",
    "description": "Lechuga, pollo, crutones y aderezo césar"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ensalada Palta Reina",
    "price": 22.90,
    "category": "Ensaladas",
    "description": "Palta rellena con pollo y verduras"
  }'

# BEBIDAS
echo "Agregando Bebidas..."

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Inca Kola 1.5L",
    "price": 8.90,
    "category": "Bebidas",
    "description": "Gaseosa Inca Kola de 1.5 litros"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Coca Cola 1.5L",
    "price": 8.90,
    "category": "Bebidas",
    "description": "Gaseosa Coca Cola de 1.5 litros"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chicha Morada 1L",
    "price": 7.90,
    "category": "Bebidas",
    "description": "Chicha morada natural de 1 litro"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Limonada Frozen",
    "price": 9.90,
    "category": "Bebidas",
    "description": "Limonada frozen de 500ml"
  }'

# POSTRES
echo "Agregando Postres..."

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Suspiro Limeño",
    "price": 12.90,
    "category": "Postres",
    "description": "Postre tradicional peruano"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Picarones con Miel",
    "price": 11.90,
    "category": "Postres",
    "description": "6 picarones con miel de chancaca"
  }'

curl -X POST "${API_URL}/tenants/${TENANT_ID}/menu" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Brownie con Helado",
    "price": 14.90,
    "category": "Postres",
    "description": "Brownie de chocolate con helado de vainilla"
  }'

echo ""
echo "✅ Menú poblado exitosamente!"
echo "Total de productos agregados: 18"
echo ""
echo "Categorías:"
echo "- Pollos: 3 productos"
echo "- Parrillas: 2 productos"
echo "- Entradas: 4 productos"
echo "- Ensaladas: 2 productos"
echo "- Bebidas: 4 productos"
echo "- Postres: 3 productos"
