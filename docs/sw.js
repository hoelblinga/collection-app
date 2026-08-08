const CACHE_NAME = 'collection-app-v2';
const ASSETS = ['./', './index.html', './manifest.json', './icon.svg'];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)).catch(()=>{})
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))
  );
  self.clients.claim();
});

// Network-first: liefert immer die aktuelle Version, wenn online, und
// aktualisiert dabei den Cache. Nur offline greift der zuletzt gecachte
// Stand. Verhindert, dass nach einem neuen Deploy dauerhaft eine alte
// gecachte Version ausgeliefert wird.
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  // API-Aufrufe (Sammlungsdaten) nie aus dem Cache beantworten, immer live vom Server.
  if(url.pathname.startsWith('/api/')){
    return;
  }
  event.respondWith(
    fetch(event.request)
      .then(res => {
        const resClone = res.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, resClone)).catch(()=>{});
        return res;
      })
      .catch(() => caches.match(event.request))
  );
});
