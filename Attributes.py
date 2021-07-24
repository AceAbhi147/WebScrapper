

class Attributes:
    def __init__(
            self,
            image_count=None,
            title=None,
            description=None,
            rating=None,
            year=None,
            link=None,
            tags=None,
            number_of_episodes=None,
            status=None):
        self.image_count = image_count
        self.title = title
        self.description = description
        self.rating = rating
        self.year = year
        self.link = link
        self.tags = tags
        self.number_of_episodes = number_of_episodes
        self.status = status

    def __str__(self):
        return f'Image: {self.image_count}.jpg, ' \
               f'Title: {self.title}, ' \
               f'Description: {self.description}, ' \
               f'Rating: {self.rating}, ' \
               f'Year: {self.year}, ' \
               f'Link: {self.link}, ' \
               f'Tags: {self.tags}, ' \
               f'Number of Episodes: {self.number_of_episodes}, ' \
               f'Status: {self.status}'

