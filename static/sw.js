// عند تثبيت Service Worker
self.addEventListener('install', function(event) {
    console.log("📦 Service Worker Installing...");

    event.waitUntil(
        caches.open('sw-cache-v1').then(function(cache) {
            console.log("🛠️ Caching assets...");
            return cache.addAll([
                '/',
                '/sport',
                '/takafa',
                '/news',
                '/arabec',
                '/index.html',
                '/static/images/favicon.ico',
                '/static/manifest.json',
                '/templates/offline.html',
                '/static/css/bootstrap.min.css',
                '/static/css/bootstrap-icons.css',
                '/static/css/main.css',
                '/static/css/templatemo-topic-listing.css',
                '/static/js/bootstrap.bundle.min.js',
                '/static/js/click-scroll.js',
                '/static/js/custom.js',
                '/static/js/jquery.min.js',
                '/static/js/jquery.sticky.js',
                '/static/js/script.js'
            ]);
        }).then(() => {
            console.log("✅ Caching complete!");
            self.skipWaiting();
        }).catch(err => {
            console.error("❌ Caching failed:", err);
        })
    );
});

// عند تفعيل Service Worker
self.addEventListener('activate', function(event) {
    console.log("⚡ Service Worker Activating...");
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== 'sw-cache-v1') {
                        console.log("🗑️ Deleting old cache:", cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});
