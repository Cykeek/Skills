# Debugging & Known Bugs — Reference

## Velo Debugging Tools

### Browser Console
Preview site → F12 → Console. All `console.log()` from frontend Velo appears here.

### Velo Console
Editor with Dev Mode on → bottom panel shows console output in preview mode.

### Backend Logs
Dashboard → Dev Tools → Logs

### Velo Inspector (2024+)
Dashboard → Dev Tools → Velo Inspector
- Inspect element IDs, datasets, variables in real-time
- View CMS query results and API responses
- Monitor Velo function performance
- Debug authentication state

### Velo Network Panel (2024+)
- View all API requests made by Velo code
- See request/response payloads in real-time
- Filter by collection, service, endpoint type
- Identify slow queries and failed requests

### Error Tracking Dashboard (2024+)
Dashboard → Dev Tools → Error Logs
Frontend + backend errors in one place. Error grouping by type and frequency.

## Debugging CMS Issues

**Data not showing:**
1. Dataset connected to correct collection?
2. Dataset mode = Read or Read & Write?
3. Filters filtering out data?
4. Collection permissions allow read?
5. Preview (live data) vs Sandbox (sandbox data)?
6. CMS synced to Live?

**⚠️ The "Dynamic Page 404" Trap (High Priority)**
If a dynamic item page returns 404 on live but works in Editor:
- Check Dataset → "Pages Generated" count
- If count < total items → **a Filter is applied**
- Fix: Open Dataset → Settings → Remove all filters → Publish

**Sandbox vs. Live:**
- Schema changes in editor → Sandbox
- Must "Sync to Live" to move to production
- Content in editor → Sandbox; content in Dashboard → Live

## Debugging Mobile Layout

1. Enter Mobile Editor (Classic) or Mobile breakpoint (Studio)
2. Check for overlapping → rearrange
3. Elements hidden but still taking space → use "Collapse" not just "Hide"
4. Fixed-width elements wider than 320-375px?
5. Text wrapping correctly?

## Performance Debugging

**Wix Site Speed Dashboard:** Dashboard → Marketing & SEO → Site Speed
Shows Core Web Vitals performance.

**Page-level issues:**
- Too many images above the fold → lazy load or reduce
- Heavy Velo in `$w.onReady()` → defer non-critical
- Too many installed apps → each adds JS overhead

## Payment & Checkout Debugging

| Issue | Check |
|-------|-------|
| Payment not processing | Provider connected? Not in test mode? SSL? |
| Tax not calculating | Tax settings configured? |
| Shipping not showing | Zones include customer's country? |
| Cart not appearing | Wix Stores installed and active? |
| Discount code not applying | Code active? Not expired? Meets minimum? |
| Abandoned cart not sending | Check it's enabled in Store → Marketing |

## Domain Debugging

**Domain not working:**
1. Wait up to 48 hours for DNS propagation
2. Verify DNS records at registrar match Wix specs
3. Clear browser cache + try incognito
4. Use https://dnschecker.org to verify globally
5. Ensure no conflicting A records
6. SSL: auto-provisioned after DNS, can take 24h more
7. Still broken after 48h → escalate to Wix Support

---

## Known Bugs & Limitations

### Classic Editor Limitations
| Limitation | Workaround |
|-----------|------------|
| Not truly responsive | Use Wix Studio for new projects |
| Mobile editor must be managed separately | Always check mobile after desktop changes |
| Max 100 pages per site | Combine content using CMS dynamic pages |
| Z-index limited to same container level | Reorganize elements into same container |
| Can't overlay text on gallery natively | Use HTML embed or absolute positioning |
| Custom fonts limited to Google Fonts | Upload via Dashboard → Upload Fonts |

### Wix Studio Limitations
| Limitation | Workaround |
|-----------|------------|
| Classic sites can't auto-convert to Studio | Build from scratch in Studio |
| Some classic widgets not in Studio | Use HTML embed as alternative |
| Grid doesn't support irregular cell spanning easily | Use nested grids or custom CSS grid |
| Components not shareable between sites | Use site duplication or template sharing |
| No full CSS Grid Area naming | Use numbered grid lines or nested layouts |
| AI-generated content needs review | Always proofread before publishing |

### Velo Limitations (Including 2024+)
| Limitation | Workaround |
|-----------|------------|
| Frontend can't access secrets | Use `.jsw` backend module |
| HTTP functions only on paid plans | Upgrade or use third-party webhook service |
| No SSR for Velo pages | Pre-render with static data where possible |
| npm package support limited | Check whitelist; use native APIs |
| wix-realtime connection limits | Use sparingly; batch updates |
| Backend cold starts (1-2s) | First call after inactivity may be slow |
| Max backend execution 14 seconds | Split heavy operations |
| Dynamic page count limit ~10,000 | Use pagination or router pages |
| No WebSocket support | Use polling or wix-realtime |
| File upload max 25MB | Compress before upload |
| No TypeScript support (2025) | Use JS with JSDoc type annotations |

### CMS Known Bugs
| Bug | Workaround |
|-----|-----------|
| Dataset loads after page paint (FOUC) | Hide initially, show after `$w.onReady()` data loads |
| Rich text formatting lost on update | Test round-trips; update carefully |
| Multi-reference fields slow to query | Use `.include()` sparingly; denormalize |
| Sandbox changes lost if not synced | Sync to Live immediately after schema changes |
| Dynamic page 404 after slug change | Update references; clear sitemap cache |
| Formula fields not auto-updating | Trigger via Velo or edit dependent fields |
| CMS image shows placeholder | Upload to Wix Media, not external URL |

### eCommerce Known Bugs
| Bug | Workaround |
|-----|-----------|
| Cart badge not updating instantly | Refresh or `cart.onChange()` listener |
| Product options not saving | Re-save product after setting |
| Refund not restoring inventory | Manually adjust inventory |
| PayPal failing in some countries | Try Wix Payments |
| Tax-inclusive price not in checkout | Confirm settings, restart checkout |
| Abandoned cart email not triggering | Verify enabled in Store → Marketing |
| Multi-currency display inconsistent | Verify per-product settings |
| Discount stacking uncontrolled | Use separate promotion periods |

### SEO Known Issues
| Issue | Fix |
|-------|-----|
| Page not indexed | Verify "Index" ON; submit to GSC |
| OG image not updating | Use Facebook/Twitter debug tools to refresh cache |
| Structured data errors | Google Rich Results Test; fix schema |
| Multilingual duplicate content | hreflang auto-set by Wix Multilingual |
