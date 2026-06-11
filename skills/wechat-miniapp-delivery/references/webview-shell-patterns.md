# WebView Shell Patterns

Use this reference when the miniapp is a thin native shell that loads its core business logic inside a `<web-view>` component pointing at an external H5 application. This is a fundamentally different architecture from native-page miniapps and requires its own delivery, testing, and release considerations.

## Identify A WebView Shell Project

Look for most of these signals together:
- Very few native pages, typically an entry page, a `web-view` container page, and an error fallback page.
- A `<web-view src={url}>` component that loads an external H5 URL.
- An H5 application in the same monorepo or a separate repo that provides the actual UI.
- A bridge layer that handles `postMessage` communication between the H5 and the miniapp.
- A URL validator or allowlist that restricts which domains the WebView can load.

If the project has many native pages with native components, it is not a WebView shell project even if it uses `<web-view>` on one or two pages.

## Architecture Overview

```
miniapp (native shell)
  pages/
    index/       -- entry, redirects to webview
    webview/     -- <web-view src={h5Url}> container
    error/       -- fallback when H5 fails to load

  bridge/
    dispatcher   -- routes postMessage from H5 to handlers
    handlers     -- implements native capabilities (navigation, share, storage, etc.)
    types        -- message type definitions shared between H5 and miniapp

  config/
    index        -- H5 base URL, allowed hosts, debug flags

  lib/
    url-validator -- validates URLs against the allowlist before loading

H5 app (runs inside web-view)
  -- full business logic, UI, routing
  -- communicates with miniapp via wx.miniProgram.postMessage / navigateTo
```

## H5 URL Configuration

The H5 base URL is typically injected at build time through framework constants such as Taro `defineConstants`.

Common pattern:
- Development: `http://localhost:<port>` for local H5 dev server.
- Production: `https://<h5-domain>` for the deployed H5.

### Critical preflight check

Verify that the production build script sets `NODE_ENV=production` or an equivalent flag so the H5 URL resolves to the production domain. Frameworks like Taro do not set `NODE_ENV` automatically in build commands. A missing `NODE_ENV=production` in the build script is a common cause of the trial or preview version still pointing at `localhost`.

Verify by inspecting the `build:weapp` script in `package.json`:
- Correct: `"build:weapp": "NODE_ENV=production taro build --type weapp"`
- Wrong: `"build:weapp": "taro build --type weapp"` (falls back to dev URL)

## Bridge Communication

The `postMessage` bridge is the only communication channel between H5 and the miniapp shell. Delivery work that touches the bridge must verify:
- Message type definitions are consistent on both sides.
- The dispatcher correctly routes new message types to their handlers.
- Handlers that invoke native APIs (such as `Taro.navigateTo`, `wx.chooseImage`, `wx.getLocation`) handle errors and permission denials gracefully.
- The H5 side does not assume the bridge is available outside the miniapp context. Feature detection is required when the same H5 runs in a browser.

## URL Security

WebView shell projects must validate every URL before loading it in the `<web-view>`. The URL validator should:
- Parse the URL and extract the hostname.
- Check the hostname against a static allowlist.
- Reject URLs with unexpected protocols such as `javascript:` or `data:`.
- Reject URLs that do not match any allowed host.

The allowlist should include:
- The production H5 domain.
- `localhost` and `127.0.0.1` for development only, controlled by a debug flag.

Never allow arbitrary URLs in the WebView. A missing or weak URL validator is a security risk that can lead to phishing or data theft.

## WeChat WebView CSS Compatibility

The rendering engine inside WeChat `<web-view>` is **not a standard browser**. It has significant CSS compatibility gaps that will silently break styling. These are different from native miniapp CSS restrictions.

### Known incompatible features

| CSS feature | Symptom | Fix |
| --- | --- | --- |
| `@layer` (Cascade Layers) | WebView discards the entire `@layer` block as an unrecognized at-rule. All rules inside are lost. Tailwind CSS v4 wraps everything in `@layer`, so the entire stylesheet disappears. | Use `postcss-layer-unwrap` to strip `@layer` wrappers at build time. Never remove this plugin once added. |
| `oklch()` color function | Colors render as transparent or fallback to black. | Use a PostCSS plugin to downgrade `oklch()` to `hsl()` or `rgb()` equivalents. |
| CSS Nesting (`& .child {}`) | Ignored by the WebView engine. Nested rules have no effect. | Use PostCSS nesting plugin to flatten, or write flat selectors. |
| `:has()` pseudo-class | Not supported. Selectors using `:has()` are dropped entirely. | Rewrite with JavaScript or restructure the markup. |
| `@container` queries | Not recognized. Rules inside are discarded. | Use media queries or JavaScript-based responsive logic. |
| `@property` definitions | Ignored. Custom property type hints and initial values do not work. | Define custom properties with fallback values in `:root`. |

### PostCSS pipeline for WebView compatibility

The H5 app must include PostCSS plugins that strip or downgrade incompatible CSS at build time. A typical pipeline:

```js
// postcss.config.js
export default {
  plugins: {
    "postcss-layer-unwrap": {},           // strip @layer
    "@tailwindcss/postcss": {},           // Tailwind (after layer unwrap)
    "postcss-oklch-fallback": {},         // oklch -> hsl/rgb
    // ... other plugins
  },
}
```

**Never remove the `postcss-layer-unwrap` plugin** if the H5 uses Tailwind CSS v4 and is loaded in a WeChat WebView. Without it, the entire stylesheet is silently discarded.

### Testing CSS compatibility

Before introducing any new CSS feature in the H5:
1. Check the feature on [caniuse.com](https://caniuse.com) for the WeChat WebView engine (based on the system WebView, not Chrome).
2. Test in the WeChat Developer Tools simulator, but also verify on a real device. The simulator uses a different rendering engine.
3. If unsure, add a PostCSS fallback plugin rather than assuming support.

## WeChat Admin Console Configuration

WebView shell projects require specific configuration in the WeChat miniapp admin console. Missing configuration will cause the WebView to show a blank page or refuse to load.

### Domain verification

Before the WebView can load an H5 URL, the domain must be registered as a business domain in the admin console:
1. Download the verification file from the admin console.
2. Place the file in the H5 project's `public/` directory (for Vite/webpack projects) so it is served at the domain root after deployment.
3. Deploy the H5 so the file is accessible at `https://<h5-domain>/<verification-file>.txt`.
4. Complete verification in the admin console.

### Required domain settings

| Setting | Purpose | Where to configure |
| --- | --- | --- |
| Business domain (业务域名) | Domains that `<web-view>` is allowed to load | Admin console > Development > Development settings |
| Server domain (服务器域名) | API endpoints the miniapp or H5 can call via `wx.request` | Admin console > Development > Development settings |
| Request domain (request 合法域名) | HTTPS domains for `wx.request` | Subset of server domains |

### Privacy settings

If the H5 collects user data through the WebView, the miniapp's privacy declaration must cover those data types even though the collection happens in the H5 layer. WeChat considers WebView data collection as part of the miniapp.

## Development Workflow

WebView shell development requires running two services simultaneously:
- The H5 dev server (typically `localhost:3000` or similar).
- The miniapp dev build in watch mode (such as `taro build --type weapp --watch`).

### Preflight for local development

- Verify the H5 dev server is running and accessible at the configured URL.
- Verify the miniapp config points to the correct local H5 URL.
- Set `urlCheck: false` in `project.private.config.json` during development to allow `localhost` in the WebView.
- Verify the bridge works by testing a `postMessage` round-trip.

### Debugging

- Inject `vConsole` into the H5 when running in debug mode to inspect logs, network requests, and storage inside the WebView.
- Use the debug flag in the miniapp config to control vConsole injection automatically: append `?vconsole` or a similar query parameter to the H5 URL.
- Use the WeChat Developer Tools "Remote Debug" feature for real-device WebView inspection.

## Delivery Considerations

### What changes require a miniapp release

- Changes to native pages (index, webview, error).
- Changes to the bridge layer (new message types, handler logic).
- Changes to the URL allowlist or H5 base URL.
- Changes to `project.config.json` or miniapp permissions.
- Taro or framework version upgrades.

### What changes only require an H5 deployment

- Business logic, UI, and routing changes within the H5.
- API integration changes handled entirely in the H5.
- Style and content updates.

This distinction is a major advantage of the WebView shell architecture: most feature work can be shipped by deploying the H5 alone, without going through the miniapp review process.

### Release coordination

When a change requires both a miniapp release and an H5 deployment:
1. Deploy the H5 first so the new version is live.
2. Upload and release the miniapp that depends on the new H5 features.
3. Verify backward compatibility: the new H5 should work with the current production miniapp version during the review period.

## Example Requests

### Adding a native capability via bridge

User says: "Add a share-to-timeline feature that the H5 triggers via postMessage."

- Add a new message type to `bridge/types.ts`.
- Add a handler in `bridge/handlers.ts` that calls `wx.updateShareMenu` or the equivalent API.
- Update the dispatcher to route the new message type.
- Add the corresponding `postMessage` call in the H5.
- Test the round-trip in WeChat Developer Tools.
- This change requires a miniapp release.

### Fixing a WebView blank screen

User says: "The WebView shows a blank page in production."

- Check if the H5 domain is registered as a business domain in the admin console.
- Check if the domain verification file is deployed and accessible.
- Check if the H5 CSS is being stripped by the WebView engine (common with Tailwind v4 and `@layer`).
- Check the PostCSS pipeline for missing compatibility plugins.
- Check the build script for missing `NODE_ENV=production`.
