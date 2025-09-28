document.addEventListener('DOMContentLoaded', function() {
    // التحقق من وجود العناصر قبل استخدامها
    const toggleLink = document.getElementById('toggle-link');
    const paragraph = document.getElementById('paragraph');
    
    // التحقق من وجود paragraph قبل استخدامه
    if (paragraph) {
        paragraph.innerHTML = paragraph.innerHTML.trim();
        
        // التحقق من وجود toggleLink قبل إضافة event listener
        if (toggleLink) {
            toggleLink.addEventListener('click', function() {
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
        }
    }

    // معالجة العناصر الأخرى
    const elements = document.querySelectorAll('.element-selector');
    if (elements.length > 0) {
        elements.forEach(element => {
            if (element && element.innerHTML) {
                element.innerHTML = element.innerHTML.trim();
            }
        });
    }
});