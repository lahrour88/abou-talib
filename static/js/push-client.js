const VAPID_PUBLIC_KEY = "<PUT_YOUR_VAPID_PUBLIC_KEY_HERE>";

async function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

export async function initPush() {
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    console.log('هذا المتصفح لا يدعم Push API.');
    return;
  }

  const registration = await navigator.serviceWorker.register('/service-worker.js');
  console.log('SW registered:', registration);

  const permission = await Notification.requestPermission();
  if (permission !== 'granted') {
    console.log('مستخدم رفض الإشعارات:', permission);
    return;
  }

  // الحصول على اشتراك موجود أو إنشاء واحد جديد
  let subscription = await registration.pushManager.getSubscription();
  if (!subscription) {
    subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: await urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
    });
  }

  // أرسل الاشتراك إلى الخادم (للتخزين/التحديث)
  await fetch('/subscribe', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      subscription,
      user_agent: navigator.userAgent,
      user_id: null  // ضع id المستخدم إن وجد
    })
  });

  console.log('تم إرسال الاشتراك للسيرفر');
}
