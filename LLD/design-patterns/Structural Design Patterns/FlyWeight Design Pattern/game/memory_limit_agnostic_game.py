from typing import List


class Image:

    def __init__(self, image: str) -> None:
        self.image: str = image


class Ball:

    def __init__(self, x_coordinate: float, y_coordinate: float, ball_image_url: str) -> None:
        self.x_coordinate: float = x_coordinate
        self.y_coordinate: float = y_coordinate
        self.image: Image = Ball.fetch_ball(ball_image_url=ball_image_url)

    @staticmethod
    def fetch_ball(ball_image_url: str) -> Image:
        return Image(image='010101010101010101010101010101010101010101010')  # Equivalent Binary of the Ball's image

    def __repr__(self) -> str:
        return f'Ball(x_coordinate: {self.x_coordinate}, y_coordinate: {self.y_coordinate}, image: {self.image})'


class Game:

    def __init__(self, ball_count: int, ball_image_url: str) -> None:
        self.ball_count: int = ball_count
        self.balls: List[Ball] = [
            Ball(x_coordinate=0, y_coordinate=0, ball_image_url=ball_image_url)
        ] * self.ball_count

    def run(self) -> None:
        ball: Ball
        for ball in self.balls:
            print(ball)


def main() -> None:
    Game(ball_count=50, ball_image_url='ball_image_url.jpg').run()


if __name__ == '__main__':
    main()
