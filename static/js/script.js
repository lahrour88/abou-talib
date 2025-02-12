if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/service-worker.js')
    .then(() => console.log('Service Worker مسجل بنجاح!'))
    .catch(error => console.log('فشل التسجيل:', error));
}
