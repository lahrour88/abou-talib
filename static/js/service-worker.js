// This file handles the service worker for the PWA, managing caching and offline functionality.

const CACHE_NAME = 'v1';
const CACHE_ASSETS = [
    '/',
    '/static/css/bootstrap.min.css',
    '/static/css/bootstrap-icons.css',
    '/static/css/main.css',
    '/static/css/templatemo-topic-listing.css',
    '/static/js/bootstrap.bundle.min.js',
    '/static/js/click-scroll.js',
    '/static/js/custom.js',
    '/static/js/jquery.min.js',
    '/static/js/jquery.sticky.js',
    '/static/js/script.js',
    '/static/images/businesswoman-using-tablet-analysis.jpg',
    '/static/images/faq_graphic.jpg',
    '/static/images/focus_sport-fb-removebg-preview.png',
    '/static/images/images-removebg-preview.png',
    '/templates/index.html',
    '/templates/takafa.html',
    '/templates/sport.html',
    '/templates/news.html',
    '/templates/arabec.html',
    '/templates/contact.html',
    '/templates/login.html',
    '/templates/post-add.html',
];

// Install event
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Caching assets');
            return cache.addAll(CACHE_ASSETS);
        })
    );
});

// Fetch event
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            return cachedResponse || fetch(event.request);
        })
    );
});

// Activate event
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        console.log('Removing old cache:', cache);
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
});


self.addEventListener('push', function(event) {
  let data = { title: 'اشعار', body: 'رسالة جديدة', url: '/' };
  if (event.data) {
    try { data = event.data.json(); } catch(e) { data.body = event.data.text(); }
  }
  const options = {
    body: data.body,
    data: { url: data.url }
  };
  event.waitUntil(self.registration.showNotification(data.title, options));
});

self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  event.waitUntil(clients.openWindow(event.notification.data.url || '/'));
});
