const host = 'http://localhost:8000';

function get_url_content() {
  const url_input = document.getElementById('url');
  const content_textarea = document.getElementById('content');
  const url = url_input.value;
  // validate url
  if (!url.match(/https?:\/\/.+/)) {
    alert('Url not valid!');
  }
  const endpoint = `${host}/api/extract?url=${url}`;
  fetch(endpoint).then(response => {
    response.json().then(payload => {
      if (response.status == 400) {
        alert(payload.message);
      } else if (response.ok) {
        content_textarea.value = payload.content;
      }
    })
  });
}