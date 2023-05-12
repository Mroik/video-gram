For the cookie file you can use [cookie-editor](https://cookie-editor.cgagnier.ca/).
When yuo extract use the JSON format.

Regarding [fb_dtsg](https://github.com/Mroik/video-gram/blob/88acb4de00eefc53137b5f5098e5a595147ae6e4/main.py#L46),
after a while the value expires. To fix it simply check a instagram request to graphql
and replace it with the value found in it.

`pull.sh` takes 2 arguments, the first a file containing all links to download,
one line per link. The second one is the cookie file to be fed to `main.py`.

`pull.sh` requires `yt-dlp` to be installed, and uses [litterbox](https://github.com/Mroik/my-scripts/blob/65a0fafdab00d2b5500a9c8188027a0f77886e06/litterbox.py)
to upload the MPD manifest to catbox. Ideally I'd use ffmpeg instead of having
to upload the manifest online, but there's a [bug](https://trac.ffmpeg.org/ticket/7395)
in it's XML parsing and sees some of the manifests as malformed. So for the time
being, this script uses `yt-dlp` with the aid of [catbox.moe](https://litterbox.catbox.moe/).
