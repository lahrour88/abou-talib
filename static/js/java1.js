document.addEventListener("DOMContentLoaded", function() {
    function toggleParagraph(event) {
      var toggleLink = event.target;
      var paragraphId = toggleLink.getAttribute("data-paragraph-id");
      var paragraph = document.getElementById(paragraphId);
      
      paragraph.classList.toggle("collapsed");
      toggleLink.textContent = paragraph.classList.contains("collapsed") ? "عرض المزيد" : "إخفاء";
    }
  
    // استهداف جميع روابط التبديل
    document.querySelectorAll(".toggle-link").forEach(function(link) {
      var paragraphId = link.id.replace("toggle-link", "paragraph");
      link.setAttribute("data-paragraph-id", paragraphId);
      link.addEventListener("click", toggleParagraph);
    });
  
    // تصغير جميع الفقرات عند تحميل الصفحة
    document.querySelectorAll(".paragraph").forEach(function(paragraph) {
      paragraph.classList.add("collapsed");
    });
  });
  