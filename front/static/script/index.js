let audio_file = null;

window.onload = () => {
  const generated_audio = sessionStorage.getItem('generated_audio');
  const file = sessionStorage.getItem('file');
  if (generated_audio != null) {
    fetch(generated_audio)
      .then(res => res.blob())
      .then(blob => {
        const url = URL.createObjectURL(blob);
        audio.setAttribute("src", url);
        audio.style.display = 'block';
      });
  }

  if (file != null) {
    const file_name = sessionStorage.getItem('file_name');
    fetch(file)
      .then(res => res.blob())
      .then(blob => {
        audio_file = new File([blob], file_name);
        set_file_name(file_name);
      })
  }
}

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
        alert('Oops, there was an error on the server!');
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
  const body = new FormData();
  body.append("content", textarea.value);
  if (audio_file != null) {
    body.append('speaker', audio_file, audio_file.name);
  }

  const request = {
    method: 'POST',
    body: body
  }

  extract_button.disabled = true;
  generate_button.disabled = true;
  spinner_div.style.visibility = "visible";
  fetch(endpoint, request).then(response => {
    if (response.status == 400) {
      response.json().then(data => alert(data.message));
    } else if (response.status == 500) {
      alert('Oops, there was an error on the server!');
    } else if (response.ok) {
      response.blob().then(binary => {
        const reader = new FileReader();
        reader.onload = () => {
          sessionStorage.setItem('generated_audio', reader.result);
        }
        reader.readAsDataURL(binary);
        const audio_url = URL.createObjectURL(binary);
        audio.setAttribute("src", audio_url);
        audio.style.display = 'block';
        sessionStorage.setItem('generated_audio', audio_url);
      });
    }
    extract_button.disabled = false;
    generate_button.disabled = false;
    spinner_div.style.visibility = "hidden";
  })
}

function set_file_name(filename) {
  const file_name = document.getElementById('file-name');
  file_name.innerText = filename;
  file_name.style.textDecoration = 'underline';
}

function handle_file_selection() {
  const file_input = document.getElementById('file');
  const file = file_input.files[file_input.files.length - 1];
  audio_file = file;
  store_file()
  set_file_name(file.name);
}

function handle_drop(event) {
  const file = event.dataTransfer.items[0].getAsFile();
  audio_file = file;
  set_file_name(file.name);
  store_file()
  event.preventDefault();
}

function store_file() {
  const reader = new FileReader();
  reader.onload = () => {
    sessionStorage.setItem('file', reader.result);
    sessionStorage.setItem('file_name', audio_file.name);
  }
  reader.readAsDataURL(audio_file);
}

function handle_dragover(event) {
  event.preventDefault();
}

function remove_file(event) {
  const file_name = document.getElementById('file-name');
  audio_file = null;
  file_name.innerText = "No file chosen";
  file_name.style.textDecoration = 'none';
  sessionStorage.removeItem('file');
  sessionStorage.removeItem('file_name');
  event.preventDefault();
}