For the cookie file you can use [cookie-editor](https://cookie-editor.cgagnier.ca/).
When you extract use the JSON format.

You'll also need `ffmpeg` to splice together video and audio.

Regarding [fb_dtsg](https://github.com/Mroik/video-gram/blob/4df66cc9818bcf1a71dc778ad3a43765714ad836/main.py#L75),
after a while the value expires. To fix it simply check a instagram request to
graphql and replace it with the value found in it.
