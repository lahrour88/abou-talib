
        document.addEventListener('DOMContentLoaded', function() {
            // الحصول على جميع الروابط والفقرات
            const toggleLinks = document.querySelectorAll('.toggle-link');

            toggleLinks.forEach(function(toggleLink) {
                toggleLink.addEventListener('click', function() {
                    const postId = toggleLink.getAttribute('data-id'); // الحصول على معرف المنشور
                    const paragraph = document.getElementById(`paragraph${postId}`); // الفقرة المرتبطة

                    if (paragraph.classList.contains('collapsed')) {
                        paragraph.classList.remove('collapsed');
                        toggleLink.textContent = 'عرض أقل';
                        toggleLink.classList.add('expanded');
                    } else {
                        paragraph.classList.add('collapsed');
                        toggleLink.textContent = 'عرض المزيد';
                        toggleLink.classList.remove('expanded');
                    }
                });
            });
        });


        let deferredPrompt;
  window.addEventListener("beforeinstallprompt", (event) => {
      event.preventDefault();
      deferredPrompt = event;
      document.getElementById("installPWA").style.display = "block";
  });

  document.getElementById("installPWA").addEventListener("click", async () => {
      if (deferredPrompt) {
          deferredPrompt.prompt();
          const { outcome } = await deferredPrompt.userChoice;
          console.log(`نتيجة التثبيت: ${outcome}`);
          deferredPrompt = null;
      }
  });

  window.addEventListener("appinstalled", () => {
      console.log("🎉 تم تثبيت التطبيق بنجاح!");
      document.getElementById("installPWA").style.display = "none";
  });

            document.addEventListener("DOMContentLoaded", function() {
                const paragraphs = document.querySelectorAll('.paragraph');
                if (paragraphs.length > 0) {
                    paragraphs.forEach(paragraph => {
                        if (paragraph) {
                            paragraph.innerHTML = paragraph.innerHTML.trim();
                        }
                    });
                }
            });

