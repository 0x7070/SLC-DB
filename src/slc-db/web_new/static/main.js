window.addEventListener("DOMContentLoaded", () => {

  // Sliding popup for errors
  const popup = document.getElementById("popup");
  if (popup && popup.textContent.trim() !== "") {
    popup.classList.add("show");
    setTimeout(() => popup.classList.remove("show"), 3000);
  }

  // Live Ctrl-F style search
  const searchInput = document.getElementById("searchInput");
  if (!searchInput) return;
  const table = document.getElementById("filmsTable");
  const tbody = table.querySelector("tbody");
  const rows = Array.from(tbody.querySelectorAll("tr"));

  searchInput.addEventListener("input", () => {
    const term = searchInput.value.toLowerCase();
    rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      if (text.includes(term)) {
        row.style.display = "";
        // Highlight
        row.innerHTML = row.textContent.replace(
          new RegExp(`(${term})`, "gi"),
          "<mark>$1</mark>"
        );
      } else {
        row.style.display = "none";
      }
    });
    if (!term) {
      rows.forEach(row => {
        row.innerHTML = row.textContent;
      });
    }
  });
});