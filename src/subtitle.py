
class Subtitle:

    def __init__(self) -> None:
        self.subtitle = []
        self.location = 0
        self.lenth = 0
    
    def add_subtitle(self, subtitle: list) -> None:
        if self.subtitle == []:
            self.subtitle.append(subtitle)
            self.lenth += 1
            return True
        
        if subtitle[1] == self.subtitle[-1][1]:
            return False
        else:
            self.subtitle.append(subtitle)
            self.lenth += 1
            return True
    
    def get_subtitle(self, lenth: int = -1) -> None:
        if lenth == -1:
            location = self.location
            self.location = len(self.subtitle)
            self.lenth = 0
            return self.subtitle[location:]
        else:
            return self.subtitle[-lenth:]
    

    def get_subtitle_str(self, lenth: int = -1) -> str:
        subtitle = self.get_subtitle(lenth)
        subtitle_str = ""
        for i in subtitle:
            subtitle_str += i[0] + i[1] + "\n"
        return subtitle_str
