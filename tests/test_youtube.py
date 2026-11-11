import unittest

from youtube_ai.youtube import extract_video_id


class ExtractVideoIdTests(unittest.TestCase):
    def test_accepts_video_id(self):
        self.assertEqual(extract_video_id("II28i__Tf3M"), "II28i__Tf3M")

    def test_accepts_watch_url(self):
        self.assertEqual(
            extract_video_id("https://www.youtube.com/watch?v=II28i__Tf3M"),
            "II28i__Tf3M",
        )

    def test_accepts_short_url(self):
        self.assertEqual(
            extract_video_id("https://youtu.be/II28i__Tf3M"),
            "II28i__Tf3M",
        )

    def test_rejects_invalid_input(self):
        with self.assertRaises(ValueError):
            extract_video_id("nao-e-uma-url-valida")


if __name__ == "__main__":
    unittest.main()
