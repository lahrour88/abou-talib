// static/sw.js

const CACHE_NAME = 'abou-talib-cache-v2';
const ASSETS = [
  '/',
  'templates/appbare.html'
  'templates/note.html'
  'templates/footer.html'
  '/static/manifest.json',
  '/static/offline.html',
  '/static/css/bootstrap.min.css',
  '/static/css/bootstrap-icons.css',
  '/static/css/main.css',
  '/static/css/templatemo-topic-listing.css',
  '/static/js/bootstrap.bundle.min.js',
  '/static/js/jquery.min.js',
  '/static/js/script.js',
  '/static/images/favicon.ico',
  '/static/android-chrome-192x192.png',
  '/static/android-chrome-512x512.png'
];

// تثبيت Service Worker وتخزين الملفات
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

// تفعيل Service Worker وحذف الكاش القديم
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

// اعتراض الطلبات
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return (
        response ||
        fetch(event.request).catch(() => caches.match('/static/offline.html'))
      );
    })
  );
});