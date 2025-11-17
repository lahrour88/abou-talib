// static/sw.js

const CACHE_NAME = 'abou-talib-cache-v2.2';

// قائمة الملفات الثابتة التي سيتم تخزينها
const ASSETS = [
  '/',  // الصفحة الرئيسية
  '/static/android-chrome-192x192.png',
  '/static/android-chrome-512x512.png',
  '/static/apple-touch-icon.png',
  '/static/favicon-16x16.png',
  '/static/favicon-32x32.png',
  '/static/favicon.ico',
  '/static/fonts/bootstrap-icons.woff',
  '/static/fonts/bootstrap-icons.woff2',
  '/static/images/242d438d75a67c92a717b2d0b8787449.webp',
  '/static/images/404.png',
  '/static/images/ai.png',
  '/static/images/blank-profile-picture-973460_1280.webp',
  '/static/images/businesswoman-using-tablet-analysis.jpg',
  '/static/images/colleagues-working-cozy-office-medium-shot.jpg',
  '/static/images/contact-us-removebg-preview.png',
  '/static/images/ConvertedPNG0-removebg-preview.png',
  '/static/images/faq_graphic.jpg',
  '/static/images/favicon.ico',
  '/static/images/icon512.png',
  '/static/images/icons-192.png',
  '/static/images/icons-512.png',
  '/static/images/journalist-is-searching-for-false-news-10961423-8798212.png',
  '/static/images/logo-abou-talib.png',
  '/static/images/rear-view-young-college-student.jpg',
  '/static/images/sport.png',
  '/static/images/takafa.png',
  '/static/images/logo.png',
  '/static/css/bootstrap-icons.css',
  '/static/css/bootstrap.min.css',
  '/static/css/chat.css',
  '/static/css/login.css',
  '/static/css/note.css',
  '/static/css/post-add.css',
  '/static/css/profile_page1.css',
  '/static/css/templatemo-topic-listing.css',
  '/static/js/bootstrap.bundle.min.js',
  '/static/js/click-scroll.js',
  '/static/js/custom.js',
  '/static/js/jquery.min.js',
  '/static/js/jquery.sticky.js',
  '/static/js/main.js',
  '/static/js/push-client.js',
  '/static/js/script.js',
  '/static/js/slider.js',
  '/static/manifest.json',
  '/static/site.webmanifest',
  '/static/robots.txt',
  '/static/sitemap.xml',
  '/static/offline.html',
  'templates/pages/index.html'
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
      return response || fetch(event.request).catch(() => caches.match('/static/offline.html'));
    })
  );
});
