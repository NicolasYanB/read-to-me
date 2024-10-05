# Read to me
A website to transform any text you want into any voice you want
# Made with
- Django
- Hugging face
- coqui XTTS
# How it works
You can upload an wav audio with a little more than 5 seconds with someone talking, then you type the text you want to hear into the text area, then click in the 'generate' button,
after that you will receive an audio with the content you wrote with the voice you uploaded.

You can also extract the text from any website you want, a blog post for example, by inserting the url on the extractor input, then with the click of a button the app will extract the meaninful text of the website and put it right into the text area
so you can generate the audio with the content of any site you want.

It works with many languages and it can detect the language of the text automatically.
# Run it by yourself
To run this on your machine just clone it and run docker compose.

I strongly recommend that you run it on a machine that have a good amount of RAM and a good CPU, the model is very large and it demands a lot from both the memory and the processor
# Is it complete ?
Actually not.

I did plan to add more features, like a sign in/up and saving voices and texts.

However...

The original purpose of this app was to generate audios from newsletters and papers I use to read. However, my machine is not suitable to run this model on a large amount of text. The long execution time made it not usable on a daily basis.

However, if you want, feel free to add more features to it.
