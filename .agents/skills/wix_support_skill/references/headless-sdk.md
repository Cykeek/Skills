# Wix Headless & REST API — Reference

## What Is Wix Headless?
Decouples frontend from Wix backend. Build frontend in any framework (Next.js, Nuxt, React, Vue, Remix, SvelteKit, Angular) while using Wix as backend.

**Use cases:** SSR performance, mobile apps, custom checkout, omnichannel commerce, branded iOS/Android apps

## REST API

**Base URL:** `https://www.wixapis.com`

**Authentication:**
- **OAuth 2.0** (recommended for Headless) — Server-to-server or 3-legged user auth
- **API Key** (legacy, server-to-server) — Create at Dashboard → Settings → API Keys

### Key Endpoints
```
# CMS / Data
GET  POST  /wix-data/v2/collections/{collectionId}/items

# Stores (legacy)
GET  /stores/v1/products
POST /stores/v1/carts/{cartId}/lineItems

# Ecom (unified — prefer this for new projects)
POST /ecom/v1/checkout
POST /ecom/v1/orders
GET  /ecom/v1/orders

# Bookings
GET  /bookings/v2/services
POST /bookings/v2/bookings

# Members
GET  /members/v1/members/{memberId}

# Blog
GET  /blog/v3/posts

# Media (new)
POST /media/v1/images/upload
GET  /media/v1/files/{fileId}/download
```

> **💡 Tip:** Prefer `/ecom/v1/*` over older `/stores/v1/*` for new projects.

### Example REST Call
```javascript
const response = await fetch('https://www.wixapis.com/wix-data/v2/collections/Products/items', {
  headers: {
    'Authorization': 'YOUR_API_KEY',
    'wix-site-id': 'YOUR_SITE_ID'
  }
});
```

## Headless SDK (@wix/sdk)

### Installation
```bash
npm install @wix/sdk
npm install @wix/stores @wix/ecom @wix/members @wix/blog @wix/data @wix/bookings @wix/events @wix/media
```

### Basic Usage
```javascript
import { createClient, OAuthStrategy } from '@wix/sdk';
import { products } from '@wix/stores';
import { orders } from '@wix/ecom';
import { items } from '@wix/data';

const wixClient = createClient({
  modules: { products, orders, items },
  auth: OAuthStrategy({ clientId: 'YOUR_CLIENT_ID' })
});

// Query products
const { items: productItems } = await wixClient.products.queryProducts()
  .eq('visible', true)
  .limit(20)
  .find();

// Get specific product
const product = await wixClient.products.getProduct('product-id');
```

### SDK v2 — Auto-pagination & Streaming
```javascript
import { createClient } from '@wix/sdk';
import { products } from '@wix/stores';

const client = createClient({ auth: OAuthStrategy({ clientId: '...' }) });

// Streaming iterator with auto-pagination
const iter = client.products.queryProducts({ limit: 100 }).iterator();
for await (const page of iter) {
  console.log('Page:', page.items);
}
```

### Available SDK Modules
- `@wix/stores` — Products, collections, inventory
- `@wix/ecom` — Cart, checkout, orders (unified)
- `@wix/members` — Profiles, authentication
- `@wix/blog` — Posts, categories
- `@wix/bookings` — Services, availability
- `@wix/events` — Events, ticketing
- `@wix/data` — CMS collection operations
- `@wix/redirects` — URL redirects
- `@wix/media` — Images and media
- `@wix/seo` — SEO settings
- `@wix/paid-plans` — Pricing plans
- `@wix/forum` — Forum/discussions

## Webhooks from Wix
Wix can send webhooks when events happen.

**Setup:** Dashboard → Settings → API Keys → + Create API Key → "Webhooks" section
Or via Wix Automations → Action: "Send a Webhook"

## Custom Code Injection
**Site-wide:** Dashboard → Settings → Custom Code → (+) Add Custom Code
**Options:** Head or Body placement, All/Specific pages, Async/Defer/Sync

**Use cases:** Google Analytics (GA4), Facebook/Meta Pixel, Hotjar, TikTok Pixel, GTM, LinkedIn Insight, Custom fonts, Schema JSON-LD

**GA4 Example:**
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```
