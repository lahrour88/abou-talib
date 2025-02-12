const CACHE_NAME = "flask-pwa-cache-v1";
const urlsToCache = [
    // صفحات التطبيق
    "/",        
    "/arabec",        
    "/takafa",
    "/page1",
    "/login",
    "/post_add",
    
    // الملفات الثابتة
    "/static/index.css",
    "/static/menu.css", 
    "/static/profile_page1.css",
    
    // ملفات JavaScript
    "/static/js/script.js",
    "/static/js/java1.json",
    "/static/js/java.js",
    
    // Manifest
    "/static/manifest.json",
    
    // الأيقونات
    "/static/img/web-app192x192.png",
    "/static/img/web-app512x512.png",
    //image
    "/static/img/log-takafa.jpg",
    "/static/img/logo.png",
    "/static/img/mara.avif",
    "/static/img/newz.png",
    "/static/img/OIIP.jpeg",
    "/static/img/OIP.jpg",
    "/static/img/r1.jpg",
    "/static/img/th.jpg",

    // صفحة Offline مخصصة
    "/offline.html"
];

// تثبيت Service Worker وتخزين الملفات
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache);
        })
    );
    self.skipWaiting(); // إجبار Service Worker على التحديث فورًا
});

// تفعيل Service Worker وحذف الكاش القديم
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        console.log("حذف الكاش القديم:", cache);
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
    self.clients.claim(); // يجعل Service Worker الجديد يأخذ التحكم فورًا
});

// جلب الملفات من الكاش عند عدم توفر الإنترنت
self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request).catch(() => {
                return caches.match("/offline.html"); // عرض صفحة Offline عند عدم توفر الإنترنت
            });
        })
    );
});
