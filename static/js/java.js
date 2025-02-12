document.addEventListener("DOMContentLoaded", function() {
  const menuBtn = document.getElementById('menu-btn');
  const menu = document.getElementById('menu');

  menuBtn.addEventListener('click', () => {
    menu.classList.toggle('active');
  });

  function showMore(event) {
    var toggleLink = event.target;
    var paragraphId = toggleLink.getAttribute("data-paragraph-id");
    var paragraph = document.getElementById(paragraphId);
    
    paragraph.classList.toggle("collapsed");
    toggleLink.textContent = paragraph.classList.contains("collapsed") ? "عرض المزيد" : "إخفاء";
  }

  document.querySelectorAll(".toggle-link").forEach(function(link) {
    var paragraphId = link.id.replace("toggle-link", "paragraph");
    link.setAttribute("data-paragraph-id", paragraphId);
    link.addEventListener("click", showMore);
  });

  document.querySelectorAll(".paragraph").forEach(function(paragraph) {
    paragraph.classList.add("collapsed");
  });
});
