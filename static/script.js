// static/script.js
function uploadImage() {
  const formData = new FormData(document.getElementById('uploadForm'));

  // Redirect to the loading page
  window.location.href = '/loading';

  fetch('/process_image', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    // Redirect to the result page and pass the data as a query parameter
    const queryParams = new URLSearchParams(data).toString();
    window.location.href = `/result?${queryParams}`;
  })
  .catch(error => {
    console.error('Error:', error);
    // Redirect to an error page if needed
  });
}
