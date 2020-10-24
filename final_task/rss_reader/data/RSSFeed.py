from dataclasses import dataclass


@dataclass
class Feed:
    """Contains title and description from channel-tag in RSS-page"""
    title: str          # title of the channel
    description: str    # channel description

    # Implemented for debugging
    def __str__(self):
        out = str(self.title)
        out += str(self.description)
        return out
