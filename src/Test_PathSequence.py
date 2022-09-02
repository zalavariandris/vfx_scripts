import unittest
from src.PathSequence import PathSequence
from pathlib import Path

class TestPathSequence(unittest.TestCase):
    def test_get_items(self):
        pattern = "c:/folder/filename.%04d.jpg"
        seq = PathSequence(pattern, (10, 15))
        self.assertEqual(seq[13], Path("c:/folder/filename.0013.jpg"))

    def test_iteration(self):
        pattern = "c:/folder/filename.%04d.jpg"
        seq = PathSequence(pattern, (10,15))
        self.assertEqual([item for item in seq], [
            Path("c:/folder/filename.0010.jpg"),
            Path("c:/folder/filename.0011.jpg"),
            Path("c:/folder/filename.0012.jpg"),
            Path("c:/folder/filename.0013.jpg"),
            Path("c:/folder/filename.0014.jpg"),
            Path("c:/folder/filename.0015.jpg")
            ])

    def test_from_item_on_disk(self):
        seq = PathSequence.from_item_on_disk("C:/Users/andris/Desktop/52_06_EXAM-half/52_06_EXAM_v04-vrayraw.0020.exr")

        self.assertEqual(seq.range(), (5,100))
        self.assertEqual(seq[5], Path("C:/Users/andris/Desktop/52_06_EXAM-half/52_06_EXAM_v04-vrayraw.0005.exr"))
        self.assertEqual(seq[29], Path("C:/Users/andris/Desktop/52_06_EXAM-half/52_06_EXAM_v04-vrayraw.0029.exr"))
        self.assertEqual(seq[100], Path("C:/Users/andris/Desktop/52_06_EXAM-half/52_06_EXAM_v04-vrayraw.0100.exr"))
      
    def test_exists(self):
        seq = PathSequence.from_item_on_disk("C:/Users/andris/Desktop/52_06_EXAM-half/52_06_EXAM_v04-vrayraw.0020.exr")
        self.assertTrue(seq.exists())

    def test_not_exists(self):
        pattern = "c:/folder/filename.%04d.jpg"
        seq = PathSequence(pattern, (10,15))

        self.assertFalse(seq.exists())

    def test_some_frames_not_exists(self):
        seq = PathSequence("C:/Users/andris/Desktop/52_06_EXAM-half/52_06_EXAM_v04-vrayraw.%04d.exr", (0,50))
        
        self.assertFalse(seq.exists())

if __name__== "__main__":
    unittest.main()