from random import choice, randint
from typing import Dict, List


class Image:

    def __init__(self, image: str) -> None:
        self.image: str = image

    def __repr__(self) -> str:
        return f'Image({self.image})'


class Ball:

    def __init__(self, image: Image) -> None:
        self.x_coordinate: float = 0
        self.y_coordinate: float = 0
        self.__image: Image = image

    def set_x_coordinate(self, x_coordinate: float) -> None:
        self.x_coordinate = x_coordinate

    def set_y_coordinate(self, y_coordinate: float) -> None:
        self.y_coordinate = y_coordinate

    def get_image(self) -> Image:
        return self.__image

    def __repr__(self) -> str:
        return f'Ball(x_coordinate: {self.x_coordinate}, y_coordinate: {self.y_coordinate}, image: {self.__image})'


class BallFactory:

    ball_image_cache: Dict[str, Image] = dict()

    @classmethod
    def get_ball(cls, ball_image_url: str) -> Ball:
        if ball_image_url not in cls.ball_image_cache:
            image: Image = BallFactory.fetch_ball(ball_image_url=ball_image_url)
            cls.ball_image_cache[ball_image_url] = image

        return Ball(image=cls.ball_image_cache.get(ball_image_url))

    @staticmethod
    def fetch_ball(ball_image_url: str) -> Image:
        return Image(image='010101010101010101010101010101010101010101010')  # Equivalent Binary of the Ball's image


class Game:

    def __init__(self, ball_count: int, ball_image_urls: List[str]) -> None:
        self.ball_count: int = ball_count
        self.balls: List[Ball] = list()
        for _ in range(self.ball_count):
            ball: Ball = BallFactory.get_ball(ball_image_url=choice(ball_image_urls))
            ball.set_x_coordinate(x_coordinate=randint(a=0, b=100))
            ball.set_y_coordinate(y_coordinate=randint(a=0, b=100))
            self.balls.append(ball)

    def run(self) -> None:
        ball: Ball
        for ball in self.balls:
            print(ball)


def main() -> None:
    Game(ball_count=50, ball_image_urls=['ball_image_url1.jpg -> yellow',
                                         'ball_image_url2.jpg -> blue',
                                         'ball_image_url3.jpg -> green',
                                         'ball_image_url4.jpg -> blue']).run()


if __name__ == '__main__':
    main()
