# Wix CMS — Reference

## 1. What It Is
The Wix CMS (Content Manager / Wix Data) is a built-in database. It stores structured content, auto-generates dynamic pages, and connects data to page elements.

**Access:** Dashboard → Content Manager | Editor → Left Panel → CMS | Velo: `import wixData from 'wix-data'`

## 2. Collections
A collection is a database table. Each has a name, fields (columns), and records (rows).

**Built-in collections:** `Blog/Posts`, `Stores/Products`, `Bookings/Services`, `Events/Events`

**Custom collections:** Create your own for any data.

### Collection Relationships (Enhanced 2024+)
- **Reference fields**: Link records between collections (one-to-many)
- **Multi-reference fields**: Many-to-many relationships
- **Reverse references**: Automatically see what references an item
- **Rollup fields**: Aggregate data from referenced collections (e.g., sum of order totals from a customer)
- **Formula fields**: Compute values from other fields (e.g., `price * quantity`)
- **Optimistic Concurrency Control**: Version-based conflict detection via `_updatedDate`

## 3. Field Types
| Type | Description | Velo Type |
|------|-------------|-----------|
| Text | Short string | `string` |
| Rich Text | HTML-formatted | `string` (HTML) |
| Number | Integer/decimal | `number` |
| Boolean | True/False | `boolean` |
| Date & Time | Date/time/datetime | `Date` |
| Image | Wix Media URL | `string` |
| Image Gallery | Multiple images | `Array` |
| Video/Audio/Document | Media URLs | `string` / `object` |
| URL/Email/Phone | Contact fields | `string` |
| Address | Structured address | `object` |
| Reference | Link to one item | `string` (ID) |
| Multi-Reference | Link to multiple items | `Array` of IDs |
| Tags / Array | Arrays of values | `Array<string>` |
| **Color** (new) | Hex color | `string` |
| **Formula** (new) | Computed field | Computed |
| **Rollup** (new) | Aggregate from references | Computed |
| **Single Select** (new) | Dropdown, one value | `string` |
| **Multi Select** (new) | Dropdown, multiple values | `Array<string>` |

## 4. Collection Permissions
| Role | Read | Write |
|------|------|-------|
| Anyone | Public read | Public write (not recommended) |
| Signed-in member | Members only | Members only |
| Content author | Own items | Own items |
| Admin only | Admin | Admin |
| Custom | Custom roles | Custom roles |

Set at: Dashboard → CMS → select collection → Settings → Permissions

## 5. Dataset Element
Bridges CMS collections to page elements. Non-visual component.

**Add:** Editor → Add → CMS → Dataset (auto-added on dynamic pages)

**Settings:**
- **Collection**: Which collection to connect
- **Mode**: Read-only, Write-only, or Read & Write
- **Filter**: Pre-filter records
- **Sort**: Default sort order
- **Page size**: Items per page
- **Current Item**: For dynamic pages
- **Real-time updates** (2024+): Auto-refresh on data change
- **Debounced search** (2024+): Built-in search filtering

**Bind elements:** Select element → Right-click → Connect to CMS → Choose field

**Enhanced 2024+:**
- Connected collections (multiple related collections)
- Computed bindings (formula/rollup fields)
- Conditional formatting (appearance based on data)
- Inline editing (edit CMS data directly on page)

## 6. Dynamic Pages
Pages auto-generated from CMS collection items.

**Create:** CMS → open collection → "Create Dynamic Page"

**URL pattern:** `/{collection-name}/{field-value}` (configurable slug)

**List vs Item page:**
- **List page** → `/blog` (shows ALL items)
- **Item page** → `/blog/my-post` (ONE item based on slug)

**⚠️ CRITICAL: The "Dynamic Page 404" Trap**
If a dynamic item page returns 404 on live but works in Editor:
1. In Editor, check Dynamic Page Dataset → "Pages Generated" count
2. If count < total items in collection → a **Filter** is applied
3. Open Dataset → Settings → Remove all filters → Publish

## 7. Querying CMS Data (wix-data)
```javascript
import wixData from 'wix-data';

// Basic query
const results = await wixData.query('MyCollection').find();

// Filtered query
const filtered = await wixData.query('Products')
  .eq('category', 'Electronics')
  .gt('price', 100)
  .contains('name', 'wireless')
  .hasSome('tags', ['sale', 'new'])
  .ascending('name')
  .limit(20)
  .skip(40)
  .find();

// Get by ID
const item = await wixData.get('Products', itemId);

// Insert / Update / Remove
await wixData.insert('MyCollection', { title: 'New' });
await wixData.update('MyCollection', { _id: 'id', title: 'Updated' });
await wixData.remove('MyCollection', id);

// Bulk operations
await wixData.bulkInsert('MyCollection', [item1, item2]);
await wixData.bulkUpdate('MyCollection', [item1, item2]);
await wixData.bulkRemove('MyCollection', [id1, id2]);
```

## 8. Query Operators Reference
| Operator | Method |
|----------|--------|
| Equals | `.eq(field, value)` |
| Not equals | `.ne(field, value)` |
| Greater than | `.gt(field, value)` |
| >= | `.ge(field, value)` |
| Less than | `.lt(field, value)` |
| <= | `.le(field, value)` |
| Contains | `.contains(field, value)` |
| Starts with | `.startsWith(field, value)` |
| Has any of | `.hasSome(field, [values])` |
| Has all of | `.hasAll(field, [values])` |
| Is empty | `.isEmpty(field)` |
| Is not empty | `.isNotEmpty(field)` |
| Ascending | `.ascending(field)` |
| Descending | `.descending(field)` |
| Limit | `.limit(n)` |
| Skip | `.skip(n)` |

## 9. References & Joins
```javascript
const results = await wixData.query('Articles')
  .include('author')  // 'author' is reference field → 'Authors' collection
  .find();
// results.items[0].author = full referenced object, not just ID
```

## 10. CMS Data Hooks
**File:** `backend/data.js` — runs before/after CMS operations.

```javascript
export function MyCollection_beforeInsert(item, context) {
  item.createdAt = new Date();
  item.slug = item.title.toLowerCase().replace(/\s+/g, '-');
  return item;
}
export function MyCollection_afterInsert(item, context) {
  // Send email, trigger automation, etc.
  return item;
}
```

Available hooks: `_beforeGet`, `_afterGet`, `_beforeInsert`, `_afterInsert`, `_beforeUpdate`, `_afterUpdate`, `_beforeRemove`, `_afterRemove`, `_beforeQuery`, `_afterQuery`, `_beforeBulkInsert`, `_afterBulkInsert`, `_beforeBulkUpdate`, `_afterBulkUpdate`, `_beforeBulkRemove`, `_afterBulkRemove`

## 11. Dynamic Page SEO with Velo
```javascript
import wixSeo from 'wix-seo';

wixSeo.setTitle(`${product.name} - My Store`);
wixSeo.setDescription(product.shortDescription);
wixSeo.setLinks([{ rel: 'canonical', href: `https://mysite.com/products/${product.slug}` }]);
wixSeo.setStructuredData([{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": product.name,
  "description": product.description,
  "image": product.mainImage,
  "offers": { "@type": "Offer", "price": product.price, "priceCurrency": "USD" }
}]);
```

## 12. Sandbox vs. Live
- CMS has **two environments**: Sandbox (dev) and Live (production)
- Schema changes (fields, collections) made in editor → Sandbox
- Must **"Sync to Live"** to move schema changes to production
- Content added in editor → Sandbox; content added in Dashboard → Live
**Path:** Editor → CMS panel → "Sync to Live"

## 13. Troubleshooting CMS Issues
**Data not showing on page:**
1. Dataset connected to correct collection?
2. Dataset mode = Read or Read & Write?
3. Filters filtering out data?
4. Collection permissions allow read for user role?
5. Page in Preview (live data) vs Sandbox (sandbox data)?
6. CMS synced to Live?

**Known CMS bugs:**
| Bug | Workaround |
|-----|-----------|
| Dataset loads after page paint (FOUC) | Hide elements initially, show after data loads in `$w.onReady()` |
| Rich text formatting lost on update | Test round-trips; update carefully |
| Multi-reference fields slow to query | Use `.include()` sparingly; consider denormalization |
| Dynamic page 404 after slug change | Update references; clear sitemap cache |
| Formula fields not auto-updating | Manually trigger via Velo or edit dependent fields |
| Image returns placeholder | Ensure uploaded to Wix Media, not external URL |
