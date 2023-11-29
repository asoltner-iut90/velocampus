function redirectToPage(select) {
  var selectedPage = select.value;
  if (selectedPage) {
    window.location = selectedPage; // Redirection vers la page sélectionnée
  }
}