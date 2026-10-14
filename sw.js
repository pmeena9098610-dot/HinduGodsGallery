const CACHE_NAME = 'hindu-gods-v8';
const ASSETS = [
  './',
  'index.html',
  'manifest.json',
  'favicon.png',
  'feed.xml',
  'sitemap.xml',
  'sitemap-images.xml',
  'images/cute_radha_krishna.webp',
  'images/cute_bal_shiva.webp',
  'images/cute_bal_hanuman.webp',
  'images/cute_krishna_makhan.webp',
  'images/cute_baby_lakshmi.webp',
  'images/cute_ganesha_reading.webp',
  'images/cute_baby_saraswati.webp',
  'hanuman-chalisa.html',
  'shiv-aarti.html',
  'ganesh-aarti.html',
  'lakshmi-aarti.html',
  'durga-aarti.html',
  'ram-stuti.html',
  'shubh-prabhat.html',
  'festivals-2026.html',
  'category-cute.html',
  'category-trending.html',
  'category-festival.html',
  'category-vishnu.html',
  'about.html',
  'contact.html',
  'privacy-policy.html',
  'terms.html',
  'disclaimer.html'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Cache-First with Stale-While-Revalidate for images
self.addEventListener('fetch', event => {
  if (event.request.destination === 'image') {
    event.respondWith(
      caches.match(event.request).then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(response => {
          if (response && response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        });
      })
    );
  } else {
    event.respondWith(
      caches.match(event.request).then(cached => cached || fetch(event.request))
    );
  }
});
