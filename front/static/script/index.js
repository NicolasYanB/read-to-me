const host = 'http://localhost:8000';

function get_url_content() {
  const url_input = document.getElementById('url');
  const content_textarea = document.getElementById('content');
  const spinner_div = document.getElementById('spinner-div');
  const extract_button = document.getElementById('extract-button');

  const url = url_input.value;
  // validate url
  if (!url.match(/https?:\/\/.+/)) {
    alert('this url is not valid!');
  }
  const endpoint = `${host}/api/extract?url=${url}`;

  extract_button.disabled = true;
  spinner_div.style.visibility = "visible";
  fetch(endpoint).then(response => {
    response.json().then(payload => {
      if (response.status == 400) {
        alert(payload.message);
      } else if (response.status == 500) {
        alert('Houve um erro no servidor');
      } else if (response.ok) {
        content_textarea.value = payload.content;
      }
      spinner_div.style.visibility = "hidden";
      extract_button.disabled = false;
    })
  });
}

function get_generated_audio() {
  const textarea = document.getElementById('content');
  const spinner_div = document.getElementById('spinner-div');
  const extract_button = document.getElementById('extract-button');
  const generate_button = document.getElementById('generate-button');
  const audio = document.getElementById('audio');

  if (textarea.value == '') {
    alert('There is no text to transform in speech!');
    return;
  }

  const endpoint = `${host}/api/generate`;
  const body = new FormData()
  body.append("content", textarea.value);

  const request = {
    method: 'POST',
    headers: {
      "Content-Type": "multipart/form-data;boundary=<calculated when request is sent>"
    },
    body: body
  }

  extract_button.disabled = true;
  generate_button.disabled = true;
  spinner_div.style.visibility = "visible";
  fetch(endpoint, request).then(response => {
    if (response.status == 400) {
      response.json().then(data => alert(data.message));
    } else if (response.status == 500) {
      alert('Houve um erro no servidor');
    } else if (response.ok) {
      response.blob().then(binary => {
        const audio_url = URL.createObjectURL(binary);
        audio.setAttribute("src", audio_url);
        audio.style.display = 'block';
      });
    }
    extract_button.disabled = false;
    generate_button.disabled = false;
    spinner_div.style.visibility = "hidden";
  })
}