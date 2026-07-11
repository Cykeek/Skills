# Velo by Wix — API Reference

## 1. Enabling Velo
Editor → Top menu → Dev Mode → Enable Dev Mode (opens Code Panel at bottom)

## 2. File Structure
```
Public/
├── myHelper.js          ← reusable frontend functions
└── constants.js         ← shared constants

Pages/
├── home.js              ← code for Home page
├── about.js             ← code for About page
├── masterPage.js        ← runs on every page (site-wide)

Backend/
├── data.js              ← CMS data hooks (before/after operations)
├── http-functions.js    ← REST endpoints (_functions/...)
├── routers.js           ← custom URL routing
├── events.js            ← platform event handlers
├── jobs.config          ← scheduled cron jobs
└── myModule.jsw         ← backend module callable from frontend
```

**Key rule:** `.jsw` files in Backend are callable from frontend. Regular `.js` in Backend are not.

## 3. $w() Selector API

```javascript
$w('#myButton')                  // by element ID
$w('Button')                     // by element type
$w('#btn1, #btn2, #text1')      // multiple IDs
// Inside repeater — MUST use $item:
$w('#myRepeater').onItemReady(($item, itemData) => {
  $item('#itemTitle').text = itemData.title;
});
```

## 4. Common Element Methods
```javascript
// Visibility
element.show(); element.hide(); element.toggle();
element.collapsed = true;   // takes up no space
element.hidden = true;      // still takes up space

// Text
$w('#text1').text = 'New text';
$w('#text1').html = '<em>Italic</em>';

// Inputs
$w('#input1').value;              // get
$w('#input1').value = 'default';  // set
$w('#input1').disable(); $w('#input1').enable();
$w('#input1').valid;              // boolean validation
$w('#input1').validationMessage;

// Images
$w('#img1').src = 'https://...';
$w('#img1').alt = 'description';

// Buttons
$w('#btn1').label = 'Click Me';
$w('#btn1').link = '/about';
$w('#btn1').target = '_blank';

// Repeater
$w('#repeater1').data = [{ _id: '1', title: 'Item 1' }, ...];

// Dropdowns
$w('#dropdown1').options = [{ label: 'A', value: 'a' }, ...];
$w('#dropdown1').value;             // selected value
$w('#dropdown1').selectedIndex;
```

## 5. Event Handlers
```javascript
$w('#myBtn').onClick((event) => { console.log(event.target.id); });
$w('#box1').onMouseIn((event) => { });
$w('#box1').onMouseOut((event) => { });
$w('#textInput').onInput((event) => { console.log(event.target.value); });
$w('#textInput').onChange((event) => { });
$w('#textInput').onKeyPress((event) => { if (event.key === 'Enter') submitForm(); });
$w('#form1').onSubmit((event) => { event.preventDefault(); });
$w('#section1').onViewportEnter((event) => { });
$w('#section1').onViewportLeave((event) => { });
```

## 6. Page Lifecycle
```javascript
// ALWAYS wrap element interactions inside $w.onReady()
$w.onReady(async function () {
  // DOM ready, elements accessible
  await loadData();
  setupEventHandlers();
});
```

## 7. wix-location (Navigation)
```javascript
import wixLocation from 'wix-location';
wixLocation.to('/about');                    // internal page
wixLocation.to('https://google.com');        // external URL
const url = wixLocation.url;                  // full URL
const path = wixLocation.path;               // ['products', 'shoes']
const query = wixLocation.query;             // { category: 'new' }
wixLocation.queryParams.add({ filter: 'price' });
wixLocation.queryParams.remove(['filter']);
wixLocation.onChange((location) => { });
```

## 8. wix-window (Lightbox, Scroll)
```javascript
import wixWindow from 'wix-window';
// Open lightbox with data
wixWindow.openLightbox('MyLightbox', { data: 'hello' });
// Receive lightbox result
const result = await wixWindow.openLightbox('MyLightbox');
// Inside lightbox code:
const ctx = wixWindow.lightbox.getContext();
wixWindow.lightbox.close('result data');
// Scroll
wixWindow.scrollTo(0, 500);
$w('#mySection').scrollTo();
```

## 9. Authentication (wix-members)
```javascript
import { authentication, currentMember, members } from 'wix-members';
const isLoggedIn = authentication.loggedIn();
const member = await currentMember.getMember();
const roles = member.roles;   // array of role objects
await authentication.logout();
// Get profile
const profile = await members.getCurrentMember({ fieldsets: ['FULL'] });
```

## 10. Storage
```javascript
import { local, session, memory } from 'wix-storage';
local.setItem('key', 'value');     // persists across sessions
session.setItem('key', 'value');   // persists in tab session
memory.setItem('key', 'value');    // lost on page refresh
```

## 11. wix-fetch (HTTP Requests from Frontend)
```javascript
import { fetch } from 'wix-fetch';
const response = await fetch('https://api.example.com/data', {
  method: 'GET',
  headers: { 'Authorization': 'Bearer token' }
});
```
> **Security Note:** Never put secret API keys in frontend fetch calls. Use backend `.jsw` modules.

## 12. Backend Web Modules (.jsw)
**Callable from frontend.** Use for API calls, database ops with secrets.

```javascript
// backend/myApi.jsw
import { getSecret } from 'wix-secrets-backend';
import { fetch } from 'wix-fetch';

export async function getWeatherData(city) {
  const apiKey = await getSecret('WEATHER_API_KEY');
  const response = await fetch(`https://api.weather.com/data?q=${city}&appid=${apiKey}`);
  return response.json();
}
```
**Frontend call:**
```javascript
import { getWeatherData } from 'backend/myApi';
const data = await getWeatherData('London');
```

## 13. HTTP Functions (Webhooks / REST Endpoints)
**File:** `backend/http-functions.js`

```javascript
import { ok, badRequest, notFound, serverError } from 'wix-http-functions';
import wixData from 'wix-data';

// GET https://domain.com/_functions/products
export async function get_products(request) {
  const results = await wixData.query('Products').find();
  return ok({ headers: { 'Content-Type': 'application/json' }, body: { products: results.items } });
}

// POST https://domain.com/_functions/submit
export async function post_submit(request) {
  const body = await request.body.json();
  const { name, email } = body;
  if (!name || !email) return badRequest({ body: { error: 'Missing fields' } });
  await wixData.insert('Submissions', { name, email });
  return ok({ body: { message: 'Submitted' } });
}
```
**URL pattern:** `_functions/{methodName}` where method = `get_`, `post_`, `put_`, `delete_`

## 14. Backend Events
**File:** `backend/events.js`

```javascript
export function wixMembers_onMemberCreated(event) { }
export function wixStores_onOrderPaid(event) { }
export function wixBlog_onPostPublished(event) { }
export function wixForms_onFormSubmit(event) { }
export function wixBookings_onBookingConfirmed(event) { }
export function wixPaidPlans_onOrderPurchased(event) { }
```

## 15. Scheduled Jobs (Cron)
**File:** `jobs.config` with job function in a backend `.js` file:
```json
{
  "jobs": [{
    "functionLocation": "/myJobs",
    "functionName": "cleanupExpiredSessions",
    "executionConfig": { "cronExpression": "0 2 * * *" }
  }]
}
```
Cron format: `second minute hour day month weekday`

## 16. Secrets Manager
**Add secret:** Dashboard → Dev Tools → Secrets Manager → (+) New Secret
**Use in backend only:**
```javascript
import { getSecret } from 'wix-secrets-backend';
const apiKey = await getSecret('MY_API_KEY');
```

## 17. Wix Pay (Frontend Payment)
```javascript
import wixPay from 'wix-pay';
import { createPayment } from 'backend/payments';

$w('#payBtn').onClick(async () => {
  const payment = await createPayment({ amount: 99.99, currency: 'USD', items: [...] });
  const result = await wixPay.startPayment(payment.id);
  if (result.status === 'Successful') wixLocation.to('/thank-you');
});
```

## 18. Repeater Best Practices
- Always use `$item` (not `$w`) inside `onItemReady` — it scopes to the current repeater item
- For large datasets (100+ items), use pagination — repeaters get slow with many items
- Set data programmatically: `$w('#myRepeater').data = [items]`
```javascript
$w('#myRepeater').onItemReady(($item, itemData, index) => {
  $item('#itemTitle').text = itemData.title;
  $item('#itemBtn').onClick(() => { console.log('Clicked:', itemData._id); });
});
```

## 19. Error Handling
```javascript
async function safeDataFetch(collectionName, filter) {
  try {
    const results = await wixData.query(collectionName).eq(...filter).find();
    return { success: true, data: results.items };
  } catch (error) {
    console.error(`[Error] ${collectionName}:`, error);
    if (error.code === 'WDE0095') return { success: false, error: 'Collection not found' };
    if (error.code === 'WDE0025') return { success: false, error: 'Permission denied' };
    return { success: false, error: error.message };
  }
}
```

## 20. Custom Router (Velo Routing)
**File:** `backend/routers.js`
```javascript
import { ok, notFound, redirect } from 'wix-router';
import wixData from 'wix-data';

export async function catalog_Router(request) {
  const slug = request.path[0];
  if (!slug) return ok('catalog-list', { title: 'All Products' });
  const result = await wixData.query('Products').eq('slug', slug).find();
  if (result.items.length === 0) return notFound();
  return ok('catalog-item', { product: result.items[0] }, {
    seoData: { title: result.items[0].name, description: result.items[0].shortDescription }
  });
}
```

## 21. HTML iFrame ↔ Wix Communication
**Inside iFrame:**
```html
<script>
  window.parent.postMessage({ type: 'buttonClicked', data: 'value' }, '*');
  window.addEventListener('message', (event) => {
    if (event.data.type === 'updateColor') document.body.style.background = event.data.color;
  });
</script>
```
**In Wix Velo:**
```javascript
$w('#htmlEmbed').onMessage((event) => { console.log(event.data); });
$w('#htmlEmbed').postMessage({ type: 'updateColor', color: '#ff0000' });
```

## 22. Multi-Step Form Pattern
```javascript
let currentStep = 1;
const formData = {};
$w.onReady(() => {
  showStep(1);
  $w('#nextBtn').onClick(() => { if (validateCurrentStep()) { collectStepData(); currentStep++; showStep(currentStep); } });
  $w('#prevBtn').onClick(() => { currentStep--; showStep(currentStep); });
  $w('#submitBtn').onClick(async () => { await submitAllData(formData); $w('#successMsg').show(); });
});
function showStep(step) {
  $w('#step1, #step2, #step3').hide();
  $w(`#step${step}`).show();
  $w('#prevBtn').toggle(step > 1);
  $w('#nextBtn').toggle(step < 3);
  $w('#submitBtn').toggle(step === 3);
}
```

## 23. Performance Optimization in Velo
```javascript
// Lazy load content on scroll
$w('#section1').onViewportEnter(async () => {
  if (!$w('#section1').data) {
    const data = await fetchHeavyData();
    populateSection(data);
  }
});

// Code splitting — load module only when needed
$w('#analyticsTab').onClick(async () => {
  const { renderChart } = await import('backend/chartBuilder');
  renderChart(await getChartData());
});
```

## 24. Common Velo Errors
| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot read property 'X' of undefined` | Element not found or data null | Check element ID; add null check |
| `$w is not a function` | Using $w before onReady | Wrap in `$w.onReady()` |
| `Permission denied` | CMS permissions | Check collection permissions |
| `Module not found: 'backend/X'` | Typo in import path | Verify filename + path |
| `Maximum call stack exceeded` | Infinite recursion | Add base case to recursive function |
| `CORS error` | API call from frontend | Move to backend `.jsw` |
| `Unexpected token in JSON` | API returned HTML error | Log `response.text()` first |

## 25. Velo SDK Modules (@wix/*) — Newer Pattern
```javascript
import { products } from '@wix/stores';
import { orders } from '@wix/ecom';
import { members } from '@wix/members';
import { items } from '@wix/data';   // CMS SDK
import { blog } from '@wix/blog';
import { bookings } from '@wix/bookings';

// Query products
const { items: productItems } = await products.queryProducts().eq('visible', true).find();

// CMS operations via SDK
const { dataItems } = await items.queryDataItems({ collectionId: 'my-collection' });
const { dataItem } = await items.createDataItem({ collectionId: 'my-collection', dataItem: { title: 'New' } });

// Blog operations
const { posts } = await blog.listPosts({ limit: 10, sort: { field: 'publishedDate', order: 'DESC' } });
```

**Available SDK modules:** `@wix/stores`, `@wix/ecom`, `@wix/members`, `@wix/blog`, `@wix/bookings`, `@wix/events`, `@wix/data`, `@wix/redirects`, `@wix/media`, `@wix/seo`, `@wix/paid-plans`, `@wix/forum`

> Classic `wix-*` imports still work. New code should prefer `@wix/*` SDK where available.
