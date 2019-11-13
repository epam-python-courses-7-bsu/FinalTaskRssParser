from dataclasses import dataclass


@dataclass
class Novelty:
    number_of_novelty: int
    title_of_novelty: str
    time_of_novelty: str
    source_link: str
    description: str
    images_links: str
    alt_text: str
    date_corrected: str
    main_source: str
