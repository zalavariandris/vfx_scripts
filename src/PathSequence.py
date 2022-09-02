from typing import Tuple, Protocol, List, Any, Union
from pathlib import Path
import re

class PathSequence:
    def __init__(self, pattern: str, range: Tuple):
        # validate pattern to printf eg: filename.%04d.exr
        m = re.match("(.+)(%0[0-9]+d)(.+)", pattern)
        if m is None:
            raise Exception("printf pattern not recognized eg.: filename.%04d.exr")

        # set members
        self._pattern = pattern
        self._first_frame = range[0]
        self._last_frame = range[1]

    def range(self)->Tuple:
        return self._first_frame, self._last_frame

    def __len__(self)->int:
        return self._last_frame-self._first_frame+1

    def __getitem__(self, i:int)->Path:
        m = re.match("(.+)(%0[0-9]+d)(.+)", self._pattern)
        filepath, digits_format, extension = m.groups() # eg.: c:/folder/filename.  %04d  .exr
        digits_count = int( re.search("[0-9]+", digits_format).group() )
        format_pattern = f"{filepath}%0{digits_count}d{extension}"
        return Path(format_pattern % i)

    def __iter__(self):
        for i in range(self._first_frame, self._last_frame+1):
            yield self[i]
       
    @classmethod
    def from_item_on_disk(self, item_path: Path):
        # Validate filename
        # file must exist
        if not Path(item_path).exists():
            raise Exception(f"Sequence item does not exist on disk: {item_path}")

        # Find digits in filename
        stem = Path(item_path).stem # remove folder, keep filename part only without extension eg: C:/folder/filename.0548.jpeg->filename.0548
        m = re.search("([0-9]+$)", stem) # search matches anywhere in the string. $ will match only at the end.
        digits_count = m.span()[1] - m.span()[0]
        name = stem[0:m.span()[0]]
        digits = stem[m.span()[0]:m.span()[1]]

        # Compose filename search pattern
        folder = Path(item_path).parent # c:/folder
        extension = Path(item_path).suffix # .exr
        match_pattern = name + "(\d{"+str(len(digits))+"})" + extension
        format_pattern = name + "%0"+str(len(digits))+"d" + extension

        # Find item in folder by pattern
        # and collect framenumbers
        frame_numbers: List=[]
        for item in folder.iterdir():
            m = re.match(match_pattern, item.name)
            if m is not None:
                frame_number = int(m.group(1))
                frame_numbers.append(frame_number)
    
        frame_numbers.sort()

        # create Sequence object
        return PathSequence(str(folder / format_pattern), (frame_numbers[0], frame_numbers[-1]))

    def exists(self)->bool:
        for item in self:
            if not item.exists():
                return False
        return True

    def missing_frames(self)->List[int]:
        missing:List = []
        for f, item in enumerate(self):
            if not item.exists():
                missing.append(f)

        return missing

    def __repr__(self) -> str:
        return f"PathSequence({self._pattern}, ({self._first_frame}-{self._last_frame}))"

    def __str__(self) -> str:
        return f"'{self._pattern}' [{self._first_frame}-{self._last_frame}]"