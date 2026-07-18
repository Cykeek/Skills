# Wix Stores (eCommerce) — Reference

## 1. Setup
1. Dashboard → Add Apps → Wix Stores
2. Wix plan must be Business minimum
3. Connect a payment provider

## 2. Product Types
| Type | Description | Example |
|------|-------------|---------|
| Physical | Tangible, needs shipping | T-shirt, book |
| Digital | Downloadable file | PDF, ebook |
| Service | Non-physical | Consultation |
| Subscription | Recurring (via Pricing Plans) | Monthly box |

## 3. Product Settings
**Fields:** Name, Description, Price, SKU, Images, Categories, Weight/Dimensions, Stock, Visibility

**Options & Variants:** Size/Color/Material options → variant combinations with individual price/SKU/stock
- **Bulk variant editor** (2024+): Spreadsheet-style editor for all variant combos
- **Variant images** (2024+): Multiple images and video per variant

**AI Product Descriptions (2024+):** Dashboard → Product → Description → "Write with AI" — choose tone (Professional/Casual/Enthusiastic/Luxury) and length

**Product Add-ons:** "Add gift wrapping for $3" style upsells at checkout

## 4. Store Collections (Categories)
- Different from CMS Collections
- Products can belong to multiple store collections
- Collections have their own display page

## 5. Payment Providers
| Provider | Regions | Notes |
|---------|---------|-------|
| Wix Payments | US, UK, EU, CA, AU, others | Native — supports cards + Apple Pay + Google Pay |
| PayPal | Worldwide | Very widely accepted |
| Stripe | Worldwide | Developer-friendly |
| Square | US, CA, AU, UK, JP | POS integration |
| Razorpay / Paytm | India | Indian market |
| Klarna / Afterpay / **Affirm** | EU, US | Buy Now Pay Later |
| **Shop Pay** | US, CA | Shopify accelerated checkout |
| **iDEAL** / **Sofort** / **Bancontact** | EU | Local payment methods |
| **Boleto** | Brazil | Local payment method |
| **SEPA Direct Debit** | EU | Bank transfer |
| Offline/Manual | Anywhere | Cash on delivery, bank transfer |

**Setup:** Dashboard → Store → Settings → Accept Payments → Connect provider

## 6. Shipping
**Path:** Dashboard → Store → Settings → Shipping & Delivery

**Options:**
- Free shipping (always or above minimum)
- Flat rate (per order or per item weight)
- Rate by weight or price
- Real-time carrier rates (UPS, FedEx, USPS, DHL)
- Local pickup / Local delivery (radius-based)
- **Multi-origin shipping** (new): Different shipping origins per product
- **Shipping zones** (enhanced): Complex regional rules with overlapping zones
- **Table-rate shipping** (new): Advanced rate tables
- **Shipped by supplier** (new): Dropshipping-friendly

## 7. Tax
**Path:** Dashboard → Store → Settings → Tax

- Automatic calculation by location
- Manual tax rates per region
- Tax-inclusive pricing toggle
- Tax-exempt customers
- **Avalara integration** (new): Automated US sales tax compliance
- **VAT/MOSS support** (enhanced): EU digital services VAT

## 8. Order Management
**Path:** Dashboard → Store → Orders

**Statuses:** Pending → Processing → Fulfilled → Cancelled / Refunded

**Actions:** Mark fulfilled, print packing slip, add tracking, issue refund (full/partial), archive, download CSV

## 9. Discounts & Promotions
**Path:** Dashboard → Store → Marketing → Coupons & Promotions

**Types:** Percentage, Fixed amount, Free shipping, Buy X Get Y

**Restrictions:** Minimum order, specific products/collections, one-time use, limited uses, expiry date

## 10. Abandoned Cart Recovery
**Path:** Dashboard → Store → Marketing → Abandoned Cart Recovery
Auto-emails customers who added to cart but didn't purchase. Configurable timing (e.g., 1 hour after abandonment).

## 11. Store Analytics
**Path:** Dashboard → Analytics → Store Reports
Revenue over time, Orders by product, Sales by country, Customer history, Conversion funnel, Average order value

## 12. Velo + Stores
```javascript
import wixStores from 'wix-stores';
import { cart } from 'wix-stores-frontend';

// Get cart
const currentCart = await cart.getCurrentCart();

// Add to cart
await cart.addToCart('product-id', 1, { options: { Size: 'M', Color: 'Blue' } });

// Checkout
await cart.checkout();

// Query products
const allProducts = await wixStores.queryProducts()
  .eq('collections.id', 'collection-id')
  .limit(12)
  .find();
```

## 13. New SDK Pattern (@wix/stores / @wix/ecom)
```javascript
import { products } from '@wix/stores';
import { orders } from '@wix/ecom';

// Query products
const { items } = await products.queryProducts().eq('visible', true).find();

// Search orders
const { orders: orderList } = await orders.searchOrders({ filter: { status: 'PAID' } });
```

> **Note:** For new projects, prefer `/ecom/v1/*` REST endpoints over `/stores/v1/*`

## 14. Known eCommerce Issues
| Bug | Workaround |
|-----|-----------|
| Cart badge count not updating instantly | Refresh or use `cart.onChange()` listener |
| Product options not saving correctly | Re-save product after setting options |
| Refund not restoring inventory | Manually adjust inventory after refund |
| PayPal failing in some countries | Try Wix Payments or another provider |
| Tax-inclusive price not showing | Confirm tax settings, restart checkout |
| Abandoned cart email not triggering | Check it's enabled in Store → Marketing |
| Multi-currency display inconsistent | Verify settings per product |
| Discount stacking uncontrolled | Use separate promotion periods |
