from fastapi import FastAPI
from librelyrics import LibreLyrics
from spotapi import Song

app = FastAPI(
    title="Lyrify",
    description="Lyrify",
    version="1.0.0",
)

ll = LibreLyrics()
song = Song()


@app.get("/")
def read_root():
    return "server working"


@app.get("/api/song")
def get_song(q: str):
    results = {}
    if q:
        songs = song.query_songs(q, limit=1)
        song_data = songs["data"]["searchV2"]["tracksV2"]["items"][0]["item"]["data"]
        try:
            results = {
                "id": song_data["id"],
                "name": song_data["name"],
                "album": song_data["albumOfTrack"]["name"],
                "album_id": song_data["albumOfTrack"]["id"],
                "cover": song_data["albumOfTrack"]["coverArt"]["sources"][-1]["url"],
                "artists": list(
                    map(lambda x: x["profile"]["name"], song_data["artists"]["items"])
                ),
            }
        except:
            print("Failed to get song data")

    return results


@app.get("/api/lyrics")
def get_lyrics(id: str):
    results = {"lyrics": ""}
    if id:
        response = ll.fetch("https://open.spotify.com/track/" + id)
        lrc = response.to_lrc()
        lyrics = lrc.split("\n", 4)[4]
        results["lyrics"] = lyrics

    return results
