from typing import List, Optional
from pathlib import Path

class Pointer:
    """Generates a pure path to the current directory.
    
    Args:
        path_manager: Provides access to paths.
        select_position: Generates a new point for building a path.

    Attributes:
        points (List): Stores elements for building a path.
        catalog_path (Path): The generated path to the current directory.
    """
    
    def __init__(self, path_manager, select_position) -> None:
        self.path_manager = path_manager
        self.select_position = select_position

        self.points: List[str] = []
        self.catalog_path: Optional[Path] = None

    def generate_path(self) -> None:
        """Generates an absolute path."""
        self.catalog_path = self.path_manager.root_path
        for point in self.points:
            self.catalog_path /= point

    def clear_points(self):
        """Deletes items from the list."""
        if self.points:
            self.points.clear()

    def root_point(self) -> None:
        """Generates a starting item."""
        self.clear_points()
        self.generate_path()

    def pop_point(self) -> None:
        """Deletes the last item from the list."""
        if self.points:
            self.points.pop()
            self.generate_path()

    def add_point(self) -> None:
        """Adds a new item to the list."""
        point = self.select_position.relative_path
        self.points.append(point)
        self.generate_path()
