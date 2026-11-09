/* Google Analytics, loaded only after the visitor says yes.
   Nothing is sent to Google before that, and nothing at all while GA_ID is still the placeholder.
   The choice is kept in localStorage; "Cookie settings" in the footer asks again. */
(function () {
  var GA_ID = "G-CKH9K1EJZM"; // GA4 measurement ID of the zweikarta.com web stream
  var KEY = "zk-analytics-consent"; // "yes" or "no"
  if (!/^G-[A-Z0-9]+$/.test(GA_ID) || GA_ID === "G-XXXXXXXXXX") return;

  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  function loadGA() {
    if (window.gtag) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("consent", "default", { analytics_storage: "granted", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied" });
    gtag("js", new Date());
    gtag("config", GA_ID, { allow_google_signals: false, allow_ad_personalization_signals: false });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
  }

  function clearGA() {
    document.cookie.split(";").forEach(function (c) {
      var name = c.split("=")[0].trim();
      if (name.indexOf("_ga") === 0) {
        ["", "; domain=" + location.hostname, "; domain=." + location.hostname.replace(/^www\./, "")].forEach(function (d) {
          document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/" + d;
        });
      }
    });
  }

  var css =
    ".zk-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:1000;max-width:34rem;margin:0 auto;" +
    "background:#11141B;color:#F2F3F7;border-radius:18px;padding:18px 20px;box-shadow:0 10px 40px rgba(0,0,0,.3);" +
    "font:15px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif}" +
    ".zk-consent p{margin:0 0 14px}.zk-consent a{color:inherit}" +
    ".zk-consent .zk-row{display:flex;gap:10px;flex-wrap:wrap}" +
    ".zk-consent button{flex:1 1 8rem;font:inherit;font-weight:600;border:0;border-radius:999px;padding:10px 16px;cursor:pointer;" +
    "background:#F2F3F7;color:#11141B}" +
    ".zk-consent button:focus-visible{outline:2px solid #FFAE2B;outline-offset:3px}";

  function banner() {
    if (document.querySelector(".zk-consent")) return;
    if (!document.getElementById("zk-consent-css")) {
      var st = document.createElement("style");
      st.id = "zk-consent-css";
      st.textContent = css;
      document.head.appendChild(st);
    }
    var box = document.createElement("div");
    box.className = "zk-consent";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-label", "Analytics cookies");
    box.innerHTML =
      '<p>May we use Google Analytics cookies to count visits and see which pages help? ' +
      'No ads, and you can change your mind any time. <a href="/privacy/">Details</a></p>' +
      '<div class="zk-row"><button type="button" data-v="no">No thanks</button>' +
      '<button type="button" data-v="yes">Allow analytics</button></div>';
    box.addEventListener("click", function (e) {
      var v = e.target.getAttribute && e.target.getAttribute("data-v");
      if (!v) return;
      var was = get();
      set(v);
      box.remove();
      if (v === "yes") loadGA();
      else if (was === "yes") { clearGA(); location.reload(); }
    });
    document.body.appendChild(box);
  }

  function settingsLink() {
    var nav = document.querySelector('footer nav[aria-label="Legal"]');
    if (!nav) return;
    var a = document.createElement("a");
    a.href = "#";
    a.textContent = "Cookie settings";
    a.addEventListener("click", function (e) { e.preventDefault(); banner(); });
    nav.appendChild(a);
  }

  /* Store buttons. Each App Store link carries ?ct=<page> (an App Store campaign token), so
     App Store Connect can show which page sent the visit. With consent, a click also sends a
     "store_click" event to GA, so GA shows which page and post led to the store. */
  var PROVIDER_TOKEN = ""; // App Store Connect › Analytics › Campaigns › "pt" value. Empty = leave links as they are.

  function storeOf(a) {
    if (/apps\.apple\.com/.test(a.hostname)) return "app_store";
    if (/play\.google\.com/.test(a.hostname)) return "google_play";
    return "";
  }

  function addProviderToken() {
    if (!PROVIDER_TOKEN) return;
    document.querySelectorAll('a[href*="apps.apple.com"]').forEach(function (a) {
      try {
        var u = new URL(a.href);
        if (!u.searchParams.get("pt")) { u.searchParams.set("pt", PROVIDER_TOKEN); a.href = u.toString(); }
      } catch (e) {}
    });
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a || !window.gtag) return;
    var store = storeOf(a);
    if (!store) return;
    var ct = "";
    try { ct = new URL(a.href).searchParams.get("ct") || ""; } catch (err) {}
    gtag("event", "store_click", {
      store: store,
      campaign: ct,
      link_text: (a.textContent || "").trim().slice(0, 100),
      transport_type: "beacon"
    });
  }, true);

  var choice = get();
  if (choice === "yes") loadGA();
  function ready() {
    addProviderToken();
    settingsLink();
    if (choice !== "yes" && choice !== "no") banner();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ready);
  else ready();
})();
