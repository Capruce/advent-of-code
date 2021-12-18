from dataclasses import dataclass
from math import ceil, sqrt
import re
import sys


Point = tuple[int, int]
Velocity = Point


RE = r"target area: x=(\d+)..(\d+), y=(-\d+)..(-\d+)"


@dataclass(frozen=True)
class Box:
    x0: int
    x1: int

    y0: int
    y1: int

    def __contains__(self, point: Point) -> bool:
        return (
            self.x0 <= point[0] <= self.x1
            and self.y0 <= point[1] <= self.y1
        )

    @classmethod
    def from_raw(cls, s: str) -> "Box":
        return Box(*map(int, re.match(RE, s).groups()))


def load_target() -> Box:
    with open(sys.argv[1], "r") as f:
        return Box.from_raw(f.readline())


def calc_y_max(target: Box) -> int:
    # The speed of the submarine when it returns to y=0 will be -(vy_0 + 1).
    # E.g. for vy_0 = 3
    #    6 |    |    |    |  x |  x |    |    |    |
    #    5 |    |    |  x |    |    |  x |    |    |
    #    4 |    |    |    |    |    |    |    |    |
    #    3 |    |  X |    |    |    |    |  x |    |
    #    2 |    |    |    |    |    |    |    |    |
    #    1 |    |    |    |    |    |    |    |    |
    #    0 |  X |    |    |    |    |    |    |  x |
    #    -------------------------------------------
    #      |  3 |  2 |  1 |  0 | -1 | -2 | -3 | -4 |
    #
    # The "maximum" vy the submarine can have when back at 0 without
    # overshooting the target the following step is target.y0.
    #       vy_return_max = -(vy_0_max + 1)
    #                     = target.y0
    #     -(vy_0_max + 1) = target.y0
    #            vy_0_max = -(target.y0 + 1)
    #
    # For a given vy_0, the distance travelled is its triangle number given by
    #     y = vy_0 * (vy_0 + 1) / 2
    #
    # Therefore:
    #     y_max = vy_0_max * (vy_0_max + 1) / 2
    #           = -(target.y0 + 1) * (-(target.y0 + 1) + 1) / 2
    #           = -(target.y0 + 1) * (-target.y0 - 1 + 1) / 2
    #           = -(target.y0 + 1) * -target.y0 / 2
    #           = target.y0 * (target.y0 + 1) / 2
    return target.y0 * (target.y0 + 1) // 2


def calc_vx_0_min(target: Box) -> int:
    # Due to the constant deceleration of 1 block/step, the furthest the
    # submarine will travel given a starting x-speed of vx_0 is the (vx_0)th
    # triangle number. E.g. for vx_0 = 5, the submarine will travel a
    # maximum of 5 + 4 + 3 + 2 + 1 blocks (15 = T(5))
    #
    # To guarantee the submarine reaches the target, vx_0 must be >=
    # t where T(t) is the smallest triangle number >= target.x0.
    # E.g. To ever reach a target at x=17..20, vx_0 must be >= 6
    # because 21 is the smallest triangle number >= 17 and 21 = T(6).
    #
    # target.x0 <= T(vx_0_min)
    # vx_0_min >= T^-1(target.x0)
    # vx_0_min = ceil(T^-1(target.x0))
    #
    # Working Out:
    #  T(t) = t(t + 1)/2
    # 2T(t) = t(t + 1)
    #       = t(t + 1) - 2T(t)
    #       = t^2 + t - 2T(t)
    #     t = (-1 + sqrt(1 + 8T(t))) / 2   (quadratic formula - positive root)
    #       = (sqrt(1 + 8T(t)) - 1) / 2
    return ceil((sqrt(1 + 8 * target.x0) - 1) / 2)


def step(position: Point, velocity: Velocity) -> tuple[Point, Velocity]:
    vx, vy = velocity
    new_position = (position[0] + vx, position[1] + vy)
    return new_position, (0 if vx == 0 else vx - 1, vy - 1)


def intersects_target(target: Box, velocity: Velocity) -> bool:
    location = (0, 0)
    while True:
        if location in target:
            return True

        if location[0] > target.x1 or location[1] < target.y1:
            return False

        location, velocity = step(location, velocity)


def count_intersecting_velocities(target: Box) -> int:
    count = 0

    vx_0_min = calc_vx_0_min(target)
    vx_0_max = target.x1

    vy_0_min = target.y0
    vy_0_max = -(target.y0 + 1)

    for vx_0 in range(vx_0_min, vx_0_max + 1):
        for vy_0 in range(vy_0_min, vy_0_max + 1):
            if intersects_target(target, (vx_0, vy_0)):
                count += 1

    return count


if __name__ == "__main__":
    TARGET = load_target()
    print("Part 1:", calc_y_max(TARGET))
    print("Part 2:", count_intersecting_velocities(TARGET))
